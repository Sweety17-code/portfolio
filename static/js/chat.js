document.addEventListener('DOMContentLoaded', () => {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWidget = document.getElementById('chat-widget');
    const closeChat = document.getElementById('close-chat');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');

    // Toggle Chat
    chatToggle.addEventListener('click', () => {
        chatWidget.classList.toggle('hidden');
        if (!chatWidget.classList.contains('hidden')) {
            chatInput.focus();
        }
    });

    closeChat.addEventListener('click', () => {
        chatWidget.classList.add('hidden');
    });

    // Send Message
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        // Add User Message
        addMessage(message, 'user');
        chatInput.value = '';
        chatInput.disabled = true;

        // Show typing indicator (optional, simplified here)
        const loadingId = addMessage('Thinking...', 'bot', true);

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // Remove loading message
            removeMessage(loadingId);
            
            if (data.error) {
                addMessage('Sorry, I encountered an error.', 'bot');
            } else {
                addMessage(data.response, 'bot');
            }
        } catch (error) {
            removeMessage(loadingId);
            addMessage('Network error. Please try again.', 'bot');
        } finally {
            chatInput.disabled = false;
            chatInput.focus();
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function addMessage(text, sender, isLoading = false) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);
        if (isLoading) msgDiv.classList.add('loading');
        msgDiv.textContent = text;
        
        const id = Date.now();
        msgDiv.dataset.id = id;

        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    function removeMessage(id) {
        const msg = chatMessages.querySelector(`[data-id="${id}"]`);
        if (msg) msg.remove();
    }
});
