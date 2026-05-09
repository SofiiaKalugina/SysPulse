const API_URL = "http://127.0.0.1:8000";

async function fetchJson(endpoint) {
    const response = await fetch(`${API_URL}${endpoint}`);

    if (!response.ok) {
        throw new Error(`Request failed: ${endpoint}`);
    }

    return response.json();
}

function formatPercent(value) {
    if (value === null || value === undefined) {
        return "-";
    }

    return `${Number(value).toFixed(1)}%`;
}

function renderSummary(machines, alerts, history) {
    const totalMachines = machines.length;
    const onlineMachines = machines.filter(machine => machine.status === "online").length;
    const activeAlerts = alerts.filter(alert => alert.status === "active").length;

    const avg = (values) => {
        if (values.length === 0) {
            return null;
        }

        const sum = values.reduce((total, value) => total + Number(value), 0);
        return sum / values.length;
    };

    document.getElementById("total-machines").textContent = totalMachines;
    document.getElementById("online-machines").textContent = onlineMachines;
    document.getElementById("active-alerts").textContent = activeAlerts;

    document.getElementById("avg-cpu").textContent = formatPercent(
        avg(history.map(metric => metric.cpu_percent))
    );

    document.getElementById("avg-ram").textContent = formatPercent(
        avg(history.map(metric => metric.ram_percent))
    );

    document.getElementById("avg-disk").textContent = formatPercent(
        avg(history.map(metric => metric.disk_percent))
    );
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
            <p>CPU: ${formatPercent(metric.cpu_percent)}</p>
            <p>RAM: ${formatPercent(metric.ram_percent)}</p>
            <p>Disk: ${formatPercent(metric.disk_percent)}</p>
            <p>Processes: ${metric.process_count}</p>
            <p class="small">Timestamp: ${metric.timestamp}</p>
        </div>
    `;
}

function renderAlertItem(alert) {
    return `
        <div class="item">
            <p>
                <span class="badge badge-${alert.severity}">${alert.severity}</span>
                <span class="badge badge-${alert.status}">${alert.status}</span>
            </p>
            <p><strong>${alert.metric_name}</strong></p>
            <p>${alert.message}</p>
            <p>Value: ${formatPercent(alert.metric_value)}</p>
            <p>Threshold: ${formatPercent(alert.threshold)}</p>
            <div class="alert-meta">
                <p>Created: ${alert.created_at}</p>
                ${alert.resolved_at ? `<p>Resolved: ${alert.resolved_at}</p>` : ""}
            </div>
        </div>
    `;
}

function renderAlerts(alerts) {
    const activeContainer = document.getElementById("active-alerts-list");
    const resolvedContainer = document.getElementById("resolved-alerts-list");

    const activeAlerts = alerts.filter(alert => alert.status === "active");
    const resolvedAlerts = alerts.filter(alert => alert.status === "resolved");

    if (activeAlerts.length === 0) {
        activeContainer.innerHTML = "<p>No active alerts.</p>";
    } else {
        activeContainer.innerHTML = activeAlerts.map(renderAlertItem).join("");
    }

    if (resolvedAlerts.length === 0) {
        resolvedContainer.innerHTML = "<p>No resolved alerts.</p>";
    } else {
        resolvedContainer.innerHTML = resolvedAlerts.map(renderAlertItem).join("");
    }
}

function renderHistory(history) {
    const container = document.getElementById("metrics-history");

    if (history.length === 0) {
        container.innerHTML = "<p>No history yet.</p>";
        return;
    }

    container.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Host</th>
                    <th>CPU</th>
                    <th>RAM</th>
                    <th>Disk</th>
                    <th>Processes</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
                ${history.map(metric => `
                    <tr>
                        <td>${metric.hostname}</td>
                        <td>${formatPercent(metric.cpu_percent)}</td>
                        <td>${formatPercent(metric.ram_percent)}</td>
                        <td>${formatPercent(metric.disk_percent)}</td>
                        <td>${metric.process_count}</td>
                        <td>${metric.timestamp}</td>
                    </tr>
                `).join("")}
            </tbody>
        </table>
    `;
}

async function loadDashboard() {
    try {
        const machines = await fetchJson("/api/machines");
        const latestMetric = await fetchJson("/api/metrics/latest");
        const alerts = await fetchJson("/api/alerts");
        const history = await fetchJson("/api/metrics/history?limit=10");

        renderSummary(machines, alerts, history);
        renderMachines(machines);
        renderLatestMetric(latestMetric);
        renderAlerts(alerts);
        renderHistory(history);

        document.getElementById("refresh-status").textContent =
            `Last refresh: ${new Date().toLocaleTimeString()}`;

    } catch (error) {
        console.error(error);

        document.getElementById("machines").innerHTML = "<p>Backend unavailable.</p>";
        document.getElementById("latest-metrics").innerHTML = "<p>Backend unavailable.</p>";
        document.getElementById("active-alerts-list").innerHTML = "<p>Backend unavailable.</p>";
        document.getElementById("resolved-alerts-list").innerHTML = "<p>Backend unavailable.</p>";
        document.getElementById("metrics-history").innerHTML = "<p>Backend unavailable.</p>";
        document.getElementById("refresh-status").textContent = "Backend unavailable.";
    }
}

loadDashboard();

setInterval(loadDashboard, 5000);