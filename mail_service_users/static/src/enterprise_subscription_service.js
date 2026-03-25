/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { SubscriptionManager } from "@web_enterprise/webclient/home_menu/enterprise_subscription_service";
import { serializeDate } from "@web/core/l10n/dates";
import { browser } from "@web/core/browser/browser";

const { DateTime } = luxon;

patch(SubscriptionManager.prototype, {
    async buy() {
        const limitDate = serializeDate(DateTime.utc().minus({ days: 15 }));
        const nbUsers = await this.orm.call("res.users", "search_count", [
            [
                ["share", "=", false],
                ["service_user", "=", false],
                ["login_date", ">=", limitDate],
            ],
        ]);
        console.log("[mail_service_users] buy() nbUsers:", nbUsers);
        browser.location = `https://www.odoo.com/odoo-enterprise/upgrade?num_users=${nbUsers}`;
    },

    async upsell() {
        const limitDate = serializeDate(DateTime.utc().minus({ days: 15 }));
        const [enterpriseCode, nbUsers] = await Promise.all([
            this.orm.call("ir.config_parameter", "get_param", ["database.enterprise_code"]),
            this.orm.call("res.users", "search_count", [
                [
                    ["share", "=", false],
                    ["service_user", "=", false],
                    ["login_date", ">=", limitDate],
                ],
            ]),
        ]);
        console.log("[mail_service_users] upsell() nbUsers:", nbUsers);
        const url = "https://www.odoo.com/odoo-enterprise/upsell";
        const contractQueryString = enterpriseCode ? `&contract=${enterpriseCode}` : "";
        browser.location = `${url}?num_users=${nbUsers}${contractQueryString}`;
    },
});