document.addEventListener("DOMContentLoaded", function () {
    const calendarEl = document.getElementById("calendar");
    if (calendarEl && typeof FullCalendar !== "undefined") {
        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: "dayGridMonth",
            height: 650,
        });
        calendar.render();
    }
});