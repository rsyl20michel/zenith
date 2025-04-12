import {patch} from "@web/core/utils/patch";
import {markup} from "@odoo/owl";

import {GanttRenderer} from "@web_gantt/gantt_renderer";

patch(GanttRenderer.prototype, {

    convertToHtml(record) {
        return markup(record || "");
    },

    computeRowsTemplate() {
        const rowsTemplate = [];
        const rowInCoarseGridKeys = this.getRowInCoarseGridKeys();
        for (let i = 0; i < rowInCoarseGridKeys.length - 1; i++) {
            const x = +rowInCoarseGridKeys[i];
            const y = +rowInCoarseGridKeys[i + 1];
            const rowName = `r${x}`;
            const height = x == 1 ? this.gridRows.slice(x - 1, y - 1).reduce((a, b) => a + b, 0) : 'auto';
            rowsTemplate.push(`[${rowName}]${height}${x == 1 ? 'px' : ''}`);
        }
        rowsTemplate.push(`[r${rowInCoarseGridKeys.at(-1)}]`);
        return rowsTemplate.join("");
    }

});
