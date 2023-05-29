// edit.js
document.addEventListener("DOMContentLoaded", () => {
  const editButtons = document.querySelectorAll(".edit-button");

  editButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const postId = button.dataset.postId;
      const postContent = document.getElementById(`post-content-${postId}`);
      const editForm = document.getElementById(`edit-form-${postId}`);
      const postEditContent = document.getElementById(
        `post-edit-content-${postId}`
      );
      const saveButton = document.getElementById(`save-button-${postId}`);

      // Hide the post content and show the edit form
      postContent.style.display = "none";
      editForm.style.display = "block";

      // Populate the edit form with the current post content
      postEditContent.value = postContent.textContent;

      // Add event listener to the save button
      saveButton.addEventListener("click", () => {
        // Retrieve the edited content from the textarea
        const editedContent = postEditContent.value;

        // Update the post content with the edited content
        postContent.textContent = editedContent;

        // Hide the edit form and show the post content again
        editForm.style.display = "none";
        postContent.style.display = "block";

        // Send the updated content to the server using AJAX or fetch
        const csrfToken = document
          .querySelector('meta[name="csrf-token"]')
          .getAttribute("content");

        fetch(`/edit-post/${postId}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ content: editedContent }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error(`Request failed with status ${response.status}`);
            }
            // Handle the response if needed
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      });
    });
  });

  // Load the updated post content on page load
  const postContents = document.querySelectorAll(".post-content");

  postContents.forEach((postContent) => {
    const postId = postContent.dataset.postId;

    fetch(`/get-post/${postId}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        postContent.textContent = data.content;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
});
