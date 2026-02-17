document.addEventListener('DOMContentLoaded', function() {
    var $ = window.django && window.django.jQuery ? window.django.jQuery : window.jQuery;
    
    if (typeof $ === 'undefined') return;

    $(document).ready(function() {
        initializeDynamicLayerGroups();
    });

    function initializeDynamicLayerGroups() {
        var $proyectoField = $('#id_proyecto');
        var $grupoField = $('#id_grupo');
        
        if ($grupoField.length === 0) {
            $grupoField = $('select[name="grupo"]');
        }

        if ($proyectoField.length === 0 || $grupoField.length === 0) return;

        var $loadingIndicator = $('<span class="loading-groups" style="display:none; margin-left: 10px; color: #666;">Cargando...</span>');
        $grupoField.after($loadingIndicator);

        $proyectoField.on('change', function() {
            var projectId = $(this).val();
            
            if (!projectId) {
                $grupoField.empty().append('<option value="">---------</option>').prop('disabled', true);
                return;
            }

            $loadingIndicator.show();
            $grupoField.prop('disabled', true);
            
            var currentValue = $grupoField.val();

            $.ajax({
                url: '/admin/projects/layer/ajax/filter-groups-by-project/',
                type: 'GET',
                data: { 'project_id': projectId },
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function(response) {
                    if (response.success) {
                        $grupoField.empty().append('<option value="">Seleccione un grupo</option>');
                        
                        $.each(response.groups, function(index, group) {
                            $grupoField.append($('<option></option>')
                                .attr('value', group.id)
                                .text(group.nombre));
                        });

                        if (currentValue && $grupoField.find('option[value="' + currentValue + '"]').length > 0) {
                            $grupoField.val(currentValue);
                        }

                        $grupoField.prop('disabled', false);
                    }
                },
                error: function() {
                    $grupoField.prop('disabled', false);
                },
                complete: function() {
                    $loadingIndicator.hide();
                }
            });
        });

        // Handle edit case
        if ($proyectoField.val()) {
            $proyectoField.trigger('change');
        } else if ($grupoField.val()) {
            $.ajax({
                url: '/admin/projects/layer/ajax/filter-groups-by-project/',
                type: 'GET',
                data: { 'grupo_id': $grupoField.val() },
                success: function(response) {
                    if (response.success && response.project_id) {
                        $proyectoField.val(response.project_id);
                        $proyectoField.trigger('change');
                    }
                }
            });
        }
    }

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
});