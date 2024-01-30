document.getElementById("correct").addEventListener("click", function () {
  sendData("correct").then((r) => console.log(r));
});
document.getElementById("rewrite").addEventListener("click", function () {
  sendData("rewrite").then((r) => console.log(r));
});
document.getElementById("clear").addEventListener("click", function () {
  document.querySelector("#text_input").innerHTML = " ";
});
async function sendData(actions) {
  // let inputElement = document.querySelector("#text_input");
  let inputElement = document.querySelector("#text_input").innerHTML;
  await new Promise((resolve) => setTimeout(resolve, 1000));
  try {
    const response = await fetch("/sub", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ textinput: inputElement, action: actions }),
      timeout: 10000,
    });
    if (response.ok) {
      const jsonResponse = await response.json();
      document.querySelector("#text_input").innerHTML = jsonResponse.textoutput
    } else {
      console.error("Server response was not OK.");
    }
  } catch (error) {
    console.error("Failed to send or receive data:", error);
  }
}
