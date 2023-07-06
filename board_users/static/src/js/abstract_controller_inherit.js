odoo.define('web.AbstractControllerBoardUser', function (require) {
    'use strict'

    var AbstractController = require('web.AbstractController')

    AbstractController.include({

        _onOpenRecord: function (event) {
            event.stopPropagation()

            var record = this.model.get(event.data.id, { raw: true })
            var self = this
            var res_id = record.res_id
            var model = this.modelName

            if (model == 'board.users') {
                self._rpc({
                    model: 'ir.ui.view',
                    method: 'get_view_id',
                    args: ['board.board_my_dash_view'],
                }).then(function (data) {
                    self.do_action({
                        name: 'Dashboard',
                        type: 'ir.actions.act_window',
                        res_model: 'board.board',
                        views: [[data, 'form']],
                        usage: 'menu',
                        context: { 'user_dashboard': record.data.user_id },
                        view_type: 'form',
                        view_mode: 'form',
                    })
                })
            } else {
                self.trigger_up('switch_view', {
                    view_type: 'form',
                    res_id: res_id,
                    mode: event.data.mode || 'readonly',
                    model: model
                })
            }
        },
    })
})
