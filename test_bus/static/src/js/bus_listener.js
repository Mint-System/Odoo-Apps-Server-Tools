/** @odoo-module **/

import {Component, useState, xml} from "@odoo/owl";

export class TestBusComponent extends Component {
    static template = xml`
        <div class="o_realtime_bus_widget">
          <span class="fa fa-bell"/> <!-- Notification icon -->
          <t t-if="state.data.length">
            <span class="o_badge"><t t-out="state.data.length"/></span>
          </t>
        </div>
    `;

    setup() {
        this.state = useState({data: []});
        this.busService = this.env.services.bus_service;
        // Add the channel to listen to.
        this.busService.addChannel("realtime-bus-test");
        // Listen to the event name after the channel is added.
        this.busService.subscribe("realtime-bus-test/sending-message", (payload) => {
            console.log("Bus message received:", payload);
        });
    }
}
