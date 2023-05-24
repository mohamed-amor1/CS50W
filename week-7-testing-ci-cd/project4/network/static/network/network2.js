// haka yemchiw ama moch dynamique
document.addEventListener("DOMContentLoaded", function () {
  const allPostsContainer = document.querySelector("#all-posts");
  const userProfileContainer = document.querySelector("#user-profile-view");
  let userProfileData = null; // Declare the userProfileData variable
  const csrfToken = getCookie("csrftoken");

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
        .then((data) => {
          userProfileData = data; // Assign fetched data to userProfileData
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
                  <h4>${post.author}</h4>
              
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

          // Conditionally render the "Follow" or "Unfollow" button
          if (
            userProfileData.is_authenticated &&
            userProfileData.username !== userProfileData.current_username
          ) {
            const followForm = document.createElement("form");
            followForm.id = "unfollow-form"; // Update the ID to "unfollow-form"
            followForm.method = "post";

            if (userProfileData.is_following) {
              // Check if the user is already following
              followForm.innerHTML = `
      <input type="hidden" name="username" value="${userProfileData.username}">
      <button id="unfollow-button" type="submit" class="btn btn-outline-danger">Unfollow</button>
    `;
            } else {
              followForm.id = "follow-form"; // Update the ID to "follow-form"

              followForm.innerHTML = `
      <input type="hidden" name="username" value="${userProfileData.username}">
      <button id="follow-button" type="submit" class="btn btn-outline-primary">Follow</button>
    `;
            }

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

  document
    .querySelector("#profile-details")
    .addEventListener("submit", (event) => {
      event.preventDefault();

      if (event.target.matches("#follow-form")) {
        const formData = new FormData(event.target);
        toggleFollowAction(formData, "follow")
          .then((response) => {
            if (response.success) {
              // Update the UI based on the successful action
              const followButton = document.querySelector("#follow-button");
              const unfollowButton = document.querySelector("#unfollow-button");
              if (followButton) {
                followButton.style.display = "none";
              }
              if (unfollowButton) {
                unfollowButton.style.display = "block";
              }
              // Update the follower count
              const followerCount = parseInt(
                document.querySelector("#follower-count").textContent
              );
              document.querySelector("#follower-count").textContent =
                followerCount + 1;
            } else {
              console.log(response.error);
              // Handle any error messages or actions
            }
          })
          .catch((error) => {
            console.log(error);
            // Handle any errors that occur during the AJAX request
          });
      } else if (event.target.matches("#unfollow-form")) {
        const formData = new FormData(event.target);
        toggleFollowAction(formData, "unfollow")
          .then((response) => {
            if (response.success) {
              // Update the UI based on the successful action
              const followButton = document.querySelector("#follow-button");
              const unfollowButton = document.querySelector("#unfollow-button");
              if (followButton) {
                followButton.style.display = "block";
              }
              if (unfollowButton) {
                unfollowButton.style.display = "none";
              }
              // Update the follower count
              const followerCount = parseInt(
                document.querySelector("#follower-count").textContent
              );
              document.querySelector("#follower-count").textContent = Math.max(
                followerCount - 1,
                0
              );
            } else {
              console.log(response.error);
              // Handle any error messages or actions
            }
          })
          .catch((error) => {
            console.log(error);
            // Handle any errors that occur during the AJAX request
          });
      }
    });

  // ...

  function toggleFollowAction(formData, action) {
    const url = action === "follow" ? "/follow/" : "/unfollow/";

    // Append the CSRF token to the form data
    formData.append("csrfmiddlewaretoken", csrfToken);

    // Create a new XMLHttpRequest object
    const xhr = new XMLHttpRequest();

    // Open the AJAX request
    xhr.open("POST", url, true);

    // Define the callback function when the request is complete
    xhr.onload = function () {
      if (xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        // Handle the response data
        if (response.success) {
          // Update the UI based on the successful action
          if (action === "follow") {
            // Hide the follow button and show the unfollow button
            const followButton = document.querySelector("#follow-button");
            followButton.style.display = "none";
            const unfollowButton = document.querySelector("#unfollow-button");
            unfollowButton.style.display = "block";

            // Update the follower count
            const followerCount = parseInt(
              document.querySelector("#follower-count").textContent
            );
            document.querySelector("#follower-count").textContent =
              followerCount + 1;
          } else if (action === "unfollow") {
            // Hide the unfollow button and show the follow button
            const unfollowButton = document.querySelector("#unfollow-button");
            unfollowButton.style.display = "none";
            const followButton = document.querySelector("#follow-button");
            followButton.style.display = "block";

            // Update the follower count
            const followerCount = parseInt(
              document.querySelector("#follower-count").textContent
            );
            document.querySelector("#follower-count").textContent = Math.max(
              followerCount - 1,
              0
            );
          }
        } else {
          console.log(response.error);
          // Handle any error messages or actions
        }
      } else {
        console.log("Request failed. Status: " + xhr.status);
        // Handle any error messages or actions
      }
    };

    // Send the AJAX request
    xhr.send(formData);

    // Return a promise for asynchronous handling
    return new Promise((resolve, reject) => {
      xhr.onload = function () {
        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          resolve(response);
        } else {
          reject(Error(xhr.statusText));
        }
      };
      xhr.onerror = function () {
        reject(Error("Network Error"));
      };
    });
  }

  function getCookie(name) {
    const cookieValue = document.cookie.match(
      "(^|;)\\s*" + name + "\\s*=\\s*([^;]+)"
    );
    return cookieValue ? cookieValue.pop() : "";
  }

  function fetchUserProfile(username) {
    return fetch(`/user-profile/${username}/json/`)
      .then((response) => response.json())
      .then((data) => {
        // Process the user profile data
        console.log(data);
        return data;
      })
      .catch((error) => {
        console.error(error);
        throw error;
      });
  }
});
