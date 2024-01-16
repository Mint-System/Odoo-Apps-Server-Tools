import datetime
import logging

from odoo import api, models
from odoo.tools import misc

_logger = logging.getLogger(__name__)


class PublisherWarrantyContract(models.AbstractModel):
    _inherit = "publisher_warranty.contract"

    @api.model
    def _get_message(self):
        Users = self.env["res.users"]
        msg = super(PublisherWarrantyContract, self)._get_message()
        limit_date = datetime.datetime.now()
        limit_date = limit_date - datetime.timedelta(15)
        limit_date_str = limit_date.strftime(misc.DEFAULT_SERVER_DATETIME_FORMAT)
        msg["nbr_users"] = Users.search_count(
            [("active", "=", True), ("service_user", "=", False)]
        )
        msg["nbr_active_users"] = Users.search_count(
            [
                ("login_date", ">=", limit_date_str),
                ("active", "=", True),
                ("service_user", "=", False),
            ]
        )
        # _logger.warning([msg['nbr_users'],msg['nbr_active_users']])
        return msg
