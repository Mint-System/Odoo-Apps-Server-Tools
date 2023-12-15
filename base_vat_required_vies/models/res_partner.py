import logging

from odoo import _, api, models

_logger = logging.getLogger(__name__)

from odoo.addons.base_vat.models.res_partner import _ref_vat


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _run_vat_test(self, vat_number, default_country, partner_is_company=True):
        super()._run_vat_test(vat_number, default_country, partner_is_company=True)
        return self.vies_passed

    @api.model
    def _build_vat_error_message(self, country_code, wrong_vat, record_label):
        return "\n" + _(
            "The VAT number [%(wrong_vat)s] for [%(country_code)s] did not pass the VIES check."
            "\nNote: the expected format is %(expected_format)s",
            wrong_vat=wrong_vat,
            record_label=record_label,
            country_code=country_code.upper(),
            expected_format=_ref_vat.get(
                country_code, "'CC##' (CC=Country Code, ##=VAT Number)"
            ),
        )
