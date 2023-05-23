document.addEventListener("DOMContentLoaded", function () {
  const allPostsContainer = document.querySelector("#all-posts");
  const userProfileContainer = document.querySelector("#user-profile-view");

  // Show the "All Posts" section by default
  allPostsContainer.style.display = "block";

  document
    .querySelector("#nav-all-posts")
    .addEventListener("click", (event) => {
      event.preventDefault();
      allPostsContainer.style.display = "block";
      userProfileContainer.style.display = "none";
    });

  // Add other network-related functionality here
});
