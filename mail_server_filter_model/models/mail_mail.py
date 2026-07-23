# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


class MailMail(models.Model):
    _inherit = "mail.mail"

    def _send(
        self,
        auto_commit=False,
        raise_exception=False,
        smtp_session=None,
        alias_domain_id=False,
        mail_server=False,
        post_send_callback=None,
    ):
        if mail_server:
            allowed_models = mail_server.model_ids.mapped("model")
            blocked = self.filtered(lambda m: not m.model or m.model not in allowed_models)
            if blocked:
                blocked.write(
                    {
                        "state": "exception",
                        "failure_type": "mail_smtp",
                        "failure_reason": _(
                            "Outgoing mail server '%(server)s' is not allowed to send emails for model '%(model)s'.",
                            server=mail_server.name,
                            model=blocked[:1].model or _("(none)"),
                        ),
                    }
                )
                blocked._postprocess_sent_message(success_pids=[], success_emails=[], failure_type="mail_smtp")
                self = self - blocked
                if not self:
                    return True
        return super()._send(
            auto_commit=auto_commit,
            raise_exception=raise_exception,
            smtp_session=smtp_session,
            alias_domain_id=alias_domain_id,
            mail_server=mail_server,
            post_send_callback=post_send_callback,
        )
