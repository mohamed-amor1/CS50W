document.addEventListener("DOMContentLoaded", function () {
  const allPostsContainer = document.querySelector("#all-posts");

  // Show the "All Posts" section by default
  allPostsContainer.style.display = "block";

  document
    .querySelector("#nav-all-posts")
    .addEventListener("click", (event) => {
      event.preventDefault(); // Prevent the default anchor tag behavior

      // Toggle the display property of the "all-posts" element
      if (allPostsContainer.style.display === "none") {
        allPostsContainer.style.display = "block";
      } else {
        allPostsContainer.style.display = "none";
      }
    });
});
