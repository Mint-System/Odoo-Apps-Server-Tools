---
commit_ref: 0cd3593fec3ea6d1906b8bd7ce6bbc11ef717fae
title: "new module fetchmail_incoming_logging"
author: "laurens kooijman <laurenskooijman@gmail.com>"
action: implement
state: completed
date_completed: 2026-11-10
harness: pi
provider: infomaniak
model: moonshotai/Kimi-K2.6
input_tokens: 165441
output_tokens: 41886
---

# new module fetchmail_incoming_logging

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` and `README.md` to get an understanding of the project
- Read entire task section and prepare a list of todos
- Update the todo list while working on task

## Task

The goal of this task is to create a new module that adds additional logging to the mail receiving process. In particular I am interested in logging how the attachments are handled.

I have prepared that boilerplate for the module in `addons/server_tools/fetchmail_incoming_logging`. Only change/add files to this folder.

First analyse the flow of methods that are involved in receiving an email. Find this in Odoo-Build, start with the methods in the class `MailThread` (odoo/addons/mail/models/mail_thread.py), in particular `message_process()`.

Then analyse what happens to attachments and how they are stored in `ir.attachment` (odoo/addons/mail/models/ir_attachment.py & odoo/odoo/addons/base/models/ir_attachment.py). Return a short summary the flow of mail and attachment processing in the worklog of this promptfile (if possible, only the method names.)

I have particular places where I want feedback through logging. However, take a moment to consider where additional feedback would be interesting to track the flow of the attachment data. Write your suggestions in the worklog of this prompt and ask which ones I would like to additionally implement after this task is in review.

To get feedback in the proces, add `_logger.info()` steps before or after specific methods to report on:
- Properties after message parsing
- Properties after attachment parsing
- Properties before attachment storage
- Properties after attachment storage

Message properties to report:
- Message arrival
- Message route
- Content of the field `attachment_ids`

Attachemnt properties to report (if possible at that stage):
- Content of the attachment field `checksum`
- State of the attachment field `index_content` (report if False, otherwise the length of the field.)
- State of the attachment field `datas` (report if False, otherwise the length of the field.)

This is an example from another mail logging module, which adds loggin before the method `message_process`:
```
class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def message_process(
        self,
        model,
        message,
        custom_values=None,
        save_original=False,
        strip_attachments=False,
        thread_id=None,
    ):
        message_copy = message
        if isinstance(message, xmlrpclib.Binary):
            message = bytes(message.data)

        if isinstance(message, str):
            message = message.encode("utf-8")
        message = email.message_from_bytes(message, policy=email.policy.SMTP)
        msg_dict = self.message_parse(message, save_original=save_original)
        _logger.info(
            "Fetched mail from %s to %s with Message-Id %s",
            msg_dict.get("from"),
            msg_dict.get("to"),
            msg_dict.get("message_id"),
        )

        return super().message_process(
            model,
            message_copy,
            custom_values=custom_values,
            save_original=save_original,
            strip_attachments=strip_attachments,
            thread_id=thread_id,
        )
```

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

### Mail and Attachment Processing Flow

The following methods are involved in receiving and processing an incoming email and its attachments:

**Mail Thread Processing:**
1. `message_process()` — Entry point; decodes raw bytes, orchestrates parsing/routing/posting.
2. `message_parse()` — Parses headers, extracts body, bounce info, and attachments.
3. `_message_parse_extract_bounce()` — Detects bounce emails and extracts bounce metadata.
4. `_message_parse_extract_payload()` — Walks MIME parts; separates body (text/html) from attachments.
5. `_message_parse_extract_payload_postprocess()` — Cleans body, resolves inline CID references.
6. `message_route()` — Determines target model/thread/alias by matching headers.
7. `_routing_check_route()` — Validates alias permissions and model gateway support.
8. `_message_route_process()` — Routes the email; calls `message_new()` or `message_update()`, then posts the message.
9. `message_new()` / `message_update()` — Creates or updates the target record.
10. `message_post()` / `message_notify()` — Creates the `mail.message`.
11. `_message_create()` — Low-level `mail.message` creation.

**Attachment Storage:**
12. `_process_attachments_for_post()` — Converts raw attachment tuples into `ir.attachment` create values; base64-encodes `datas`.
13. `_create_attachments_for_post()` — Calls `ir.attachment.create()`.
14. `ir.attachment.create()` — Computes `checksum`, `index_content`, `file_size`; stores to filestore or DB.
15. `_get_datas_related_values()` — Computes derived fields (`checksum`, `index_content`, `store_fname`, etc.).
16. `_compute_checksum()` / `_index()` / `_file_write()` — Helpers for checksum, full-text indexing, and filestore persistence.
17. `_post_add_create()` — Post-creation hook; registers attachment as main attachment if applicable.

### Implemented Logging

The module overrides the following methods to add `_logger.info()` calls:

- `message_parse()` — Logs message arrival properties (from, to, message_id, subject, attachment count/names) and attachment parsing state (content length; checksum/index_content/datas are N/A at this stage).
- `message_route()` — Logs the resolved route (model, thread_id, alias name).
- `message_post()` — After posting, logs the created `mail.message.attachment_ids`.
- `_process_attachments_for_post()` — Before creating attachments, logs each attachment name, raw content length, and computed `datas` length; checksum and index_content are N/A at this stage.
- `_create_attachments_for_post()` — After attachment creation, logs each attachment id, `checksum`, `index_content` length (or False), and `datas` length (or False).

### Suggestions for Additional Logging

The following additional logging points could provide deeper visibility into the attachment/data flow. Please confirm which ones you would like to implement after review:

1. **Attachment mimetype detection** — Log the detected/guessed `mimetype` for each attachment before storage (in `_process_attachments_for_post`).
2. **Filestore path logging** — After `ir.attachment.create()`, log whether the attachment was stored in DB (`db_datas`) or filestore (`store_fname`).
3. **Inline/CID attachment linking** — Log when an inline attachment (referenced by `cid:` in the HTML body) is matched and linked to the body (in `_process_attachments_for_post` or `_message_parse_extract_payload_postprocess`).
4. **Main attachment registration** — Log when `_post_add_create()` registers an attachment as the record’s main attachment.
5. **Attachment deduplication** — If `create_unique()` is used anywhere in your flow, log whether an attachment was created or reused based on its checksum.
6. **Message update path** — In `_message_route_process`, log whether `message_new()` or `message_update()` was invoked, including the resulting record ID.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness, provider and model. If you have access to session info also add token count.
