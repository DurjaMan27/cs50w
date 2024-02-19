document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email(1, 'compose'));

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(id, action) {

  if(action == 'compose') {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#single-email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-recipients').disabled = false;
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  } else {
    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      // Clear out composition fields
      document.querySelector('#compose-recipients').value = email['sender'];
      document.querySelector('#compose-recipients').disabled = true;
      document.querySelector('#compose-subject').value = `RE: ${email['subject']}`;
      document.querySelector('#compose-body').value = `On ${email['timestamp']}, ${email['sender']} wrote: ${email['body']}`;
    })

    if(action == 'reply') {
      // Show compose view and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#single-email-view').style.display = 'block';
      document.querySelector('#compose-view').style.display = 'block';
    } else if(action == 'replyAll') {
      console.log('not implemented yet');
    }
  }

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
    load_mailbox('sent');
  };
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#single-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      let div = document.createElement('div');
      div.className = 'email';

      if(email['read']) {
        div.style.backgroundColor = '#dadee6';
      } else {
        div.style.backgroundColor = 'white';
      }
      div.style.border = '1px solid black';

      div.innerHTML = `
        <h2>${email['sender']} - ${email['subject']}</h2>
        <p>${email['timestamp']}</p>
      `;
      document.querySelector('#emails-view').appendChild(div);
      div.addEventListener('click', () => load_email(email['id']));
    })
  });
}

function load_email(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      let div = document.createElement('div');
      div.className = 'full-email';

      div.style.border = '1px solid black';
      div.innerHTML = `
        <h2>${email['sender']}</h2>
        <h2>${email['subject']}</h2>
        <p>${email['body']}</p>
        <p>${email['timestamp']}</p>
      `;

      console.log(div);

      document.querySelector('#email-content').innerHTML = '';
      document.querySelector('#email-content').appendChild(div);

      document.querySelector('#reply').addEventListener('click', () => compose_email(id, 'reply'));
      document.querySelector('#replyAll').addEventListener('click', () => compose_email(id, 'replyAll'));

      if(email['archived']) {
        document.querySelector('#archive').style.display = 'none';
        document.querySelector('#unarchive').style.display = 'block';
        document.querySelector('#unarchive').addEventListener('click', () => unarchive_email(id));
      } else {
        document.querySelector('#archive').style.display = 'block';
        document.querySelector('#unarchive').style.display = 'none';
        document.querySelector('#archive').addEventListener('click', () => archive_email(id));
      }
  });
}

function archive_email(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    load_mailbox('inbox');
  })
}

function unarchive_email(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    load_mailbox('inbox');
  })
}