function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const userMessage = userInput.value.trim();

    if (userMessage) {
        // Display user message
        const userBubble = document.createElement('div');
        userBubble.classList.add('message', 'user-message');
        userBubble.innerText = userMessage;
        chatBox.appendChild(userBubble);

        // Scroll chat box to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;

        // Clear input field
        userInput.value = '';

        // Display bot response (placeholder for now)
        setTimeout(() => {
            const botBubble = document.createElement('div');
            botBubble.classList.add('message', 'bot-message');
            botBubble.innerText = "I'm here to help! How can I assist you today?";
            chatBox.appendChild(botBubble);

            // Scroll chat box to the bottom
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 500); // Delay response for realism
    }
}
