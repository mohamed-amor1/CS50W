$(document).ready(function () {
  var followBadge = $("#follow-badge");
  var followUrl = followBadge.data("follow-url");
  var unfollowUrl = followBadge.data("unfollow-url");

  // Retrieve the following state from local storage or default to false
  var isFollowing = localStorage.getItem("isFollowing") === "true" || false;

  // Hide the follow badge initially
  followBadge.addClass("hidden");

  // Update the badge text and appearance based on the initial following state
  updateBadge(isFollowing);

  // Retrieve the followers count from local storage or default to 0
  var currentCount = parseInt(localStorage.getItem("followersCount")) || 0;
  updateFollowersCount(currentCount);

  followBadge.on("click", function (e) {
    e.preventDefault();

    var url = isFollowing ? unfollowUrl : followUrl;
    var method = isFollowing ? "DELETE" : "POST";
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
      url: url,
      method: method,
      headers: { "X-CSRFToken": csrfToken },
      success: function (response) {
        // Toggle the following state
        isFollowing = !isFollowing;

        // Update the badge text and appearance
        updateBadge(isFollowing);

        // Update the followers count
        currentCount += isFollowing ? 1 : -1;
        updateFollowersCount(currentCount);

        // Store the following state and count in local storage
        localStorage.setItem("isFollowing", isFollowing.toString());
        localStorage.setItem("followersCount", currentCount.toString());
      },
      error: function (xhr, status, error) {
        console.log("Error:", error);
      },
    });
  });

  function updateBadge(isFollowing) {
    followBadge.removeClass("hidden");
    followBadge.removeClass("badge-primary badge-secondary");
    followBadge.addClass(isFollowing ? "badge-secondary" : "badge-primary");
    followBadge.text(isFollowing ? "Unfollow" : "Follow");
  }

  function updateFollowersCount(count) {
    var followersCount = $("#followers-count");
    followersCount.text(count);
  }
});
