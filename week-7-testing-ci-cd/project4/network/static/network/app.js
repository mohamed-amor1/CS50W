import { fetchUserProfile, toggleFollowAction } from "./api.js";
import { getCookie } from "./utils.js";

document.addEventListener("DOMContentLoaded", function () {
  const allPostsContainer = document.querySelector("#all-posts");
  const userProfileContainer = document.querySelector("#user-profile-view");
  let userProfileData = null;
  const csrfToken = getCookie("csrftoken");

  allPostsContainer.style.display = "block";

  document
    .querySelector("#nav-all-posts")
    .addEventListener("click", (event) => {
      event.preventDefault();
      allPostsContainer.style.display = "block";
      userProfileContainer.style.display = "none";
    });

  function showUserProfile(username) {
    fetchUserProfile(username)
      .then((data) => {
        userProfileData = data;
        const followersCount = userProfileData.followers;
        const followingCount = userProfileData.following;

        const profileDetailsContainer =
          document.querySelector("#profile-details");
        profileDetailsContainer.innerHTML = `
        <h2>User Profile</h2>
        <h3>Username: ${userProfileData.username}</h3>
        <p>Email: ${userProfileData.email}</p>
        <p class="follower-count">Followers: <span id="follower-count">${followersCount}</span></p>
        <p class="following-count">Following: <span id="following-count">${followingCount}</span></p>
        <div class="follow-container"></div>
        <h3 style="margin-top:40px">Posts:</h3>
      `;

        const followContainer =
          profileDetailsContainer.querySelector(".follow-container");
        const followButton = document.createElement("button");
        followButton.textContent = "Follow";
        followButton.classList.add("follow-button");

        followContainer.innerHTML = "";
        followContainer.appendChild(followButton);

        followButton.addEventListener("click", () => {
          const formData = new FormData();
          formData.append("user_id", userProfileData.id);
          toggleFollowAction(formData, "follow")
            .then((response) => {
              if (response.success) {
                followButton.textContent = "Following";
                followersCount++;
                document.querySelector("#follower-count").textContent =
                  followersCount;
              }
            })
            .catch((error) => console.error(error));
        });
      })
      .catch((error) => console.error(error));
  }

  document
    .querySelector("#nav-user-profile")
    .addEventListener("click", (event) => {
      event.preventDefault();
      allPostsContainer.style.display = "none";
      userProfileContainer.style.display = "block";
      const username = event.target.textContent;
      showUserProfile(username);
    });
});
