odoo.define('home_background_image.Home', function (require) {
"use strict";

    const session = require('web.session');
    const WebClient = require('web.WebClient');

    WebClient.include({

        //--------------------------------------------------------------------------
        // Public
        //--------------------------------------------------------------------------

        /**
         * @override
         */
        async load_menus() {
            const menuData = await this._super(...arguments);
            const company_id = session.user_context.allowed_company_ids[0];
            const url = session.url('/web/image', {
                id: company_id,
                model: 'res.company',
                field: 'background_image',
            });
            this.homeMenuStyle = `background-image: url(${url})`;
            return menuData;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @override
         * @private
         */
         _instanciateHomeMenuWrapper() {
            const homeMenuManager = this._super(...arguments);
            if (this.homeMenuStyle) {
                homeMenuManager.state.style = this.homeMenuStyle;
            }
            return homeMenuManager;
        },
    });
});
