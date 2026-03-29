document.addEventListener("DOMContentLoaded", function() {
    let askingName = true;
    let userName = "";

    function sendMessage() {
        let input = document.getElementById("userInput").value.trim();
        let messages = document.getElementById("messages");
        if (!input) return;

        // Display user's message
        messages.innerHTML += "<p class='message user'>" + input + "</p>";

        // Send to backend
        fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ message: input })
        })
        .then(response => response.json())
        .then(data => {
            messages.innerHTML += "<p class='message bot'>" + data.reply + "</p>";
            document.getElementById("userInput").value = "";
            messages.scrollTop = messages.scrollHeight;

            if (askingName) {
                userName = input;
                askingName = false;
            }
        })
        .catch(err => {
            console.error(err);
            messages.innerHTML += "<p class='message bot'>😅 Something went wrong!</p>";
        });
    }

    document.getElementById("chatForm").addEventListener("submit", function(e) {
        e.preventDefault();
        sendMessage();
    });
});
