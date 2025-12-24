const API_URL = "YOUR_API_GATEWAY_URL/chat";

async function send() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: input.value })
  });

  const data = await response.json();
  chat.textContent += `\nYou: ${input.value}\nAI: ${data.reply}\n`;
  input.value = "";
}
