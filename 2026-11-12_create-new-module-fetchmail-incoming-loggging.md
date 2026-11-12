---
commit_ref:
title: "Create new module Fetchmail Incoming Loggging"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: draft
date_completed: YYYY-MM-DD
harness:
provider:
model:
input_tokens:
output_tokens:
---

# Create new module Fetchmail Incoming Loggging

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` and `README.md` to get an understanding of the project
- Read entire task section and prepare a list of todos
- Update the todo list while working on task

## Task

Create a new module `addons/server_tools/fetchmail_incoming_logging`.

It logs the the `mail.thread` processing methods to `ir.logging`. I want to know which methods are triggered for a mail processing.

And if available I want to know if attachment data has been processed.

Inherit the `mail.thread` model and create a new `_log_message_state(self, log_message)` that prepares the values for `ir.logging`.

- `message_parse`
- `message_route`
- `message_post`
- `_process_attachments_for_post`
- `_create_attachments_for_post`
- `_fetchmail_log_message`

Here some pseudo code:

```python

	_log_message_state(self, log_message, message_id=None, attachment_ids=None){
		# If message id is set add to logging message
		if message_id:

		# If attachments is set, check length and add to logging message
		if  attachment_ids:

        self.env["ir.logging"].create({
            "name": name,
            "type": "server",
            "level": "INFO",
            "dbname": env.cr.dbname,
            "message": message,
            "func": func,
            "path": "",
            "line": "1",
        })
	}

    @api.model
    def message_route(self, message, message_dict, model, thread_id=None, custom_values=None):
        routes = super().message_route(
            message, message_dict, model, thread_id=thread_id, custom_values=custom_values
        )
        message_id = ...
        attachment_ids = ...
        self._log_message_state("Message routed", message_id, attachment_ids)

        return routes
```

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

@Clanker Add a summary here once the task has been completed.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness, provider and model. If you have access to session info also add token count. Finally, update the changelog with the most important changes.
