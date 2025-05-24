(function($) {
    $(document).ready(function() {
        var categoryField = $('#id_category');
        var attributesModalBody = $('#attributes-modal-body');
        var attributesInputField = $('#id_attributes_data'); 
        var currentAttributes = {}; 

        function loadAttributes() {
            var selectedCategoryId = categoryField.val();

            console.log(selectedCategoryId)
            if (!selectedCategoryId) {
                attributesModalBody.html('<p class="text-danger">Please select a category first.</p>');
                return;
            }

            $.get(`/api/v1/category/view/${selectedCategoryId}/attributes`, function(data) {
                attributesModalBody.empty();


                currentAttributes = attributesInputField.val() ? JSON.parse(attributesInputField.val()) : {};

                if (data && data.length > 0) {
                    data.forEach(function(attribute) {
                        var existingValue = currentAttributes[attribute.name] || ''; 

                        var inputField = $('<input>', {
                            type: 'text',
                            name: 'attribute_' + attribute.id,
                            placeholder: 'Enter ' + attribute.name,
                            class: 'form-control mb-2',
                            'data-attribute-id': attribute.name,
                            value: existingValue 
                        });

                        var label = $('<label>', {
                            for: 'attribute_' + attribute.id,
                            text: attribute.name,
                            class: 'form-label'
                        });

                        attributesModalBody.append(label);
                        attributesModalBody.append(inputField);
                    });
                } else {
                    attributesModalBody.html('<p class="text-muted">No attributes available for this category.</p>');
                }
            }).fail(function() {
                attributesModalBody.html('<p class="text-danger">Error fetching attributes.</p>');
            });
        }

        // Open modal and load attributes
        $('.attribute-btn').click(function() {
            loadAttributes();

            var modalElement = document.getElementById('attributes-modal');
            if (typeof bootstrap !== 'undefined') {
                var modal = new bootstrap.Modal(modalElement);
                modal.show();
            } else {
                $(modalElement).modal('show');
            }
        });
        
         // "Close" is clicked
        $('#modal-close-btn').click(function () {
            const modalElement = document.getElementById('attributes-modal');
            if (typeof bootstrap !== 'undefined') {
                const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
                modal.hide();
            } else {
                $(modalElement).modal('hide');
            }
        });

        $('#modal-save-btn').click(function() {
            var attributesData = {};

            // Loop over each input field in the modal and collect the data
            $('#attributes-modal-body input').each(function() {
                var attrId = $(this).data('attribute-id');
                var attrValue = $(this).val();
                attributesData[attrId] = attrValue;
            });

            // Serialize the attributes data and store it in the hidden input field
            attributesInputField.val(JSON.stringify(attributesData));

            // Close the modal
            var modalElement = document.getElementById('attributes-modal');
            if (typeof bootstrap !== 'undefined') {
                var modal = bootstrap.Modal.getInstance(modalElement);
                modal.hide();
            } else {
                $(modalElement).modal('hide');
            }
        });
    });
})(django.jQuery);
