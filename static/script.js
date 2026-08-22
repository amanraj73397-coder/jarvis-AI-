const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chat = document.getElementById("chat");

function addMessage(text, type) {
    const message = document.createElement("div");
    message.className = "message " + type;

    if (typeof text === "object" && text.type === "link") {
        const link = document.createElement("a");

        link.href = text.url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent = text.text;

        message.appendChild(link);
    } else {
        message.textContent = text;
    }

    chat.appendChild(message);
    chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {
    const message = input.value.trim();

    if (!message) return;

    addMessage(message, "user");
    input.value = "";
    sendButton.disabled = true;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        if (response.status === 401) {
            window.location.href = "/";
            return;
        }

        addMessage(
            data.reply || "JARVIS ko response nahi mila.",
            "jarvis"
        );

    } catch (error) {
        addMessage(
            "Server se connection nahi ho paya. 😕",
            "jarvis"
        );
    } finally {
        sendButton.disabled = false;
        input.focus();
    }
}

sendButton.addEventListener("click", sendMessage);

input.addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

async function logout() {
    try {
        await fetch("/logout");
    } finally {
        window.location.href = "/";
    }
}

input.focus();
