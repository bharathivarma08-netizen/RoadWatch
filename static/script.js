const API_BASE = "";

const SEVERITY_COLORS = {
    High:   "#D32F2F",
    Medium: "#FF9800",
    Low:    "#4CAF50"
};

const map = L.map("map").setView([16.5062, 80.6480], 12);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19
}).addTo(map);

let markerLayer = L.layerGroup().addTo(map);

async function loadPotholes() {
    try {
        const res = await fetch(`${API_BASE}/potholes`);
        const potholes = await res.json();

        markerLayer.clearLayers();

        let total = 0, high = 0, medium = 0, low = 0;
        let hasHighRisk = false;

        potholes.forEach(p => {
            if (p.status !== "active") return;

            total++;
            if (p.severity === "High")        { high++;   hasHighRisk = true; }
            else if (p.severity === "Medium")    medium++;
            else                                 low++;

            const marker = L.circleMarker([p.latitude, p.longitude], {
                radius:      p.severity === "High" ? 12 : p.severity === "Medium" ? 9 : 7,
                fillColor:   SEVERITY_COLORS[p.severity],
                color:       "#fff",
                weight:      2,
                fillOpacity: 0.85
            });

            marker.bindPopup(`
                <div style="font-family:sans-serif;min-width:180px;">
                    <b style="color:${SEVERITY_COLORS[p.severity]}">${p.severity} Risk Pothole</b><br>
                    <small>📍 ${p.latitude.toFixed(5)}, ${p.longitude.toFixed(5)}</small><br>
                    <small>🕒 ${new Date(p.timestamp).toLocaleString()}</small><br>
                    <small>✅ Confirmed: ${p.confirmed_count || 0} times</small><br><br>
                    <button onclick="resolvePothole('${p.id}')"
                        style="background:#4CAF50;color:#fff;border:none;
                               padding:4px 10px;border-radius:4px;cursor:pointer;">
                        Mark Resolved
                    </button>
                </div>
            `);

            markerLayer.addLayer(marker);
        });

        // Update stats — matching your index.html IDs
        document.getElementById("totalCount").textContent  = total;
        document.getElementById("highCount").textContent   = high;
        document.getElementById("mediumCount").textContent = medium;
        document.getElementById("lowCount").textContent    = low;

        updateAlert(hasHighRisk, high, total);

    } catch (err) {
        console.error("Failed to load potholes:", err);
    }
}

function updateAlert(hasHighRisk, highCount, total) {
    const banner = document.getElementById("alertBanner");
    if (!banner) return;

    if (hasHighRisk) {
        banner.style.background = "#D32F2F";
        banner.textContent = `⚠️ DANGER: ${highCount} high-risk pothole(s) detected. Drive carefully!`;
    } else if (total > 0) {
        banner.style.background = "#FF9800";
        banner.textContent = `⚠️ CAUTION: ${total} pothole(s) reported nearby. Reduce speed.`;
    } else {
        banner.style.background = "#4CAF50";
        banner.textContent = "✅ No active potholes reported. Road is clear.";
    }
}

async function reportPothole() {
    const lat      = parseFloat(document.getElementById("latitude").value);
    const lon      = parseFloat(document.getElementById("longitude").value);
    const severity = document.getElementById("severity").value;

    if (isNaN(lat) || isNaN(lon)) {
        alert("Please enter valid coordinates.");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/report`, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ latitude: lat, longitude: lon, severity: severity })
        });

        if (res.ok) {
            alert("✅ Pothole reported successfully!");
            document.getElementById("latitude").value  = "";
            document.getElementById("longitude").value = "";
            loadPotholes();
        } else {
            alert("❌ Failed to submit. Try again.");
        }
    } catch (err) {
        alert("❌ Server not reachable.");
    }
}

async function resolvePothole(id) {
    try {
        const res = await fetch(`${API_BASE}/resolve`, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ id })
        });
        if (res.ok) {
            alert("✅ Marked as resolved.");
            loadPotholes();
        }
    } catch (err) {
        console.error("Resolve failed:", err);
    }
}

// Load on start + refresh every 30 seconds
loadPotholes();
setInterval(loadPotholes, 30000);