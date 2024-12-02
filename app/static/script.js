async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const userMessage = userInput.value.trim();

    if (userMessage) {
        // Display user message
        const userBubble = document.createElement('div');
        userBubble.classList.add('message', 'user-message');
        userBubble.innerText = userMessage;
        chatBox.appendChild(userBubble);
        chatBox.scrollTop = chatBox.scrollHeight;
        userInput.value = '';

        try {
            // Send user message to Flask backend
            const response = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userMessage })
            });

            if (response.ok) {
                const responseData = await response.json();

                // Display chatbot response
                const botBubble = document.createElement('div');
                botBubble.classList.add('message', 'bot-message');
                botBubble.innerText = responseData.response;
                chatBox.appendChild(botBubble);
                chatBox.scrollTop = chatBox.scrollHeight;
            } else {
                throw new Error('Failed to fetch response from server.');
            }
        } catch (error) {
            const errorBubble = document.createElement('div');
            errorBubble.classList.add('message', 'bot-message');
            errorBubble.innerText = "Sorry, I'm having trouble connecting to the server.";
            chatBox.appendChild(errorBubble);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }
}

function stripMarkup(text) {
    const div = document.createElement('div');
    div.innerHTML = text;
    return div.textContent || div.innerText || "";
}

async function submitSurvey() {
    const form = document.getElementById('survey-form');
    const surveyData = {
        q1: form.q1.value,
        q2: form.q2.value,
        q3: form.q3.value,
    };

    try {
        const response = await fetch('http://localhost:5000/survey', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(surveyData),
        });

        if (response.ok) {
            alert('Thank you for your feedback!');
            form.reset(); // Clear the form after submission
        } else {
            alert('There was an error submitting your survey.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while submitting your survey.');
    }
}
