import {patch} from "@web/core/utils/patch";
import {CalendarCommonRenderer} from "@web/views/calendar/calendar_common/calendar_common_renderer";
import {renderToString} from "@web/core/utils/render";

patch(CalendarCommonRenderer.prototype, {

    onEventContent({event}) {
        const record = this.props.model.records[event.id];
        if (record) {
            // This is needed in order to give the possibility to change the event template.
            const injectedContentStr = renderToString(this.constructor.eventTemplate, {
                ...record,
                startTime: this.getStartTime(record),
                endTime: this.getEndTime(record),
                city: record.city ? record.city : '',
            });
            const domParser = new DOMParser();
            const {children} = domParser.parseFromString(injectedContentStr, "text/html").body;
            return {domNodes: children};
        }
        return true;
    }

});
