function sendMessage() {

   let userName = "";
let askingName = true;  // true until user gives name

    let input = document.getElementById("userInput").value;
    let messages = document.getElementById("messages");

    if (!input) return;

    // Display user's message
   messages.innerHTML += "<p class='message user'>" + input + "</p>";

    // Send to Flask
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

        // If bot just asked for name, mark it as provided
        if (askingName) {
            userName = input;
            askingName = false;
        }
  });

}
