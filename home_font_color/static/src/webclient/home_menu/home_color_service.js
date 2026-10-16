import { registry } from "@web/core/registry";

registry.category("services").add("home_font_color", {
    dependencies: ["orm"],
    start(env, { orm }) {
        orm.call("res.company", "get_home_font_color", []).then((color) => {
            if (color) {
                document.documentElement.style.setProperty(
                    "--o-home-menu-caption-color", color
                );
            }
        });
    },
});