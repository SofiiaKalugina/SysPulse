const API_URL = "http://127.0.0.1:8000";

async function fetchJson(endpoint) {
    const response = await fetch(`${API_URL}${endpoint}`);

    if (!response.ok) {
        throw new Error(`Request failed: ${endpoint}`);
    }

    return response.json();
}

function renderMachines(machines) {
    const container = document.getElementById("machines");

    if (machines.length === 0) {
        container.innerHTML = "<p>No machines found.</p>";
        return;
    }

    container.innerHTML = machines.map(machine => `
        <div class="item">
            <strong>${machine.hostname}</strong>
            <p>Status: <span class="status-${machine.status}">${machine.status}</span></p>
            <p class="small">OS: ${machine.os_name} ${machine.os_version}</p>
            <p class="small">Last seen: ${machine.last_seen_at}</p>
        </div>
    `).join("");
}

function renderLatestMetric(metricData) {
    const container = document.getElementById("latest-metrics");

    if (metricData.status === "empty") {
        container.innerHTML = "<p>No metrics received yet.</p>";
        return;
    }

    const metric = metricData;

    container.innerHTML = `
        <div class="item">
            <strong>${metric.hostname}</strong>
            <p>CPU: ${metric.cpu_percent}%</p>
            <p>RAM: ${metric.ram_percent}%</p>
            <p>Disk: ${metric.disk_percent}%</p>
            <p>Processes: ${metric.process_count}</p>
            <p class="small">Timestamp: ${metric.timestamp}</p>
        </div>
    `;
}

function renderAlerts(alerts) {
    const container = document.getElementById("alerts");

    if (alerts.length === 0) {
        container.innerHTML = "<p>No alerts.</p>";
        return;
    }

    container.innerHTML = alerts.map(alert => `
        <div class="item">
            <p class="alert">${alert.severity.toUpperCase()}</p>
            <p>${alert.message}</p>
            <p>Value: ${alert.metric_value}</p>
            <p>Threshold: ${alert.threshold}</p>
            <p>Status: ${alert.status}</p>
        </div>
    `).join("");
}

async function loadDashboard() {
    try {
        const machines = await fetchJson("/api/machines");
        const latestMetric = await fetchJson("/api/metrics/latest");
        const alerts = await fetchJson("/api/alerts");

        renderMachines(machines);
        renderLatestMetric(latestMetric);
        renderAlerts(alerts);
    } catch (error) {
        console.error(error);

        document.getElementById("machines").innerHTML = "<p>Backend unavailable.</p>";
        document.getElementById("latest-metrics").innerHTML = "<p>Backend unavailable.</p>";
        document.getElementById("alerts").innerHTML = "<p>Backend unavailable.</p>";
    }
}

loadDashboard();

setInterval(loadDashboard, 5000);