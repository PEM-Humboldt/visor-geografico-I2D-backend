// Wait for Django admin to load jQuery
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded fired - starting dynamic layer groups initialization');

    // Use Django's jQuery when available, fallback to window.jQuery
    var $ = window.django && window.django.jQuery ? window.django.jQuery : window.jQuery;

    if (typeof $ === 'undefined') {
        console.error('jQuery is not available. Make sure Django admin is properly loaded.');
        return;
    }

    console.log('jQuery found:', typeof $);

    'use strict';

    // Initialize when jQuery is ready
    $(document).ready(function() {
        console.log('jQuery document ready - initializing dynamic layer groups');
        initializeDynamicLayerGroups();
    });

    function initializeDynamicLayerGroups() {
        console.log('initializeDynamicLayerGroups called');

        // Find the project field
        var $proyectoField = $('#id_proyecto');
        
        // Find the grupo field - try multiple selectors
        var $grupoField = $('#id_grupo');
        if ($grupoField.length === 0) {
            $grupoField = $('select[name="grupo"]');
        }

        console.log('Proyecto field found:', $proyectoField.length > 0, 'ID:', $proyectoField.attr('id'));
        console.log('Grupo field found:', $grupoField.length > 0, 'ID:', $grupoField.attr('id'), 'Name:', $grupoField.attr('name'));

        if ($proyectoField.length === 0 || $grupoField.length === 0) {
            console.error('Dynamic layer groups: Required fields not found');
            return;
        }

        console.log('Dynamic layer groups: Initializing...');

        // Add loading indicator
        var $loadingIndicator = $('<span class="loading-groups" style="display:none; margin-left: 10px; color: #666;">Cargando grupos...</span>');
        $grupoField.after($loadingIndicator);

        // Handle project selection change
        $proyectoField.on('change', function() {
            var projectId = $(this).val();
            console.log('Project selection changed. Project ID:', projectId);

            if (!projectId) {
                console.log('No project selected, clearing groups');
                $grupoField.empty().append('<option value="">---------</option>');
                $grupoField.prop('disabled', true);
                return;
            }

            console.log('Making AJAX request for project:', projectId);

            // Show loading indicator
            $loadingIndicator.show();
            $grupoField.prop('disabled', true);

            // Get CSRF token for Django
            var csrfToken = $('[name=csrfmiddlewaretoken]').val() ||
                           document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                           getCookie('csrftoken');

            // Make AJAX request to get groups for selected project
            $.ajax({
                url: '/admin/projects/layer/ajax/filter-groups-by-project/',
                type: 'GET',
                data: {
                    'project_id': projectId
                },
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function(response) {
                    console.log('AJAX success:', response);

                    if (response.success) {
                        // Store the current selected value before clearing
                        var currentSelectedValue = $grupoField.val();
                        console.log('Current selected grupo value before clear:', currentSelectedValue);

                        // Clear existing options
                        $grupoField.empty();

                        // Add default option
                        $grupoField.append('<option value="">Seleccione un grupo</option>');

                        // Add groups
                        $.each(response.groups, function(index, group) {
                            var $option = $('<option></option>')
                                .attr('value', group.id)
                                .text(group.nombre);
                            $grupoField.append($option);
                        });

                        // Restore the previously selected value if it exists in the new options
                        if (currentSelectedValue && $grupoField.find('option[value="' + currentSelectedValue + '"]').length > 0) {
                            $grupoField.val(currentSelectedValue);
                            console.log('Restored previous selection:', currentSelectedValue);
                        }

                        // Enable the field
                        $grupoField.prop('disabled', false);

                        console.log('Grupo field final state:', {
                            value: $grupoField.val(),
                            selectedText: $grupoField.find('option:selected').text(),
                            optionsCount: $grupoField.find('option').length
                        });

                        // Show success message
                        showMessage('Grupos cargados para el proyecto: ' + response.project_name + ' (' + response.groups.length + ' grupos)', 'success');

                    } else {
                        console.error('AJAX response error:', response.error);
                        showMessage('Error: ' + (response.error || 'No se pudieron cargar los grupos'), 'error');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('AJAX error:', status, error);
                    var errorMessage = 'Error al cargar los grupos';
                    if (xhr.status === 403) {
                        errorMessage = 'Error de permisos: No tiene autorización para acceder a esta función';
                    } else if (xhr.status === 404) {
                        errorMessage = 'Error: Endpoint no encontrado';
                    }
                    showMessage(errorMessage, 'error');
                    $grupoField.prop('disabled', false);
                },
                complete: function() {
                    console.log('AJAX request completed');
                    $loadingIndicator.hide();
                }
            });
        });

        // If editing existing layer, trigger change to load groups
        if ($proyectoField.val()) {
            console.log('Editing existing layer, loading groups for project:', $proyectoField.val());
            $proyectoField.trigger('change');
        } else if ($grupoField.val()) {
            // If no project is selected but grupo has a value (editing case),
            // find the project from the selected grupo and trigger the load
            console.log('Editing existing layer with grupo:', $grupoField.val(), 'but no project selected');
            
            // Make AJAX request to get the project for this grupo
            $.ajax({
                url: '/admin/projects/layer/ajax/filter-groups-by-project/',
                type: 'GET',
                data: {
                    'grupo_id': $grupoField.val()
                },
                success: function(response) {
                    if (response.success && response.project_id) {
                        console.log('Found project for grupo:', response.project_id);
                        $proyectoField.val(response.project_id);
                        $proyectoField.trigger('change');
                    }
                },
                error: function() {
                    console.log('Could not determine project for existing grupo');
                }
            });
        }

        console.log('Setup complete.');
    }

    function showMessage(message, type) {
        // Remove existing messages
        $('.dynamic-message').remove();

        // Create message element
        var messageClass = type === 'error' ? 'errornote' : 'success';
        var $message = $('<div class="dynamic-message ' + messageClass + '" style="margin: 10px 0; padding: 8px 12px; border-radius: 4px;">' + message + '</div>');

        // Insert message after the proyecto field
        $('#id_proyecto').closest('.form-row').after($message);

        // Auto-hide success messages after 3 seconds
        if (type === 'success') {
            setTimeout(function() {
                $message.fadeOut(500, function() {
                    $(this).remove();
                });
            }, 3000);
        }
    }

    // Helper function to get CSRF cookie
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Add CSS for better visual feedback
    $(document).ready(function() {
        if ($('head style[data-dynamic-layer-admin]').length === 0) {
            $('<style data-dynamic-layer-admin="true">')
                .prop('type', 'text/css')
                .html(`
                    .proyecto-selector:focus {
                        border-color: #4CAF50 !important;
                        box-shadow: 0 0 5px rgba(76, 175, 80, 0.3) !important;
                    }
                    .grupo-selector:disabled {
                        background-color: #f5f5f5 !important;
                        color: #999 !important;
                    }
                    .loading-groups {
                        animation: pulse 1.5s ease-in-out infinite alternate;
                    }
                    @keyframes pulse {
                        from { opacity: 1; }
                        to { opacity: 0.5; }
                    }
                    .dynamic-message.success {
                        background-color: #d4edda;
                        border: 1px solid #c3e6cb;
                        color: #155724;
                    }
                    .dynamic-message.errornote {
                        background-color: #f8d7da;
                        border: 1px solid #f5c6cb;
                        color: #721c24;
                    }
                `)
                .appendTo('head');
        }
    });
});