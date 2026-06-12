/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class TestBusListener extends Component {

    static template = "test_bus.Counter";
    setup() {
        console.log('Test Bus Listener initializing ...');
        // Get the bus service
        this.busService = this.env.services.bus_service;
        this.busService.addChannel("test_bus_channel");
        // Subscribe
        this.busService.subscribe("test_notification", this.onBusEvent.bind(this));
        
        console.log('Test Bus Listener initialized - waiting for notifications...');
    }
    
    onBusEvent(event) {
        const data = event.data;
        console.log("bus event called");
        
        if (data.type === 'test_notification') {
            console.log('Bus Notification Received!');
            console.log('Counter:', data.counter);
            console.log('Message:', data.message);
            console.log('Full event data:', data);
        }
    }
}

registry.category("public_components").add('test_bus.test_bus_listener', TestBusListener);
