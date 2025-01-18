document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('userInput');
    const button = document.getElementById('submitBtn');
    const responseMessage = document.getElementById('responseMessage');

    button.addEventListener('click', function() {
        const userInput = input.value.trim();

        if (!userInput) {
            responseMessage.innerHTML = `<p class="error">Please enter a question!</p>`;
            return;
        }

        // 清空之前的消息
        responseMessage.innerHTML = `<p>Loading...</p>`;

        fetch('/response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: userInput }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                responseMessage.innerHTML = `<p class="error">${data.error}</p>`;
            } else {
                responseMessage.innerHTML = `<p>${data.response}</p>`;
            }
        })
        .catch(error => {
            responseMessage.innerHTML = `<p class="error">An error occurred: ${error.message}</p>`;
        });
    });
});
