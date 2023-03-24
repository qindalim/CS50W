document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector("#details-view").style.display = "none";
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email(event) {
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      load_mailbox("sent", result);
    })

  // Prevent page from reloading after sending email
  event.preventDefault();
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector("#details-view").style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      emails.forEach((email) => {

        const row = document.createElement("div");
        const row_content = document.createElement("div");

        // Do not show archived mails in inbox, do not show normal mails in archive
        if ((mailbox === "inbox" && email["archived"]) || (mailbox === "archive" && !email["archived"])) {
          return false;
        }

        // Recipient or sender bolded
        const recipients_sender = document.createElement("strong");
        
        // If sentbox -> recipients, else -> sender
        if (mailbox === "sent") {
          recipients_sender.innerHTML = email["recipients"].join();
        }
        else {
          recipients_sender.innerHTML = email["sender"];
        }
        recipients_sender.innerHTML += " ";
        row_content.append(recipients_sender);
        
        // Add email subject beside recipient or sender
        row_content.innerHTML += email["subject"];
      
        // Datetime on the right
        const datetime = document.createElement("div");

        datetime.innerHTML = email["timestamp"];
        datetime.style.float = "right";
        datetime.style.display = "inline-block";
        row_content.append(datetime);

        // Add content to each row
        row.append(row_content);

        // Additional styling
        row_content.style.padding = "10px";
        row.style.border = "1px solid black";

        // Add event listener to read email
        row.addEventListener("click", () => view_email(email["id"]));

        // Read emails become light grey
        if (email["read"]) {
          row.style.backgroundColor = "lightgrey";
        } 

        // Add rows to emails view
        document.querySelector("#emails-view").append(row);
      });
    })
}

function view_email(email_id) {
  document.querySelector("#details-view").style.display = "block";
  document.querySelector("#emails-view").style.display = "none";

  // Reset email content
  document.querySelector("#details-view").innerHTML = "";

  // Get the email's info and build the section.
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(result => {
      // Create content
      const from = document.createElement("div");
      const to = document.createElement("div");
      const subject = document.createElement("div");
      const datetime = document.createElement("div");
      const body = document.createElement("div");

      from.innerHTML = `<strong>From: </strong> ${result["sender"]}`;
      to.innerHTML = `<strong>To: </strong> ${result["recipients"].join()}`;
      subject.innerHTML = `<strong>Subject: </strong> ${result["subject"]}`;
      datetime.innerHTML = `<strong>Timestamp: </strong> ${result["timestamp"]}`;
      body.innerHTML = result["body"];

      // Make reply button
      const reply = document.createElement("button");
      reply.innerHTML = "Reply";
      reply.classList = "btn btn-outline-primary";

      // Add event listener to reply button
      reply.addEventListener("click", () => reply_email(result));

      // Make archive button
      const archive = document.createElement("button");
      archive.classList = "btn btn-outline-primary";
      archive.style.margin = "10px";

      // If mail is archived, change button to unarchive
      if (result["archived"]) {
        archive.innerHTML += "Unarchive";
      } else {
        archive.innerHTML += "Archive";
      }

      // Add event listener to archive button
      archive.addEventListener("click", () => {
        archive_email(result);
        load_mailbox("inbox");
      });

      // Append items in order
      document.querySelector("#details-view").append(from);
      document.querySelector("#details-view").append(to);
      document.querySelector("#details-view").append(subject);
      document.querySelector("#details-view").append(datetime);
      document.querySelector("#details-view").append(reply);
      document.querySelector("#details-view").append(archive);

      // Draw line after archive and reply buttons
      document.querySelector("#details-view").append(document.createElement("hr"));

      document.querySelector("#details-view").append(body);
    })

  // Change read status
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });
}

function archive_email(email) {
  fetch(`/emails/${email["id"]}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: !email["archived"]
    })
  });
}

function reply_email(email) {
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#details-view").style.display = "none";

  // Prefill email
  document.querySelector("#compose-recipients").value = email["sender"];
  document.querySelector("#compose-subject").value = "Re: " + email["subject"];
  document.querySelector("#compose-body").value = `On ${email["timestamp"]} ${email["sender"]} wrote: \n${email["body"]}`;
}

