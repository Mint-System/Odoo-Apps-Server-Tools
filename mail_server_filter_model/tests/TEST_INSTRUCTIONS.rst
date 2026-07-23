Init:

- Start mailpit
- Init contacts app

Configure model:

- Go to Settings > Technical > Outgoing Mail Servers
- Create entry for mailpit with host localhost:1025
- Add res.partner to allowed models

Send message:

- Open any contact and send a message
- Ensure it shows up in mailpit

Disallow send message:

- Remove res.partner from allowed models
- Send a message on the same contact
- Ensure the mail is not send
- Open Settings > Technical > Emails, open the mail and check the error message
