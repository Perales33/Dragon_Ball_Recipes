$(document).ready(function() {
    var detailCount = 0; // Contador para los detalles de la receta

    // Función para actualizar los números de los pasos y los IDs de los campos
    function updateDetailNumbers() {
        $('.detail').each(function(index) {
            $(this).find('h4').text('Paso ' + (index + 1)); // Actualiza el título del paso

            // Actualiza los IDs de los campos de entrada y área de texto
            $(this).find('input, textarea').each(function() {
                var id = $(this).attr('id');
                if (id) {
                    var newId = id.replace(/\d+$/, (index + 1)); // Reemplaza el número al final del ID
                    $(this).attr('id', newId);
                }
            });
        });
    }

    // Función para mostrar u ocultar los botones de eliminar según el número de detalles
    function updateRemoveButtons() {
        $('.remove-detail').each(function() {
            if ($('.detail').length > 1) {
                $(this).show(); // Muestra el botón si hay más de un detalle
            } else {
                $(this).hide(); // Oculta el botón si hay solo un detalle
            }
        });
    }

    // Maneja el clic en el botón "Añadir Detalle"
    $('#add-detail').click(function() {
        detailCount++; // Incrementa el contador de detalles
        $('#details-container').append(`
            <div class="detail">
                <h4>Paso ${detailCount}</h4>
                <div class="form-group">
                    <label for="step-number-${detailCount}">Número del Paso</label>
                    <input type="number" id="step-number-${detailCount}" name="step_numbers[]" class="form-control" value="${detailCount}" required>
                </div>
                <div class="form-group">
                    <label for="ingredient-${detailCount}">Ingrediente</label>
                    <input type="text" id="ingredient-${detailCount}" name="ingredients[]" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="quantity-${detailCount}">Cantidad</label>
                    <input type="text" id="quantity-${detailCount}" name="quantities[]" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="step-description-${detailCount}">Descripción del Paso</label>
                    <textarea id="step-description-${detailCount}" name="step_descriptions[]" class="form-control" rows="2" required></textarea>
                </div>
                <button type="button" class="btn btn-danger btn-sm remove-detail">Eliminar Detalle</button>
            </div>
        `);
        updateRemoveButtons(); // Actualiza la visibilidad de los botones de eliminar
    });

    // Maneja el clic en los botones "Eliminar Detalle"
    $('#details-container').on('click', '.remove-detail', function() {
        $(this).closest('.detail').remove(); // Elimina el detalle
        detailCount--; // Decrementa el contador de detalles
        updateDetailNumbers(); // Actualiza los números de los pasos
        updateRemoveButtons(); // Actualiza la visibilidad de los botones de eliminar
    });

    updateRemoveButtons(); // Inicializa los botones al cargar la página
});
