let counter = 0;

// Define a function named count()
function count() {
  // Increment the counter by 1
  counter++;

  // Update the text content of the <h1> element with the current value of counter
  document.querySelector("h1").innerHTML = counter;

  // Check if the counter is a multiple of 10
  if (counter % 10 === 0) {
    // If it is, display an alert with a message showing the current counter value
    alert(`Count is now ${counter}`);
  }
}

// Wait for the DOMContentLoaded event before assigning the onclick event handler
document.addEventListener("DOMContentLoaded", function () {
  // Assign the count() function as the onclick event handler for the button
  document.querySelector("button").onclick = count;

});
