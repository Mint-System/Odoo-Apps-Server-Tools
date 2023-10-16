from odoo import api, fields, models, tools


class BoardUsers(models.Model):
    _name = "board.users"
    _description = "Board Users"
    _auto = False

    user_id = fields.Many2one("res.users", string="User", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            create or replace view board_users as (
                select
                    min(i.id) as id,
                    i.user_id as user_id
                from
                    ir_ui_view_custom as i
                group by
                	i.user_id
            )
        """
        )


class Board(models.AbstractModel):
    _inherit = "board.board"

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        user_dashboard = self.env.context.get("user_dashboard")
        if user_dashboard:
            self = self.with_env(self.env(user=user_dashboard))
        res = super(Board, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        return res
