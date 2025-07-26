let ws = new WebSocket("ws://" + window.location.host + "/ws");
let chart;
let normalCount = 0;
let anomalyCount = 0;
let totalCount = 0;
let sessionCount = 0;

// Initialize chart
function initChart(initialNormal, initialAnomaly) {
    normalCount = initialNormal || 0;
    anomalyCount = initialAnomaly || 0;
    totalCount = normalCount + anomalyCount;

    let ctx = document.getElementById('logChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Normal', 'Anomaly'],
            datasets: [{
                data: [normalCount, anomalyCount],
                backgroundColor: ['green', 'red']
            }]
        },
        options: { responsive: true }
    });

    updateStatsAndChart();
}

// Update stats text and chart
function updateStatsAndChart() {
    animateCount('normalCount', normalCount);
    animateCount('anomalyCount', anomalyCount);
    animateCount('totalLogs', totalCount);
    animateCount('sessionCount', sessionCount);

    if (chart) {
        chart.data.datasets[0].data = [normalCount, anomalyCount];
        chart.update();
    }

    document.getElementById("lastUpdated").textContent = new Date().toLocaleString();
}

// Animate a number smoothly
function animateCount(id, newCount) {
    let el = document.getElementById(id);
    let current = parseInt(el.textContent) || 0;
    let diff = newCount - current;
    let step = diff / 20;
    let i = 0;
    let interval = setInterval(() => {
        i++;
        el.textContent = Math.round(current + step * i);
        if (i >= 20) {
            el.textContent = newCount;
            clearInterval(interval);
        }
    }, 20);
}

// WebSocket handling
ws.onopen = () => {
    sessionCount++;
    updateStatsAndChart();
};

ws.onclose = () => {
    sessionCount = Math.max(0, sessionCount - 1);
    updateStatsAndChart();
};

ws.onmessage = function(event) {
    let msg = JSON.parse(event.data);
    if (msg.type === "session_update") {
        sessionCount = msg.count;
    } else if (msg.type === "log") {
        addLogRow(msg.data);
    } else if (msg.type === "alert") {
        addAlertRow(msg.data);
    }
    updateStatsAndChart();
};

function addLogRow(data) {

    let table = document.getElementById("logsTable");
    let row = table.insertRow(-1);  // append at bottom
    row.className = 'fade-in';

    let timestamp = data.timestamp || '-';
    let label = (data.label || '').toLowerCase();
    let log = data.log || '-';

    row.innerHTML = `<td>${timestamp}</td><td>${label}</td><td>${log}</td>`;

    if (label === 'anomaly') {
        row.classList.add('log-anomaly');
        anomalyCount++;
    } else if (label === 'normal') {
        row.classList.add('log-normal');
        normalCount++;
    } else {
        row.style.color = 'gray';
    }

    totalCount++;
    updateStatsAndChart();
    autoScroll('logsContainer');
}

// Add alert row
function addAlertRow(data) {
    let container = document.getElementById("alertsContainer");
    let div = document.createElement('div');
    div.className = 'alert-critical fade-in';
    div.innerHTML = `${data.advice}<br><small>Ref Log: ${data.log}</small>`;
    // container.prepend(div);
    container.appendChild(div);
    autoScroll('alertsContainer');
}

// Auto-scroll
function autoScroll(containerId) {
    let container = document.getElementById(containerId);
    container.scrollTop = container.scrollHeight;
}

// Toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}

// Filter logs
function filterLogs(type) {
    let rows = document.querySelectorAll("#logsTable tr");
    rows.forEach(row => {
        if (type === 'all' || row.cells[1].textContent === type) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Periodic timestamp update
setInterval(() => {
    document.getElementById("lastUpdated").textContent = new Date().toLocaleString();
}, 60000);
