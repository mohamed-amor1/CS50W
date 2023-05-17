// Check if the counter value is stored in localStorage, if not, initialize it to 0
if (!localStorage.getItem("counter")) {
  localStorage.setItem("counter", 0);
}

// Define a function named count() that increments the counter value and updates the <h1> element
function count() {
  // Get the current counter value from localStorage
  let counter = localStorage.getItem("counter");

  // Increment the counter by 1
  counter++;

  // Update the text content of the <h1> element with the current value of the counter
  document.querySelector("h1").innerHTML = counter;

  // Store the updated counter value back to localStorage
  localStorage.setItem("counter", counter);
}

// Wait for the DOMContentLoaded event before executing the following code
document.addEventListener("DOMContentLoaded", function () {
  // Set the initial counter value in the <h1> element from localStorage
  document.querySelector("h1").innerHTML = localStorage.getItem("counter");

  // Assign the count() function as the onclick event handler for the button
  document.querySelector("button").onclick = count;
});
