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

  // Delegate the event handling to the parent element
  allPostsContainer.addEventListener("click", (event) => {
    if (event.target.closest(".user-profile-link")) {
      event.preventDefault();
      const username =
        event.target.closest(".user-profile-link").dataset.username;
      fetchUserProfile(username)
        .then((userProfileData) => {
          const followersCount = userProfileData.followers;
          const followingCount = userProfileData.following;

          // Update the user profile section dynamically
          const profileDetailsContainer =
            document.querySelector("#profile-details");
          profileDetailsContainer.innerHTML = `
            <h2>User Profile</h2>
            <h3>Username: ${userProfileData.username}</h3>
            <p>Email: ${userProfileData.email}</p>
            <p class="follower-count">Followers: <span id="follower-count">${followersCount}</span></p>
            <p class="following-count">Following: <span id="following-count">${followingCount}</span></p>
            <div class="follow-container"></div>
            <h3 style="margin-top:40px">Posts by ${userProfileData.username}</h3>
            <div id="user-posts" class="posts-container"></div>
          `;

          const userPostsContainer = document.querySelector("#user-posts");
          const posts = userProfileData.posts;

          // Loop through the user's posts and append them to the user-posts container
          for (let i = 0; i < posts.length; i++) {
            const post = posts[i];
            const postElement = document.createElement("div");
            postElement.classList.add("row", "post-row");
            postElement.innerHTML = `
              <div class="col" style="border: 1px solid #e5e7eb; margin: 5px; margin-bottom: 20px; border-radius: 0.4em; padding: 10px;">
                <a href="#" class="user-profile-link" data-username="${post.author}">
                  <h4>${post.author}</h4>
                </a>
                <div>${post.text}</div>
                <div style="color: gray">${post.timestamp}</div>
                <div class="likes-container">
                  <img src="/static/network/red-heart-icon.svg" alt="Heart Icon" width="20" height="20" />
                  <div class="likes-count" style="color: gray">${post.likes}</div>
                </div>
              </div>
            `;
            userPostsContainer.appendChild(postElement);
          }

          allPostsContainer.style.display = "none";
          userProfileContainer.style.display = "block";

          // Conditionally render the "Follow" button
          if (
            userProfileData.is_authenticated &&
            userProfileData.username !== userProfileData.current_username
          ) {
            const followForm = document.createElement("form");
            followForm.id = "follow-form";
            followForm.method = "post";
            followForm.innerHTML = `
  <input type="hidden" name="username" value="${userProfileData.username}">
  <button id="follow-button" type="submit" class="btn btn-outline-primary">Follow</button>
`;

            const followContainer = document.querySelector(".follow-container");
            followContainer.innerHTML = "";
            followContainer.appendChild(followForm);
          }
        })
        .catch((error) => {
          console.log(error);
          // Handle any errors that occur during the AJAX request
        });
    }
  });

  // Delegate the event handling to the parent element
  document
    .querySelector("#profile-details")
    .addEventListener("submit", (event) => {
      if (event.target.id === "follow-form") {
        event.preventDefault();
        const formData = new FormData(event.target);

        // Disable the follow button to prevent multiple clicks
        const followButton = event.target.querySelector("#follow-button");
        followButton.disabled = true;

        // Send an AJAX request to the server to follow the user
        fetch("follow/", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"), // Include the CSRF token
          },
          body: formData,
        })
          .then((response) => response.json())
          .then((data) => {
            // Handle the response from the server
            if (data.success) {
              // Update the follower and following counts
              const followerCountElement =
                document.querySelector("#follower-count");
              const followingCountElement =
                document.querySelector("#following-count");

              if (data.action === "follow") {
                followerCountElement.textContent =
                  parseInt(followerCountElement.textContent) + 1;
              } else if (data.action === "unfollow") {
                followerCountElement.textContent =
                  parseInt(followerCountElement.textContent) - 1;
              }

              // Update the UI or perform any other necessary actions
              console.log(data.message);
            } else {
              console.log(data.error);
            }
          })
          .catch((error) => {
            console.log(error);
            // Handle any errors that occur during the AJAX request
          })
          .finally(() => {
            // Enable the follow button after the request is complete
            followButton.disabled = false;
          });
      }
    });
});

function fetchUserProfile(username) {
  return fetch(`/user-profile/${username}/json/`)
    .then((response) => response.json())
    .catch((error) => {
      console.log(error);
      // Handle any errors that occur during the AJAX request
    });
}

function getCookie(name) {
  const cookieValue = document.cookie.match(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
  return cookieValue ? cookieValue.pop() : "";
}
