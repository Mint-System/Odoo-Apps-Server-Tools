odoo.define('show_db_name.UserMenu', function (require) {
   "use strict";

   var UserMenu = require('web.UserMenu');

   UserMenu.include({
      start: function () {
         var self = this;
         var session = this.getSession();
         return this._super.apply(this, arguments).then(function () {
            var topbar_name = session.name;
            topbar_name = _.str.sprintf("%s (%s)", topbar_name, session.db);
            self.$('.oe_topbar_name').text(topbar_name);
         });
      },
   });
});
