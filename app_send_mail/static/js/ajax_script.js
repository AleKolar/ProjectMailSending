$(document).ready(function() {
    $('#createNewsletterForm').on('submit', function(e) {
        e.preventDefault(); // Отменяем стандартное поведение формы

        $.ajax({
            type: 'POST',
            url: '/send_newsletter/', // URL, к которому будет отправлен запрос
            data: $(this).serialize(), // Сериализуем данные формы
            success: function(response) {
                alert('Рассылка успешно отправлена!');
                $('#createNewsletterModal').modal('hide'); // Закрываем модальное окно
            },
            error: function(response) {
                alert('Ошибка при отправке рассылки.');
            }
        });
    });
});