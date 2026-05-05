/** @odoo-module **/
import { Component, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class LiveDataComponent extends Component {
    static template = "test_bus.LiveDataTemplate";

    setup() {
        this.rpc = useService("rpc");
        this.busService = useService("bus_service");
    }

    // onWillStart() {
    //     // Subscribe to the channel
    //     this.busService.subscribe("your_channel", (message) => {
    //         console.log("Bus message received:", message);
    //     });
    //     this.busService.start();
    // }
    onWillStart(() => {
        this.busService.addChannel("my_channel");  // let bus service manage the channel
        this.busService.subscribe("notification", (message) => {
            console.log("Bus message received:", message);
            this.state.message = message;
        });
        this.busService.start();
    });

    async fetchLiveData() {
        const result = await this.rpc("/test_bus/live_data", {});
        console.log("RPC result:", result);
    }
}

registry.category("actions").add("live_data_action", LiveDataComponent);