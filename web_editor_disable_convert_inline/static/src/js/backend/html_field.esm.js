/** @odoo-module **/
import {HtmlField} from "@web_editor/js/backend/html_field";
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";

const {onWillStart} = owl;

patch(HtmlField.prototype, "web_editor_class_selector.HtmlField", {
    async _toInline() {
        const $editable = this.wysiwyg.getEditable();
        this.wysiwyg.odooEditor.sanitize(this.wysiwyg.odooEditor.editable);
        const html = this.wysiwyg.getValue();
        const $odooEditor = $editable.closest(".odoo-editor-editable");
        // Save correct nodes references.
        // Remove temporarily the class so that css editing will not be converted.
        $odooEditor.removeClass("odoo-editor-editable");
        $editable.html(html);

        // Await toInline($editable, undefined, this.wysiwyg.$iframe);
        $odooEditor.addClass("odoo-editor-editable");

        this.wysiwyg.setValue($editable.html());
        this.wysiwyg.odooEditor.sanitize(this.wysiwyg.odooEditor.editable);
    },
});
