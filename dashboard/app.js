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

function renderSummary(summary) {
    document.getElementById("total-machines").textContent = summary.total_machines;
    document.getElementById("online-machines").textContent = summary.online_machines;
    document.getElementById("active-alerts").textContent = summary.active_alerts;

    document.getElementById("avg-cpu").textContent = formatPercent(summary.avg_cpu);
    document.getElementById("avg-ram").textContent = formatPercent(summary.avg_ram);
    document.getElementById("avg-disk").textContent = formatPercent(summary.avg_disk);
}

function metricProgress(label, value) {
    const numericValue = Number(value);
    const safeValue = Math.min(Math.max(numericValue, 0), 100);
    const warningClass = safeValue >= 80 ? "progress-warning" : "";

    return `
        <div class="metric-row">
            <div class="metric-label">
                <span>${label}</span>
                <strong>${formatPercent(safeValue)}</strong>
            </div>
            <div class="progress">
                <div class="progress-fill ${warningClass}" style="width: ${safeValue}%"></div>
            </div>
        </div>
    `;
}

function getPanelBody(panelId) {
    return document.querySelector(`#${panelId} .panel-body`);
}

function renderMachines(machines) {
    const container = getPanelBody("machines");

    if (machines.length === 0) {
        container.innerHTML = '<p class="empty-state">No machines found.</p>';
        return;
    }

    container.innerHTML = machines.map(machine => `
        <div class="item">
            <strong>${machine.hostname}</strong>
            <p>
                <span class="status-pill status-${machine.status}">
                    ${machine.status}
                </span>
            </p>
            <p class="small">OS: ${machine.os_name} ${machine.os_version}</p>
            <p class="small">Last seen: ${machine.last_seen_at}</p>
        </div>
    `).join("");
}

function renderLatestMetric(metricData) {
    const container = getPanelBody("latest-metrics");

    if (metricData.status === "empty") {
        container.innerHTML = '<p class="empty-state">No metrics received yet.</p>';
        return;
    }

    const metric = metricData;

    container.innerHTML = `
        <div class="item">
            <strong>${metric.hostname}</strong>

            ${metricProgress("CPU", metric.cpu_percent)}
            ${metricProgress("RAM", metric.ram_percent)}
            ${metricProgress("Disk", metric.disk_percent)}

            <p class="small">Processes: ${metric.process_count}</p>
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
            <p class="small">Value: ${formatPercent(alert.metric_value)}</p>
            <p class="small">Threshold: ${formatPercent(alert.threshold)}</p>
            <div class="alert-meta">
                <p>Created: ${alert.created_at}</p>
                ${alert.resolved_at ? `<p>Resolved: ${alert.resolved_at}</p>` : ""}
            </div>
        </div>
    `;
}

function renderAlerts(alerts) {
    const activeContainer = getPanelBody("active-alerts-list");
    const resolvedContainer = getPanelBody("resolved-alerts-list");

    const activeAlerts = alerts.filter(alert => alert.status === "active");
    const resolvedAlerts = alerts.filter(alert => alert.status === "resolved");

    if (activeAlerts.length === 0) {
        activeContainer.innerHTML = '<p class="empty-state">No active alerts.</p>';
    } else {
        activeContainer.innerHTML = activeAlerts.map(renderAlertItem).join("");
    }

    if (resolvedAlerts.length === 0) {
        resolvedContainer.innerHTML = '<p class="empty-state">No resolved alerts.</p>';
    } else {
        resolvedContainer.innerHTML = resolvedAlerts.map(renderAlertItem).join("");
    }
}

function renderHistory(history) {
    const container = document.getElementById("metrics-history");

    if (history.length === 0) {
        container.innerHTML = '<p class="empty-state">No history yet.</p>';
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

function setBackendStatus(isOnline) {
    const statusElement = document.getElementById("backend-status");

    if (isOnline) {
        statusElement.textContent = "Online";
        statusElement.className = "connection-status connection-online";
    } else {
        statusElement.textContent = "Offline";
        statusElement.className = "connection-status connection-offline";
    }
}

function renderAlertAnalytics(analytics) {
    document.getElementById("intel-total-alerts").textContent = analytics.total_alerts;
    document.getElementById("intel-active-alerts").textContent = analytics.active_alerts;
    document.getElementById("intel-resolved-alerts").textContent = analytics.resolved_alerts;

    document.getElementById("intel-common-alert").textContent =
        analytics.most_common_alert || "None";

    document.getElementById("intel-noisy-machine").textContent =
        analytics.noisy_machine || "None";
}

function renderIncidentSummary(incidentSummary) {
    document.getElementById("incident-summary-text").textContent =
        incidentSummary.summary || "No incident summary available.";
}

async function loadDashboard() {
    try {
        const summary = await fetchJson("/api/summary");
        const machines = await fetchJson("/api/machines");
        const latestMetric = await fetchJson("/api/metrics/latest");
        const alerts = await fetchJson("/api/alerts");
        const history = await fetchJson("/api/metrics/history?limit=10");
        const alertAnalytics = await fetchJson("/api/alerts/analytics");
        const incidentSummary = await fetchJson("/api/incidents/summary");

        renderSummary(summary);
        renderMachines(machines);
        renderLatestMetric(latestMetric);
        renderAlerts(alerts);
        renderHistory(history);
        renderAlertAnalytics(alertAnalytics);
        renderIncidentSummary(incidentSummary);

        setBackendStatus(true);

        document.getElementById("refresh-status").textContent =
            `Last refresh: ${new Date().toLocaleTimeString()}`;

    } catch (error) {
        console.error(error);

        getPanelBody("machines").innerHTML = '<p class="empty-state">Backend unavailable.</p>';
        getPanelBody("latest-metrics").innerHTML = '<p class="empty-state">Backend unavailable.</p>';
        getPanelBody("active-alerts-list").innerHTML = '<p class="empty-state">Backend unavailable.</p>';
        getPanelBody("resolved-alerts-list").innerHTML = '<p class="empty-state">Backend unavailable.</p>';
        document.getElementById("metrics-history").innerHTML = '<p class="empty-state">Backend unavailable.</p>';

        document.getElementById("total-machines").textContent = "-";
        document.getElementById("online-machines").textContent = "-";
        document.getElementById("active-alerts").textContent = "-";
        document.getElementById("avg-cpu").textContent = "-";
        document.getElementById("avg-ram").textContent = "-";
        document.getElementById("avg-disk").textContent = "-";
        document.getElementById("intel-total-alerts").textContent = "-";
        document.getElementById("intel-active-alerts").textContent = "-";
        document.getElementById("intel-resolved-alerts").textContent = "-";
        document.getElementById("intel-common-alert").textContent = "-";
        document.getElementById("intel-noisy-machine").textContent = "-";
        document.getElementById("incident-summary-text").textContent = "Backend unavailable.";

        setBackendStatus(false);

        document.getElementById("refresh-status").textContent = "Backend unavailable.";
    }
}

loadDashboard();

setInterval(loadDashboard, 5000);