function fetchUserProfile(username) {
  return fetch(`/user-profile/${username}/json/`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      return data;
    })
    .catch((error) => {
      console.error(error);
      throw error;
    });
}

function toggleFollowAction(formData, action) {
  const url = action === "follow" ? "/follow/" : "/unfollow/";
  formData.append("csrfmiddlewaretoken", getCookie("csrftoken"));

  return fetch(url, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .catch((error) => {
      console.log(error);
      throw error;
    });
}

export { fetchUserProfile, toggleFollowAction };
