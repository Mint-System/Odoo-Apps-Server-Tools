# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import logging

from email.message import EmailMessage

from odoo import api, models

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def message_parse(self, message, save_original=False):
        msg_dict = super().message_parse(message, save_original=save_original)

        attachments = msg_dict.get("attachments", [])
        _logger.info(
            "Message parsed - from: %s, to: %s, message_id: %s, subject: %s, "
            "attachment_count: %s, attachment_names: %s",
            msg_dict.get("from"),
            msg_dict.get("to"),
            msg_dict.get("message_id"),
            msg_dict.get("subject"),
            len(attachments),
            [att[0] for att in attachments if att],
        )

        for idx, att in enumerate(attachments):
            content = att[1] if len(att) > 1 else None
            content_len = len(content) if content else False
            _logger.info(
                "Attachment parsed [%s/%s] - name: %s, content_length: %s, "
                "checksum: N/A, index_content: N/A, datas: N/A",
                idx + 1,
                len(attachments),
                att[0],
                content_len,
            )

        return msg_dict

    @api.model
    def message_route(self, message, message_dict, model, thread_id=None, custom_values=None):
        routes = super().message_route(
            message, message_dict, model, thread_id=thread_id, custom_values=custom_values
        )

        for route in routes or []:
            alias_name = route[4].display_name if route[4] else "None"
            _logger.info(
                "Message routed - model: %s, thread_id: %s, alias: %s",
                route[0],
                route[1],
                alias_name,
            )

        return routes

    def message_post(self, **kwargs):
        result = super().message_post(**kwargs)

        if self.env.context.get("from_alias") and result:
            _logger.info(
                "Message posted - message_id: %s, attachment_ids: %s",
                result.message_id,
                result.attachment_ids.ids,
            )

        return result

    def _process_attachments_for_post(self, attachments, attachment_ids, message_values):
        if self.env.context.get("from_alias") and attachments:
            for idx, attachment in enumerate(attachments):
                if len(attachment) == 2:
                    name, content = attachment
                    info = {}
                elif len(attachment) == 3:
                    name, content, info = attachment
                else:
                    continue

                if isinstance(content, str):
                    encoding = info.get("encoding") if info else None
                    try:
                        content = content.encode(encoding or "utf-8")
                    except UnicodeEncodeError:
                        content = content.encode("utf-8")
                elif isinstance(content, EmailMessage):
                    content = content.as_bytes()

                content_len = len(content) if content else False
                datas_len = len(base64.b64encode(content)) if content else False
                _logger.info(
                    "Attachment before storage [%s/%s] - name: %s, "
                    "content_length: %s, checksum: N/A, index_content: N/A, "
                    "datas_length: %s",
                    idx + 1,
                    len(attachments),
                    name,
                    content_len,
                    datas_len,
                )

        return super()._process_attachments_for_post(
            attachments, attachment_ids, message_values
        )

    def _create_attachments_for_post(self, values_list, extra_list):
        attachments = super()._create_attachments_for_post(values_list, extra_list)

        if self.env.context.get("from_alias"):
            for idx, attachment in enumerate(attachments):
                datas_val = attachment.datas
                index_val = attachment.index_content
                _logger.info(
                    "Attachment after storage [%s/%s] - name: %s, id: %s, "
                    "checksum: %s, index_content: %s, datas_length: %s",
                    idx + 1,
                    len(attachments),
                    attachment.name,
                    attachment.id,
                    attachment.checksum,
                    len(index_val) if index_val else False,
                    len(datas_val) if datas_val else False,
                )

        return attachments
