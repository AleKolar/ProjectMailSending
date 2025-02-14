$(document).ready(function() {
    // Настройка CSRF-токена для всех AJAX-запросов
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Определяем CSRF-токен
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    // Функция для получения CSRF-токена из cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Проверяем, начинается ли cookie с нужного имени
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Обработчик изменения чекбокса
    $('#sendToAll').change(function() {
        const individualFields = $('#individualFields');
        const sendToAllValue = $('#sendToAllValue');
        if ($(this).is(':checked')) {
            individualFields.hide();
            sendToAllValue.val('true'); // Устанавливаем значение для отправки всем
        } else {
            individualFields.show();
            sendToAllValue.val('false'); // Устанавливаем значение для отправки фильтрованным
        }
    });

    // Обработчик отправки формы
    $('#createNewsletterForm').on('submit', function(e) {
        e.preventDefault(); // Отменяем стандартное поведение формы

        $.ajax({
            type: 'POST',
            url: '/create_newsletter/', // URL для отправки
            data: $(this).serialize(), // Сериализуем данные формы
            success: function(response) {
                alert('Рассылка успешно создана и будет отправлена!');
                $('#createNewsletterModal').modal('hide'); // Закрываем модальное окно
            },
            error: function(response) {
                alert('Ошибка при создании рассылки.');
            }
        });
    });
});