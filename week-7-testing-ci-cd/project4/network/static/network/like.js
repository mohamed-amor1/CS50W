// Include the JavaScript code for like.js here
document.addEventListener("DOMContentLoaded", () => {
  const csrfToken = "{{ csrf_token }}";
  const likeButtons = document.querySelectorAll('[id^="like-button-"]');
  likeButtons.forEach((button) => {
    button.removeEventListener("click", handleLikeButtonClick);
    button.addEventListener("click", handleLikeButtonClick);
  });

  function handleLikeButtonClick() {
    const postId = this.dataset.postId;
    const liked = this.dataset.liked === "true";

    // Update the button text immediately
    this.textContent = liked ? "Like" : "Unlike";

    like(postId, !liked)
      .then((data) => {
        // Update the button state after the server response
        this.dataset.liked = data.liked.toString();

        // Update the like count
        const likeCountElement = document.querySelector(
          `[data-post-id="${postId}"]`
        );
        likeCountElement.textContent = data.likes_count;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  function like(postId, liked) {
    return new Promise((resolve, reject) => {
      fetch(`/like/${postId}`, {
        method: liked ? "DELETE" : "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          resolve(data);
        })
        .catch((error) => {
          console.error("Error:", error);
          reject(error);
        });
    });
  }
});
