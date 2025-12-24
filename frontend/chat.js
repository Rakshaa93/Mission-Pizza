let userName = null;
let userLocation = null;
let cart = [];  

async function sendMessage() {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user-msg");
  input.value = "";


  if (!userName) {
    userName = text;
    addMessage(`Nice to meet you, ${userName}!  Where are you located?`, "bot-msg");
    return;
  }


  if (!userLocation) {
    userLocation = text;
    addMessage(
      `Great! You can now order pizza.\nType pizza names to add them.\nType "menu" to see options.\nType "checkout" to place order.`,
      "bot-msg"
    );
    return;
  }

  const lowerText = text.toLowerCase();

  if (lowerText.includes("menu")) {
    const botMsg = addMessage("Fetching menu...", "bot-msg");
    const res = await fetch("/menu");
    const menu = await res.json();

    let menuText = "Available Pizzas:\n\n";
    for (const pizza in menu) {
      menuText += `${pizza} (${menu[pizza].join(", ")})\n`;
    }
    botMsg.innerText = menuText;
    return;
  }

  if (lowerText.includes("checkout") || lowerText.includes("place order")) {
    if (cart.length === 0) {
      addMessage("Your cart is empty. Add pizzas first!", "bot-msg");
      return;
    }

    const botMsg = addMessage("Placing your order...", "bot-msg");

    try {
      const response = await fetch("/order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: cart.join(", "),
          name: userName,
          location: userLocation
        })
      });

      const data = await response.json();
      botMsg.innerText = data.message;

      cart = []; t
    } catch (err) {
      botMsg.innerText = "Something went wrong during checkout.";
    }
    return;
  }


let quantity = 1;
let itemText = text;

const qtyMatch = text.match(/(.*?)(\s*[x*]\s*\d+)$/i);
if (qtyMatch) {
  itemText = qtyMatch[1].trim();
  quantity = parseInt(qtyMatch[2].replace(/[^0-9]/g, ""));
}

for (let i = 0; i < quantity; i++) {
  cart.push(itemText);
}

addMessage(
  `Added "${itemText}" (${quantity} item${quantity > 1 ? "s" : ""}) to your order.\nCurrent items: ${cart.length}`,
  "bot-msg"
);

}

function addMessage(text, className) {
  const chatBox = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.className = className;
  msg.innerText = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
  return msg;
}
