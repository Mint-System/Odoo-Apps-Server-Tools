# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _fetchmail_log_message(self, log_message, message_id=None, attachment_ids=None, func=""):
        """Create an ir.logging record for a mail processing step.

        :param str log_message: base logging message
        :param str message_id: optional email Message-Id
        :param attachment_ids: optional attachments or attachment ids
        :param str func: calling function name
        """
        if message_id:
            log_message += f" | message_id: {message_id}"
        if attachment_ids:
            log_message += f" | attachments: {len(attachment_ids)}"
        
        name = f"fetchmail_{message_id}" if message_id else "fetchmail"

        self.env["ir.logging"].sudo().create({
            "name": name,
            "type": "server",
            "level": "INFO",
            "dbname": self.env.cr.dbname,
            "message": log_message,
            "func": func,
            "path": "",
            "line": "1",
        })

    @api.model
    def message_parse(self, message, save_original=False):
        msg_dict = super().message_parse(message, save_original=save_original)
        self._fetchmail_log_message(
            "message_parse",
            message_id=msg_dict.get("message_id"),
            attachment_ids=msg_dict.get("attachments"),
            func="message_parse",
        )
        return msg_dict

    @api.model
    def message_route(self, message, message_dict, model=None, thread_id=None, custom_values=None):
        routes = super().message_route(
            message, message_dict, model, thread_id=thread_id, custom_values=custom_values
        )
        self._fetchmail_log_message(
            "message_route",
            message_id=message_dict.get("message_id"),
            attachment_ids=message_dict.get("attachments"),
            func="message_route",
        )
        return routes

    @api.returns("mail.message", lambda value: value.id)
    def message_post(self, **kwargs):
        new_message = super().message_post(**kwargs)
        self._fetchmail_log_message(
            "message_post",
            message_id=new_message.message_id,
            attachment_ids=new_message.attachment_ids,
            func="message_post",
        )
        return new_message

    def _process_attachments_for_post(self, attachments, attachment_ids, message_values):
        result = super()._process_attachments_for_post(attachments, attachment_ids, message_values)
        self._fetchmail_log_message(
            "_process_attachments_for_post",
            message_id=message_values.get("message_id"),
            attachment_ids=result.get("attachment_ids"),
            func="_process_attachments_for_post",
        )
        return result

    def _create_attachments_for_post(self, values_list, extra_list):
        attachments = super()._create_attachments_for_post(values_list, extra_list)
        self._fetchmail_log_message(
            "_create_attachments_for_post",
            attachment_ids=attachments,
            func="_create_attachments_for_post",
        )
        return attachments
