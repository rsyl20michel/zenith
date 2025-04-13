import {patch} from "@web/core/utils/patch";
import {markup} from "@odoo/owl";

import {GanttRenderer} from "@web_gantt/gantt_renderer";

patch(GanttRenderer.prototype, {

    convertToHtml(record) {
        return markup(record.replace('.75', '.60') || "");
    },

    /**
     * @param {"t0" | "t1" | "t2"} type
     * @returns {number}
     */
    getRowTypeHeight(type) {
        return {
            t0: 24,
            t1: 106,
            t2: 16,
        }[type];
    },

});
