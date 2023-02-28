from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    @api.depends('company_id')
    def _compute_active_user_count(self):
        res = super()._compute_active_user_count()
        active_user_count = self.env['res.users'].sudo().search_count([('share', '=', False),('service_user', '=', False)])
        for record in self:
            record.active_user_count = active_user_count
        return res