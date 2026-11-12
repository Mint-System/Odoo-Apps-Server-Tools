# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from email.message import EmailMessage

from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def message_parse(self, message, save_original=False):
        msg_dict = super().message_parse(message, save_original=save_original)

        attachments = msg_dict.get("attachments", [])
        message_id = msg_dict.get("message_id")
        self._fetchmail_log_message(
            "Message parsed - message_id: {}, from: {}, to: {}, subject: {}, "
            "attachment_count: {}, attachment_names: {}".format(
                message_id,
                msg_dict.get("from"),
                msg_dict.get("to"),
                msg_dict.get("subject"),
                len(attachments),
                [att[0] for att in attachments if att],
            ),
            func="message_parse",
            message_id=message_id,
        )

        for idx, att in enumerate(attachments):
            content = att[1] if len(att) > 1 else None
            content_len = len(content) if content else False
            self._fetchmail_log_message(
                "Attachment parsed [{}/{}] - message_id: {}, name: {}, "
                "content_length: {}, checksum: N/A, index_content: N/A, "
                "datas: N/A".format(
                    idx + 1,
                    len(attachments),
                    message_id,
                    att[0],
                    content_len,
                ),
                func="message_parse",
                message_id=message_id,
            )

        return msg_dict

    @api.model
    def message_route(self, message, message_dict, model, thread_id=None, custom_values=None):
        routes = super().message_route(
            message, message_dict, model, thread_id=thread_id, custom_values=custom_values
        )

        message_id = message_dict.get("message_id")
        for route in routes or []:
            alias_name = route[4].display_name if route[4] else "None"
            self._fetchmail_log_message(
                "Message routed - message_id: {}, model: {}, thread_id: {}, "
                "alias: {}".format(
                    message_id,
                    route[0],
                    route[1],
                    alias_name,
                ),
                func="message_route",
                message_id=message_id,
            )

        return routes

    def message_post(self, **kwargs):
        result = super().message_post(**kwargs)

        if self.env.context.get("from_alias") and result:
            self._fetchmail_log_message(
                "Message posted - message_id: {}, attachment_ids: {}".format(
                    result.message_id,
                    result.attachment_ids.ids,
                ),
                func="message_post",
                message_id=result.message_id,
                db_id=result.id,
            )

        return result

    def _process_attachments_for_post(self, attachments, attachment_ids, message_values):
        message_id = message_values.get("message_id") if message_values else False
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
                self._fetchmail_log_message(
                    "Attachment before storage [{}/{}] - message_id: {}, "
                    "name: {}, content_length: {}, checksum: N/A, "
                    "index_content: N/A, datas_length: {}".format(
                        idx + 1,
                        len(attachments),
                        message_id,
                        name,
                        content_len,
                        datas_len,
                    ),
                    func="_process_attachments_for_post",
                    message_id=message_id,
                )

        if message_id:
            self = self.with_context(fetchmail_message_id=message_id)
        return super()._process_attachments_for_post(
            attachments, attachment_ids, message_values
        )

    def _create_attachments_for_post(self, values_list, extra_list):
        attachments = super()._create_attachments_for_post(values_list, extra_list)

        if self.env.context.get("from_alias"):
            message_id = self.env.context.get("fetchmail_message_id")
            for idx, attachment in enumerate(attachments):
                datas_val = attachment.datas
                index_val = attachment.index_content
                self._fetchmail_log_message(
                    "Attachment after storage [{}/{}] - message_id: {}, "
                    "name: {}, id: {}, checksum: {}, index_content: {}, "
                    "datas_length: {}".format(
                        idx + 1,
                        len(attachments),
                        message_id,
                        attachment.name,
                        attachment.id,
                        attachment.checksum,
                        len(index_val) if index_val else False,
                        len(datas_val) if datas_val else False,
                    ),
                    func="_create_attachments_for_post",
                    message_id=message_id,
                )

        return attachments

    def _fetchmail_log_message(self, message, func="", message_id=None, db_id=None):
        """Write a persistent ir.logging entry in a separate transaction."""
        name = "fetchmail_incoming_logging"
        if message_id:
            name = f"{name}_{message_id[:6]}"
        if db_id:
            message = f"db_id: {db_id}, {message}"
        with self.pool.cursor() as cr:
            env = self.env(cr=cr)
            env["ir.logging"].sudo().create({
                "name": name,
                "type": "server",
                "level": "INFO",
                "dbname": env.cr.dbname,
                "message": message,
                "func": func,
                "path": "",
                "line": "1",
            })
            env.cr.commit()
