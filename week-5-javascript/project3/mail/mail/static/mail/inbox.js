document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document.querySelector("#inbox").addEventListener("click", () => {
    load_mailbox("inbox");
    inbox_email();
  });

  document.querySelector("#sent").addEventListener("click", () => {
    load_mailbox("sent");
    fetch("/emails/sent")
      .then((response) => response.json())
      .then((emails) => {
        console.log(emails);
        emails.forEach((email) => {
          renderEmail(email);
        });
      });
  });

  document.querySelector("#archived").addEventListener("click", () => {
    load_mailbox("archive");

    archive_email(); // Fetch and render the archived emails
  });
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");
  inbox_email();

  document.querySelector("#compose-form").onsubmit = () => {
    send_mail();
    load_mailbox("sent");
    return false;
  };
});

function renderEmail(email) {
  const { id, sender, subject, timestamp, read } = email;

  const row = document.createElement("div");
  row.classList.add("row");
  row.style.margin = "0";
  row.style.textAlign = "left";
  row.style.fontSize = "16px";
  row.style.padding = "0";
  row.style.alignItems = "center";
  row.innerHTML = `
    <div class="col-sm-2 col-md-2 col-12" style="border-left: 1px solid black; border-top: 1px solid black; border-bottom: 1px solid black; text-align: left; padding-left: 6px; padding-bottom: 5px; padding-top: 5px;"><strong>${sender}</strong></div>
    <div class="col-sm-7 col-md-7 col-12" style="border-top: 1px solid black; border-bottom: 1px solid black; padding-bottom: 5px; padding-top: 5px;">
      <a href="javascript:void(0)" onclick="read_email(${id})">${subject}</a>
    </div>
    <div class="col-sm col-md col-12" style="color: grey; border-right: 1px solid black; border-top: 1px solid black; border-bottom: 1px solid black; text-align: right; padding-right: 5px; padding-bottom: 5px; padding-top: 5px;">${timestamp}</div>
  `;

  if (read) {
    row.style.backgroundColor = "#f5f5f5";
  } else {
    row.style.backgroundColor = "white";
  }

  // Append the email element to the emails view container
  document.querySelector("#emails-view").appendChild(row);

  row.querySelector(".col-sm-7").addEventListener("click", () => {
    read_email(id);
  });
}

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;
}

function send_mail() {
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: document.querySelector("#compose-recipients").value,
      subject: document.querySelector("#compose-subject").value,
      body: document.querySelector("#compose-body").value,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      console.log(result);

      // Fetch and display sent emails
      load_mailbox("sent");
      fetch("/emails/sent")
        .then((response) => response.json())
        .then((emails) => {
          emails.forEach((email) => {
            renderEmail(email);
          });
        });
    });
}

function inbox_email() {
  fetch("/emails/inbox")
    .then((response) => response.json())
    .then((emails) => {
      emails.forEach((email) => {
        renderEmail(email);
      });
    });
}

function archive_email() {
  fetch("/emails/archive")
    .then((response) => response.json())
    .then((emails) => {
      emails.forEach((email) => {
        renderEmail(email);
      });
    })
    .catch((error) => {
      // Handle any errors that occurred during the fetch request
      console.log("Error fetching archived emails:", error);
    });
}

function read_email(email_id) {
  // Show the email view and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  // Show the email view and hide other views
  document.querySelector("#emails-view").innerHTML = "";

  fetch(`/emails/${email_id}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((email) => {
      console.log(email);

      const details = document.createElement("div");
      const formattedEmailText = email.body.replace(/\n/g, "<br>");
      if (email.archived === true) {
        details.innerHTML = `
        <div><strong>From:</strong> ${email.sender}</div>
        <div><strong>To:</strong> ${email.recipients}</div>
        <div><strong>Subject:</strong> ${email.subject}</div>
        <div><strong>Timestamp:</strong> ${email.timestamp}</div>
        <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>

        <hr />

        <div>${formattedEmailText}</div>
        <hr />

        <button  class="btn btn-sm btn-outline-primary float-right" id="unarchive">Unarchive</button>
      `;
      } else {
        details.innerHTML = `
        <div><strong>From:</strong> ${email.sender}</div>
        <div><strong>To:</strong> ${email.recipients}</div>
        <div><strong>Subject:</strong> ${email.subject}</div>
        <div><strong>Timestamp:</strong> ${email.timestamp}</div>
        <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>

        <hr />

        <div>${formattedEmailText}</div>
        <hr />

        <button  class="btn btn-sm btn-outline-primary float-right" id="archive">Archive</button>
      `;
      }

      document.querySelector("#emails-view").innerHTML = "";

      document.querySelector("#emails-view").append(details);

      // Attach event listener to the reply button
      document.querySelector("#reply").addEventListener("click", () => {
        // Handle reply functionality here
        document.querySelector("#emails-view").style.display = "none";
        document.querySelector("#compose-view").style.display = "block";

        // Clear out composition fields
        document.querySelector("#compose-recipients").value = email.sender;
        document.querySelector("#compose-subject").value =
          email.subject.startsWith("Re")
            ? email.subject
            : "Re: " + email.subject;
        document.querySelector(
          "#compose-body"
        ).value = `On ${email.timestamp} ${email.sender} wrote: \n${email.body}\n\n`;
      });

   if (email.archived === true) {
     // Attach event listener to the unarchive button
     document.querySelector("#unarchive").addEventListener("click", () => {
       // Handle unarchive functionality here
       fetch(`/emails/${email_id}`, {
         method: "PUT",
         body: JSON.stringify({
           archived: false,
         }),
       }).then(() => {
         load_mailbox("inbox");
         inbox_email();
       });
     });
   } else {
     // Attach event listener to the archive button
     document.querySelector("#archive").addEventListener("click", () => {
       // Handle archive functionality here
       fetch(`/emails/${email_id}`, {
         method: "PUT",
         body: JSON.stringify({
           archived: true,
         }),
       }).then(() => {
         load_mailbox("inbox");
         inbox_email();
       });
     });
   }

      // Mark the email as read
      return fetch(`/emails/${email_id}`, {
        method: "PUT",
        body: JSON.stringify({
          read: true,
        }),
      });
    })
    .then((response) => response.json())
    .then((result) => {
      console.log(result);
    });
}
