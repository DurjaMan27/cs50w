document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector("compose-recipients").value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
  };

  load_mailbox('inbox');
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(email => {
      const sender = document.createElement('h1');
      sender.innerHTML = email.sender;
      sender.setAttribute('class', 'email-sender');

      const subject = document.createElement('h2');
      subject.innerHTML = email.subject;
      subject.setAttribute('class', 'email-subject');

      const timestamp = document.createElement('p');
      timestamp.innerHTML = email.timestamp;
      timestamp.setAttribute('class', 'email-timestamp');

      const div = document.createElement('div');
      div.appendChild(sender)
      div.appendChild(subject);
      div.appendChild(timestamp);

      const url = document.createElement('a').innerHTML = div;
      url.setAttribute('href', '');
      const li = document.createElement('li').innerHTML = url;
      document.querySelector('#emails').append(li);
    });
  })
}