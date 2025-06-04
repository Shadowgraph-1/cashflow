(function($) {
    $(document).ready(function() {
        var categoryField = $('#id_category');
        var subcategoryField = $('#id_subcategory');
        var typeField = $('#id_type');
        var amountField = $('#id_amount');
        var form = $('form');

        function updateSubcategories() {
            var categoryId = categoryField.val();
            if (categoryId) {
                $.ajax({
                    url: '/admin/get_subcategories/',
                    data: { category_id: categoryId },
                    success: function(data) {
                        console.log('Полученные подкатегории:', data);
                        subcategoryField.empty();
                        subcategoryField.append('<option value="">---------</option>');
                        $.each(data, function(index, item) {
                            subcategoryField.append(
                                $('<option>').val(item.id).text(item.name)
                            );
                        });
                        var currentSubcategory = subcategoryField.data('current');
                        if (currentSubcategory) {
                            subcategoryField.val(currentSubcategory);
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error('Ошибка AJAX:', error, xhr.status, xhr.responseText);
                        alert('Ошибка загрузки подкатегорий. Пожалуйста, войдите в админку.');
                    }
                });
            } else {
                subcategoryField.empty();
                subcategoryField.append('<option value="">---------</option>');
            }
        }

        function filterCategories() {
            var typeId = typeField.val();
            categoryField.empty();
            categoryField.append('<option value="">Выберите категорию</option>');
            if (typeId) {
                $('option', categoryField).each(function() {
                    if ($(this).data('type') == typeId || $(this).val() == "") {
                        $(this).show();
                    } else {
                        $(this).hide();
                    }
                });
            }
            updateSubcategories();
        }

        form.on('submit', function(event) {
            var amount = amountField.val();
            var type = typeField.val();
            var category = categoryField.val();

            if (!amount || amount <= 0) {
                event.preventDefault();
                alert('Сумма должна быть больше 0!');
                return false;
            }

            if (!type) {
                event.preventDefault();
                alert('Пожалуйста, выберите тип!');
                return false;
            }

            if (!category) {
                event.preventDefault();
                alert('Пожалуйста, выберите категорию!');
                return false;
            }
        });


        $.ajax({
            url: '/check-auth/',
            success: function(data) {
                if (data.is_authenticated) {
                    updateSubcategories();
                }
            },
            error: function() {
                alert('Ошибка проверки авторизации. Пожалуйста, войдите в админку.');
            }
        });

        typeField.change(filterCategories);
        categoryField.change(updateSubcategories);
    });
})(jQuery);