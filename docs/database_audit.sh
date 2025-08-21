#!/bin/bash

# Database Audit Script for Visor I2D Humboldt Project
# This script runs comprehensive database verification queries and exports results to markdown
# Usage: ./database_audit.sh [output_file]

set -e

# Configuration
CONTAINER_NAME="visor_i2d_db"
DB_NAME="i2d_db"
DB_USER="i2d_user"
OUTPUT_FILE="${1:-database_audit_$(date +%Y%m%d_%H%M%S).md}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[AUDIT]${NC} $1"
}

# Function to check if container is running
check_container() {
    if ! docker ps --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        print_error "Container ${CONTAINER_NAME} is not running!"
        print_status "Available containers:"
        docker ps --format "table {{.Names}}\t{{.Status}}"
        exit 1
    fi
    print_status "Container ${CONTAINER_NAME} is running"
}

# Function to execute SQL query with timing and format output
execute_query() {
    local query="$1"
    local description="$2"
    local file_location="${3:-N/A}"
    local query_purpose="${4:-Database verification query}"

    print_header "Executing: $description"

    # Start timing
    local start_time=$(date +%s.%N)

    # Execute query and capture output
    local result
    result=$(docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -t -A -F'|' -c "$query" 2>&1)
    local exit_code=$?

    # End timing
    local end_time=$(date +%s.%N)
    local execution_time=$(echo "$end_time - $start_time" | bc -l)
    local execution_ms=$(echo "$execution_time * 1000" | bc -l | cut -d'.' -f1)

    if [ $exit_code -ne 0 ]; then
        print_error "Query failed: $description (${execution_ms}ms)"
        echo "**❌ Query Failed**: $description" >> "$OUTPUT_FILE"
        echo "- **Execution Time**: ${execution_ms}ms" >> "$OUTPUT_FILE"
        echo "- **File Location**: $file_location" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "$result" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        return 1
    fi

    # Format output for markdown
    echo "### $description" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "- **Execution Time**: ${execution_ms}ms" >> "$OUTPUT_FILE"
    echo "- **File Location**: $file_location" >> "$OUTPUT_FILE"
    echo "- **Purpose**: $query_purpose" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "**Query:**" >> "$OUTPUT_FILE"
    echo '```sql' >> "$OUTPUT_FILE"
    echo "$query" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "**Result:**" >> "$OUTPUT_FILE"

    if [ -n "$result" ]; then
        local result_lines=$(echo "$result" | wc -l)
        echo "- **Rows Returned**: $result_lines" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "$result" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
    else
        echo "- **Rows Returned**: 0" >> "$OUTPUT_FILE"
        echo "*No results returned*" >> "$OUTPUT_FILE"
    fi

    echo "" >> "$OUTPUT_FILE"
    echo "---" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"

    print_status "✓ Completed: $description (${execution_ms}ms)"
}

# Function to execute backend application query with sample parameters
execute_backend_query() {
    local base_query="$1"
    local description="$2"
    local file_location="$3"
    local query_purpose="$4"
    local sample_param="${5:-'01'}"  # Default sample parameter

    # Replace parameter placeholder with sample value
    local query=$(echo "$base_query" | sed "s/%s/'$sample_param'/g")

    execute_query "$query" "$description (Sample: $sample_param)" "$file_location" "$query_purpose"
}

# Function to create markdown header
create_header() {
    cat > "$OUTPUT_FILE" << EOF
# Database Audit Report - Visor I2D Humboldt Project

**Generated:** $TIMESTAMP
**Container:** $CONTAINER_NAME
**Database:** $DB_NAME
**User:** $DB_USER

## Executive Summary

This report contains the results of comprehensive database verification queries and backend application queries to document the current state of the database structure, schemas, permissions, configuration, and performance metrics.

---

EOF
}

# Function to add summary section
add_summary() {
    cat >> "$OUTPUT_FILE" << EOF

## Summary and Recommendations

### Key Findings
- Database audit completed successfully
- All queries executed from container: \`$CONTAINER_NAME\`
- Backend application queries tested with sample parameters
- Performance metrics captured for all queries
- Results captured for future comparison and troubleshooting

### Performance Summary
- Query execution times recorded in milliseconds
- Row counts documented for result set analysis
- Backend query performance validated with sample data

### Next Steps
1. Compare this report with previous audits to identify changes
2. Address any permission issues identified
3. Create missing schemas if needed
4. Update application configuration based on actual database structure
5. Optimize slow-performing queries based on execution times

### Troubleshooting
If any queries failed, check:
- Container connectivity
- User permissions
- Database availability
- Network configuration
- Table/schema existence

---

**Report End:** $(date '+%Y-%m-%d %H:%M:%S')
EOF
}

# Main execution
main() {
    print_header "Starting Database Audit for Visor I2D"
    print_status "Output file: $OUTPUT_FILE"

    # Set output file with timestamp if not provided
    if [ -z "$1" ]; then
        OUTPUT_FILE="database_audit_$(date +%Y%m%d_%H%M%S).md"
    else
        OUTPUT_FILE="$1"
        # If output file starts with "docs/" and we're already in docs directory, remove the prefix
        if [[ "$OUTPUT_FILE" == docs/* ]] && [[ "$(basename "$PWD")" == "docs" ]]; then
            OUTPUT_FILE="${OUTPUT_FILE#docs/}"
        fi
    fi

    # Check prerequisites
    check_container

    # Create markdown header
    create_header

    # Add section for infrastructure queries
    echo "## Database Infrastructure Verification" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"

    # Execute all verification queries
    print_header "Running Schema Verification Queries"

    # 1. Basic database information
    execute_query "SELECT current_user, current_database(), version();" "Database Connection Information" "System Query" "Verify database connectivity and version"

    # 2. All schemas
    execute_query "SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;" "All Available Schemas" "System Query" "List all database schemas"

    # 3. Accessible schemas
    execute_query "SELECT nspname AS schema_name FROM pg_namespace WHERE has_schema_privilege(current_user, nspname, 'USAGE') ORDER BY nspname;" "Schemas Accessible to Current User" "System Query" "Check schema access permissions"

    # 4. Current search path
    execute_query "SHOW search_path;" "Current Search Path" "System Query" "Verify Django search path configuration"

    # 5. Specific schema existence check
    execute_query "SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = 'capas_base') AS capas_base_exists, EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = 'geovisor') AS geovisor_exists, EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = 'django') AS django_exists, EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = 'gbif_consultas') AS gbif_consultas_exists;" "Expected Schemas Existence Check" "System Query" "Validate expected schema configuration"

    # 6. Schema permissions detailed
    execute_query "SELECT n.nspname AS schema_name, has_schema_privilege(current_user, n.nspname, 'USAGE') AS can_use, has_schema_privilege(current_user, n.nspname, 'CREATE') AS can_create FROM pg_namespace n WHERE n.nspname NOT LIKE 'pg_%' AND n.nspname != 'information_schema' ORDER BY n.nspname;" "Detailed Schema Permissions" "System Query" "Analyze user permissions per schema"

    # 7. Tables in each accessible schema
    execute_query "SELECT schemaname, tablename, tableowner FROM pg_tables WHERE schemaname NOT IN ('information_schema', 'pg_catalog') ORDER BY schemaname, tablename;" "Tables by Schema" "System Query" "Inventory all accessible tables"

    # 8. Database size information
    execute_query "SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) AS size FROM pg_database ORDER BY pg_database_size(pg_database.datname) DESC;" "Database Sizes" "System Query" "Monitor database storage usage"

    # 9. Connection information
    execute_query "SELECT datname, usename, application_name, client_addr, state, query_start FROM pg_stat_activity WHERE datname = current_database();" "Current Database Connections" "System Query" "Monitor active database connections"

    # 10. PostGIS information (if available)
    execute_query "SELECT PostGIS_Version();" "PostGIS Version Information" "System Query" "Verify PostGIS extension status" || true

    # 11. Extensions installed
    execute_query "SELECT extname, extversion FROM pg_extension ORDER BY extname;" "Installed Extensions" "System Query" "List all database extensions"

    # 12. Table counts per schema
    execute_query "SELECT schemaname, COUNT(*) as table_count FROM pg_tables WHERE schemaname NOT IN ('information_schema', 'pg_catalog') GROUP BY schemaname ORDER BY schemaname;" "Table Counts by Schema" "System Query" "Analyze table distribution per schema"

    # 13. Index information
    execute_query "SELECT schemaname, tablename, indexname, indexdef FROM pg_indexes WHERE schemaname NOT IN ('information_schema', 'pg_catalog') ORDER BY schemaname, tablename, indexname;" "Database Indexes" "System Query" "Inventory database indexes for optimization"

    # 14. Foreign key constraints
    execute_query "SELECT tc.table_schema, tc.constraint_name, tc.table_name, kcu.column_name, ccu.table_schema AS foreign_table_schema, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name FROM information_schema.table_constraints AS tc JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name AND ccu.table_schema = tc.table_schema WHERE tc.constraint_type = 'FOREIGN KEY' ORDER BY tc.table_schema, tc.table_name;" "Foreign Key Constraints" "System Query" "Document referential integrity constraints"

    # Add section for backend application queries
    echo "## Backend Application Query Performance" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "This section tests the actual queries used by the Visor I2D backend application with sample parameters to measure real-world performance." >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"

    print_header "Running Backend Application Queries"

    # Get sample parameters dynamically from database
    print_status "🔍 Getting sample parameters from database..."

    # Get a sample department code
    SAMPLE_DEPT=$(docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT codigo FROM gbif_consultas.dpto_queries WHERE codigo IS NOT NULL LIMIT 1;" 2>/dev/null | xargs)
    if [ -z "$SAMPLE_DEPT" ]; then
        SAMPLE_DEPT="05"  # Fallback
    fi

    # Get a sample municipality code
    SAMPLE_MPIO=$(docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT codigo FROM gbif_consultas.mpio_queries WHERE codigo IS NOT NULL LIMIT 1;" 2>/dev/null | xargs)
    if [ -z "$SAMPLE_MPIO" ]; then
        SAMPLE_MPIO="05001"  # Fallback
    fi

    # Get a sample municipality name for search
    SAMPLE_MPIO_NAME=$(docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT SUBSTRING(nombre, 1, 5) FROM capas_base.mpio_politico WHERE nombre IS NOT NULL LIMIT 1;" 2>/dev/null | xargs)
    if [ -z "$SAMPLE_MPIO_NAME" ]; then
        SAMPLE_MPIO_NAME="Medell"  # Fallback
    fi

    print_status "📊 Using sample parameters: Dept=$SAMPLE_DEPT, Mpio=$SAMPLE_MPIO, Search=$SAMPLE_MPIO_NAME"

    # Backend Query 1: Department Biodiversity Data
    execute_query "SELECT DISTINCT ON (tipo) codigo, nombre, tipo, species, endemicas, exoticas, registers FROM gbif_consultas.dpto_queries WHERE codigo = '$SAMPLE_DEPT' AND tipo IS NOT NULL LIMIT 10;" "Department Biodiversity Data by Code (Sample: $SAMPLE_DEPT)" "applications/dpto/views.py:11-12" "Retrieve distinct biodiversity data types for a specific department"

    # Backend Query 2: Department Threatened Species
    execute_query "SELECT codigo, nombre, tipo, amenazadas FROM gbif_consultas.dpto_amenazas WHERE codigo = '$SAMPLE_DEPT' AND tipo IS NOT NULL LIMIT 10;" "Department Threatened Species Data (Sample: $SAMPLE_DEPT)" "applications/dpto/views.py:19-20" "Retrieve threatened species data for a specific department"

    # Backend Query 3: Municipality Biodiversity Data
    execute_query "SELECT DISTINCT ON (tipo) codigo, nombre, tipo, species, endemicas, exoticas, registers FROM gbif_consultas.mpio_queries WHERE codigo = '$SAMPLE_MPIO' AND tipo IS NOT NULL LIMIT 10;" "Municipality Biodiversity Data by Code (Sample: $SAMPLE_MPIO)" "applications/mupio/views.py:11-12" "Retrieve distinct biodiversity data types for a specific municipality"

    # Backend Query 4: Municipality Threatened Species
    execute_query "SELECT codigo, nombre, tipo, amenazadas FROM gbif_consultas.mpio_amenazas WHERE codigo = '$SAMPLE_MPIO' AND tipo IS NOT NULL LIMIT 10;" "Municipality Threatened Species Data (Sample: $SAMPLE_MPIO)" "applications/mupio/views.py:19-20" "Retrieve threatened species data for a specific municipality"

    # Backend Query 5: GBIF Information
    execute_query "SELECT id, download_date, doi FROM gbif_consultas.gbif_info LIMIT 10;" "GBIF Information Retrieval" "applications/gbif/views.py:19-20" "Retrieve all GBIF download information and metadata"

    # Backend Query 6: Municipality Search (with accent handling)
    execute_query "SELECT codigo, dpto_nombre, nombre, nombre_unaccented FROM capas_base.mpio_politico WHERE (nombre ILIKE '%$SAMPLE_MPIO_NAME%' OR nombre_unaccented ILIKE '%$SAMPLE_MPIO_NAME%') LIMIT 5;" "Municipality Search by Name (Sample: $SAMPLE_MPIO_NAME)" "applications/mupiopolitico/views.py:13-15" "Search municipalities by name with accent handling"

    # Backend Query 7: Check if gbif.gbif table exists, if not use alternative
    GBIF_TABLE_EXISTS=$(docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'gbif' AND table_name = 'gbif');" 2>/dev/null | xargs)

    if [ "$GBIF_TABLE_EXISTS" = "t" ]; then
        # Backend Query 7: GBIF Records Export by Municipality
        execute_query "SELECT codigo_mpio, codigo_dpto, reino, filo, clase, orden, familia, genero, especie, fecha_observacion, latitud, longitud FROM gbif.gbif WHERE codigo_mpio = '$SAMPLE_MPIO' LIMIT 10;" "GBIF Records Export by Municipality (Sample: $SAMPLE_MPIO)" "applications/gbif/views.py:52" "Export GBIF records for a specific municipality"

        # Backend Query 8: GBIF Records Export by Department
        execute_query "SELECT codigo_mpio, codigo_dpto, reino, filo, clase, orden, familia, genero, especie, fecha_observacion, latitud, longitud FROM gbif.gbif WHERE codigo_dpto = '$SAMPLE_DEPT' LIMIT 10;" "GBIF Records Export by Department (Sample: $SAMPLE_DEPT)" "applications/gbif/views.py:52" "Export GBIF records for a specific department"
    else
        # Alternative queries using gbif_consultas schema
        execute_query "SELECT 'gbif.gbif table not found - using alternative query' as note, codigo, nombre, tipo, species, registers FROM gbif_consultas.mpio_queries WHERE codigo = '$SAMPLE_MPIO' LIMIT 10;" "GBIF Records Export by Municipality - Alternative (Sample: $SAMPLE_MPIO)" "applications/gbif/views.py:52" "Export GBIF records for a specific municipality (alternative query)"

        execute_query "SELECT 'gbif.gbif table not found - using alternative query' as note, codigo, nombre, tipo, species, registers FROM gbif_consultas.dpto_queries WHERE codigo = '$SAMPLE_DEPT' LIMIT 10;" "GBIF Records Export by Department - Alternative (Sample: $SAMPLE_DEPT)" "applications/gbif/views.py:52" "Export GBIF records for a specific department (alternative query)"
    fi

    # Backend Query 9: Check if species list table exists
    SPECIES_TABLE_EXISTS=$(docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'gbif' AND table_name = 'lista_especies_consulta');" 2>/dev/null | xargs)

    if [ "$SPECIES_TABLE_EXISTS" = "t" ]; then
        # Backend Query 9: Species List Export by Municipality
        execute_query "SELECT DISTINCT reino, filo, clase, orden, familia, genero, especies, endemicas, amenazadas, exoticas FROM gbif.lista_especies_consulta WHERE codigo_mpio = '$SAMPLE_MPIO' LIMIT 10;" "Species List Export by Municipality (Sample: $SAMPLE_MPIO)" "applications/gbif/views.py:53-56" "Export distinct species list for a municipality"

        # Backend Query 10: Species List Export by Department
        execute_query "SELECT DISTINCT reino, filo, clase, orden, familia, genero, especies, endemicas, amenazadas, exoticas FROM gbif.lista_especies_consulta WHERE codigo_dpto = '$SAMPLE_DEPT' LIMIT 10;" "Species List Export by Department (Sample: $SAMPLE_DEPT)" "applications/gbif/views.py:53-56" "Export distinct species list for a department"
    else
        # Alternative queries using available data
        execute_query "SELECT 'gbif.lista_especies_consulta table not found - using alternative query' as note, codigo, nombre, tipo, species, endemicas, exoticas FROM gbif_consultas.mpio_queries WHERE codigo = '$SAMPLE_MPIO' LIMIT 10;" "Species List Export by Municipality - Alternative (Sample: $SAMPLE_MPIO)" "applications/gbif/views.py:53-56" "Export distinct species list for a municipality (alternative query)"

        execute_query "SELECT 'gbif.lista_especies_consulta table not found - using alternative query' as note, codigo, nombre, tipo, species, endemicas, exoticas FROM gbif_consultas.dpto_queries WHERE codigo = '$SAMPLE_DEPT' LIMIT 10;" "Species List Export by Department - Alternative (Sample: $SAMPLE_DEPT)" "applications/gbif/views.py:53-56" "Export distinct species list for a department (alternative query)"
    fi

    # Additional Backend Query: Get available department and municipality codes for reference
    execute_query "SELECT DISTINCT codigo, nombre FROM gbif_consultas.dpto_queries WHERE codigo IS NOT NULL ORDER BY codigo LIMIT 10;" "Available Department Codes" "System Query" "List available department codes for testing"

    execute_query "SELECT DISTINCT codigo, nombre FROM gbif_consultas.mpio_queries WHERE codigo IS NOT NULL ORDER BY codigo LIMIT 10;" "Available Municipality Codes" "System Query" "List available municipality codes for testing"

    # Add summary
    add_summary

    print_status "✅ Database audit completed successfully!"
    print_status "Report saved to: $OUTPUT_FILE"
    print_status "File size: $(du -h "$OUTPUT_FILE" | cut -f1)"

    # Display quick summary
    echo ""
    print_header "Quick Summary:"
    echo "📄 Report file: $OUTPUT_FILE"
    echo "🐳 Container: $CONTAINER_NAME"
    echo "🗄️  Database: $DB_NAME"
    echo "👤 User: $DB_USER"
    echo "⏰ Generated: $TIMESTAMP"
    echo "🔍 Infrastructure queries: 14"
    echo "🚀 Backend queries tested: 10"
    echo "⚡ Performance timing: Enabled"
}

# Help function
show_help() {
    cat << EOF
Database Audit Script for Visor I2D Humboldt Project

Usage: $0 [output_file]

Arguments:
  output_file    Optional. Path to output markdown file
                 Default: database_audit_YYYYMMDD_HHMMSS.md

Examples:
  $0                                    # Use default filename
  $0 audit_report.md                   # Custom filename
  $0 docs/database_audit_latest.md     # Custom path and filename

This script will:
- Verify the PostgreSQL container is running
- Execute comprehensive database verification queries (14 queries)
- Test backend application queries with sample parameters (10 queries)
- Measure execution time for all queries in milliseconds
- Export results to a formatted markdown report
- Provide troubleshooting information

Requirements:
- Docker must be running
- Container '$CONTAINER_NAME' must be running
- User must have access to execute docker commands
- 'bc' command must be available for timing calculations
EOF
}

# Check for help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# Check if bc is available for timing calculations
if ! command -v bc &> /dev/null; then
    print_error "The 'bc' command is required for timing calculations but is not installed."
    print_status "Please install bc: sudo apt-get install bc"
    exit 1
fi

# Run main function
main "$@"
