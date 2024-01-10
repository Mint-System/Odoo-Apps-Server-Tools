import logging

from odoo import _, api, models

_logger = logging.getLogger(__name__)

from odoo.addons.base_vat.models.res_partner import _ref_vat


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _run_vat_test(self, vat_number, default_country, partner_is_company=True):
        res = super()._run_vat_test(
            vat_number, default_country, partner_is_company=True
        )

        # Return false if vat check failed for eu country.
        is_eu_country = self.country_id in self.env.ref("base.europe").country_ids
        vies_check = self._run_vies_test(self.vat, self.country_id)
        if is_eu_country and vies_check is False:
            return False
        elif isinstance(vies_check, str) and vies_check.upper() != self.country_id.code:
            return False
        else:
            return res

    @api.model
    def _build_vat_error_message(self, country_code, wrong_vat, record_label):
        return "\n" + _(
            "The VAT number [%(wrong_vat)s] for [%(country_code)s] did not pass the VAT/VIES check."
            "\nNote: the expected format is %(expected_format)s",
            wrong_vat=wrong_vat,
            record_label=record_label,
            country_code=country_code.upper(),
            expected_format=_ref_vat.get(
                country_code, "'CC##' (CC=Country Code, ##=VAT Number)"
            ),
        )
