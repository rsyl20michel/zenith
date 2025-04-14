/** @odoo-module **/

import {AttendeeCalendarModel} from "@calendar/views/attendee_calendar/attendee_calendar_model";
import {patch} from "@web/core/utils/patch";

patch(AttendeeCalendarModel.prototype, {
    /**
     * Split the events to display an event for each attendee with the correct status.
     * If the all filter is activated, we don't display an event for each attendee and keep
     * the previous behavior to display a single event.
     */
    async updateAttendeeData(data) {
        await super.updateAttendeeData(...arguments);

        for (const event of Object.values(data.records)) {
            if (event.rawRecord.opportunity_id) {
                let leads = await this.orm.searchRead("crm.lead",
                    [["id", "=", event.rawRecord.opportunity_id[0]]],
                    ["city", "street", "street2", "zip"]);

                event.city = leads && leads.length ? leads[0].city : '';
                event.colorIndex = event.rawRecord.type_of_opportunity_color ? event.rawRecord.type_of_opportunity_color : event.attendeeId;
            }
        }
    }
});
