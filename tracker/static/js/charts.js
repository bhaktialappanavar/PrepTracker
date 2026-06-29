// PREPTRACKER CHARTS


// Topics Doughnut Chart

const topicCanvas = document.getElementById("topicChart");
if (topicCanvas) {
    const completed = Number(topicCanvas.dataset.completed);
    const remaining = Number(topicCanvas.dataset.remaining);
    new Chart(topicCanvas, {
        type: "doughnut",
        data: {
            labels: ["Completed", "Remaining"],
            datasets: [{
                data: [completed, remaining],
                backgroundColor: [
                    "#71826C",
                    "#e5e7eb"
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });
}


// Study Hours Chart

const studyCanvas = document.getElementById("studyChart");
if (studyCanvas) {
    const studyHours = JSON.parse(studyCanvas.dataset.hours);
    const studyDates = JSON.parse(studyCanvas.dataset.dates);
    new Chart(studyCanvas, {
        type: "bar",
        data: {
            labels: studyDates,
            datasets: [{
                label: "Study Hours",
                data: studyHours,
                backgroundColor: "#E3B227",
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}