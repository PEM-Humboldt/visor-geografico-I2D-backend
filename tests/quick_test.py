#!/usr/bin/env python3
"""
Quick Django GIS Test - Simple verification script
"""
import sys
sys.path.append('/project')

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'i2dbackend.settings.local')
django.setup()

from applications.dpto.models import DptoQueries
from applications.mupio.models import MpioQueries

print("🚀 Quick Django GIS Test")
print("=" * 25)

# Test 1: Count records
dpto_count = DptoQueries.objects.count()
mpio_count = MpioQueries.objects.count()
print(f"✅ Departments: {dpto_count}")
print(f"✅ Municipalities: {mpio_count}")

# Test 2: Geometry operations
dept = DptoQueries.objects.first()
if dept and dept.geom:
    print(f"✅ Sample: {dept.nombre}")
    print(f"✅ Area: {dept.geom.area:.4f}")
    print(f"✅ Type: {dept.geom.geom_type}")
else:
    print("❌ No geometry data")

print("🎯 Test completed!")
