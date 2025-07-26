const ws = new WebSocket(`ws://${location.host}/ws`);

ws.onopen = () => console.log("✅ WebSocket connected");

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.type === "log") {
        addLog(message.data);
    } else if (message.type === "alert") {
        addAlert(message.data);
    }
};

ws.onclose = () => console.log("❌ WebSocket disconnected");

function addLog({ log, label }) {
    const table = document.getElementById("logs-table").querySelector("tbody");
    const row = document.createElement("tr");
    const timestamp = new Date().toLocaleString();
    row.innerHTML = `<td>${timestamp}</td><td>${label}</td><td>${log}</td>`;
    row.className = label === "anomaly" ? "anomaly" : "normal";
    table.prepend(row);
}

function addAlert({ log, advice }) {
    const list = document.getElementById("alerts-list");
    const item = document.createElement("li");
    item.innerHTML = `<b>${advice}</b><br/><small>${log}</small>`;
    item.className = "alert";
    list.prepend(item);
}
