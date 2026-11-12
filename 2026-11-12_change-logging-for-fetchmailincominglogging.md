---
commit_ref: b352b5bb5fb873ab3271c9c87a51706fcb39d25c
title: "change logging for fetchmail_incoming_logging"
author: "laurens kooijman <laurenskooijman@gmail.com>"
action: implement
state: completed
date_completed: 2026-11-12
harness: pi
provider: moonshotai
model: Kimi-K2.6
input_tokens: 39494
output_tokens: 9131
---

# change logging for fetchmail_incoming_logging

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` and `README.md` to get an understanding of the project
- Read entire task section and prepare a list of todos
- Update the todo list while working on task

## Task

I asked you to create the module `fetchmail_incoming_logging` which you can find in addons/server-tools. The related prompt you can find in `addons/server-tools/tmp/prompt-log/2026-11-12_new-module-fetchmailincominglogging.md`.

Please change the logging approach by creating entries into `ir.logging`, instead of logging as `_logger.info()` calls which is implemented now.

The module is defined here `odoo/odoo/addons/base/models/ir_logging.py`.

An example of an application is found here `odoo/addons/l10n_ro_edi/models/res_company.py`. Excerpt from this file:
```
    def _l10n_ro_edi_log_message(self, message: str, func: str):
        with self.pool.cursor() as cr:
            self = self.with_env(self.env(cr=cr))
            self.env['ir.logging'].sudo().create({
                'name': 'l10n_ro_edi_log',
                'type': 'server',
                'level': 'INFO',
                'dbname': self.env.cr.dbname,
                'message': message,
                'func': func,
                'path': '',
                'line': '1',
            })
            self.env.cr.commit()
```

Another example from `odoo/addons/base_automation/models/base_automation.py`:
```
    def _prepare_loggin_values(self, **values):
        self.ensure_one()
        defaults = {
            'name': _("Webhook Log"),
            'type': 'server',
            'dbname': self._cr.dbname,
            'level': 'INFO',
            'path': "base_automation(%s)" % self.id,
            'func': '',
            'line': ''
        }
        defaults.update(**values)
        return defaults

    def _execute_webhook(self, payload):
        """ Execute the webhook for the given payload.
        The payload is a dictionnary that can be used by the `record_getter` to
        identify the record on which the automation should be run.
        """
        self.ensure_one()
        ir_logging_sudo = self.env['ir.logging'].sudo()

        # info logging is done by the ir.http logger
        msg = "Webhook #%s triggered with payload %s"
        msg_args = (self.id, payload)
        _logger.debug(msg, *msg_args)
        if self.log_webhook_calls:
            ir_logging_sudo.create(self._prepare_loggin_values(message=msg % msg_args))
```


@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

- Added `_fetchmail_log_message` helper method to `mail.thread` in `addons/server_tools/fetchmail_incoming_logging/models/mail_thread.py`.
- Replaced all `_logger.info()` calls with `ir.logging` entry creation via the helper.
- The helper uses `self.pool.cursor()` and commits explicitly so logs persist even if the main transaction rolls back.
- Removed the unused `logging` import and `_logger` definition, cleaned up `__pycache__`.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness, provider and model. If you have access to session info also add token count.
