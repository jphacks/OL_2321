$('#send-btn').on('click', function () {
    const message = $('#message-input').val();
    if (message.trim()) {
        $('#chatbox').append('<div style="text-align: right; margin: 10px; color: blue;">' + message + '</div>');
        $('#message-input').val('');

        // Make AJAX request here to Flask endpoint
        $.ajax({
            url: '/message',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'message': message }),
            success: function (response) {
                $('#chatbox').append('<div style="text-align: left; margin: 10px; color: green;">' + response.message + '</div>');
                const chatbox = document.getElementById("chatbox");
                chatbox.scrollTop = chatbox.scrollHeight;
            }
        });
    }
});

// Pressing enter to send message
$('#message-input').keypress(function (e) {
    if (e.which == 13) {
        $('#send-btn').click();
        return false;
    }
});
