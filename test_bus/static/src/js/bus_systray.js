/** @odoo-module **/

import {registry} from "@web/core/registry";
import {TestBusComponent} from "./bus_listener";

registry.category("systray").add("test_bus_component", {
    Component: TestBusComponent,
});
