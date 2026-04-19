async function sendText() {
    let input = document.getElementById("userInput").value;
    let chatBox = document.getElementById("chatBox");

    if (input === "") return;

    // User message
    let userMsg = document.createElement("div");
    userMsg.className = "message user";
    userMsg.innerText = input;
    chatBox.appendChild(userMsg);

    document.getElementById("userInput").value = "";

    // Bot typing...
    let botMsg = document.createElement("div");
    botMsg.className = "message bot";
    botMsg.innerText = "Thinking...";
    chatBox.appendChild(botMsg);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        let response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: input })
        });

        let data = await response.json();

        botMsg.innerText = data.result;

    } catch (error) {
        botMsg.innerText = "Error connecting to AI 😢";
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}