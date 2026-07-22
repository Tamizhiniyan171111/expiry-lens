// static/js/charts.js
// Draws our dashboard charts using Chart.js (loaded via CDN in base.html)
// The actual DATA is injected into the page by Flask/Jinja2 via 
// hidden data attributes on the canvas elements - see dashboard.html

document.addEventListener("DOMContentLoaded", () => {
    // ===================================
    // CHART 1: Saved vs Wasted (Doughnut Chart)
    // ===================================
    const savedWastedCanvas = document.getElementById("saved-wasted-chart");

    if (savedWastedCanvas) {
        // Read the numbers Flask embedded as data-* attributes
        const savedCount = parseInt(savedWastedCanvas.getAttribute("data-saved"));
        const wastedCount = parseInt(savedWastedCanvas.getAttribute("data-wasted"));

        new Chart(savedWastedCanvas, {
            type: "doughnut",
            data: {
                labels: ["Saved", "Wasted"],
                datasets: [{
                    data: [savedCount, wastedCount],
                    backgroundColor: ["#2e7d32", "#c62828"],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: "bottom" }
                }
            }
        });
    }

    // ===================================
    // CHART 2: Items by Status (Bar Chart)
    // ===================================
    const statusChartCanvas = document.getElementById("status-breakdown-chart");

    if (statusChartCanvas) {
        const freshCount = parseInt(statusChartCanvas.getAttribute("data-fresh"));
        const warningCount = parseInt(statusChartCanvas.getAttribute("data-warning"));
        const urgentCount = parseInt(statusChartCanvas.getAttribute("data-urgent"));
        const expiredCount = parseInt(statusChartCanvas.getAttribute("data-expired"));

        new Chart(statusChartCanvas, {
            type: "bar",
            data: {
                labels: ["Fresh", "Expiring Soon", "Urgent", "Expired"],
                datasets: [{
                    label: "Number of Items",
                    data: [freshCount, warningCount, urgentCount, expiredCount],
                    backgroundColor: ["#66bb6a", "#f9a825", "#e65100", "#c62828"],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                }
            }
        });
    }
});