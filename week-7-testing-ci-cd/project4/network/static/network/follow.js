$(document).ready(function () {
  var followBadge = $("#follow-badge");
  var followUrl = followBadge.data("follow-url");
  var unfollowUrl = followBadge.data("unfollow-url");
  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  var followersCount = $("#followers-count");

  // Hide the follow badge initially
  followBadge.addClass("hidden");

  // Check if the initial state is "Following" based on the badge text
  var isFollowing = followBadge.text() === "Unfollow";

  updateBadge(isFollowing);

  followBadge.on("click", function (e) {
    e.preventDefault();

    var url = isFollowing ? unfollowUrl : followUrl;
    var method = isFollowing ? "DELETE" : "POST";

    $.ajax({
      url: url,
      method: method,
      headers: {
        "X-CSRFToken": csrfToken,
      },
      success: function (response) {
        // Toggle the following state
        isFollowing = !isFollowing;

        // Update the badge text and appearance
        updateBadge(isFollowing);

        // Update the followers count dynamically
        followersCount.text(response.followers_count);
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
});
