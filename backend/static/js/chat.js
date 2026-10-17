// ==========================
// CONFIG
// ==========================
let currentEmotion = "neutral"; // updated from emotion.js
const chatBox = document.getElementById("chatBox");
const input = document.getElementById("chatInput");

// ==========================
// INIT
// ==========================
document.addEventListener("DOMContentLoaded", () => {
    input.focus();
});

// ==========================
// SEND MESSAGE
// ==========================
async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    // typing indicator
    const typing = addMessage("Thinking...", "ai");

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: text,
                emotion: currentEmotion
            })
        });

        const data = await res.json();

        typing.innerText = data.reply || "No response";

    } catch (err) {
        console.error(err);
        typing.innerText = "⚠️ Server error. Try again.";
    }

    scrollToBottom();
}

// ==========================
// ADD MESSAGE
// ==========================
function addMessage(text, type) {
    const div = document.createElement("div");
    div.className = `msg ${type}`;
    div.innerText = text;

    chatBox.appendChild(div);
    scrollToBottom();

    return div;
}

// ==========================
// AUTO SCROLL
// ==========================
function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

// ==========================
// ENTER KEY SEND
// ==========================
input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

// ==========================
// VOICE INPUT 🎤
// ==========================
let recognition;

function startMic() {
    try {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = "en-US";
        recognition.start();

        setMicState(true);

        recognition.onresult = (e) => {
            const text = e.results[0][0].transcript;
            input.value = text;
            sendMessage();
        };

        recognition.onend = () => {
            setMicState(false);
        };

    } catch (err) {
        alert("Speech recognition not supported in this browser.");
        console.error(err);
    }
}

// Mic UI feedback
function setMicState(active) {
    const micBtn = document.getElementById("micBtn");
    if (!micBtn) return;

    if (active) {
        micBtn.classList.add("mic-active");
    } else {
        micBtn.classList.remove("mic-active");
    }
}

// ==========================
// EMOJI PICKER 😊
// ==========================
let emojiVisible = false;

const picker = new EmojiMart.Picker({
    theme: "dark",
    onEmojiSelect: (emoji) => {
        input.value += emoji.native;
        input.focus();
    }
});

document.getElementById("emojiPicker").appendChild(picker);

function toggleEmoji() {
    const box = document.getElementById("emojiPicker");
    emojiVisible = !emojiVisible;
    box.style.display = emojiVisible ? "block" : "none";
}

// ==========================
// OPTIONAL: BOT GREETING
// ==========================
function initChat() {
    addMessage("Hello 👋 I'm your AI assistant. Ask me anything!", "ai");
}

// call on load
initChat();