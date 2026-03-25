/** @odoo-module **/
import {patch} from "@web/core/utils/patch";
import {SubscriptionManager} from "@web_enterprise/enterprise_subscription/enterprise_subscription_service";

patch(SubscriptionManager.prototype, "mail_service_users.SubscriptionManager", {
    async buy() {
        const limitDate = serializeDate(DateTime.utc().minus({days: 15}));
        const args = [
            [
                ["share", "=", false],
                ["service_user", "=", false],
                ["login_date", ">=", limitDate],
            ],
        ];
        const nbUsers = await this.orm.call("res.users", "search_count", args);
        browser.location = `https://www.odoo.com/odoo-enterprise/upgrade?num_users=${nbUsers}`;
    },

    async upsell() {
        const limitDate = serializeDate(DateTime.utc().minus({days: 15}));
        const [enterpriseCode, nbUsers] = await Promise.all([
            this.orm.call("ir.config_parameter", "get_param", [
                "database.enterprise_code",
            ]),
            this.orm.call("res.users", "search_count", [
                [
                    ["share", "=", false],
                    ["service_user", "=", false],
                    ["login_date", ">=", limitDate],
                ],
            ]),
        ]);
        const url = "https://www.odoo.com/odoo-enterprise/upsell";
        const contractQueryString = enterpriseCode ? `&contract=${enterpriseCode}` : "";
        browser.location = `${url}?num_users=${nbUsers}${contractQueryString}`;
    },
});
