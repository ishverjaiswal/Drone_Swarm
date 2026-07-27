import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function App() {
  const [swarmData, setSwarmData] = useState({});
  const [selectedDrone, setSelectedDrone] = useState("tello_01");
  const [historyMap, setHistoryMap] = useState({});

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/telemetry");

    ws.onmessage = (event) => {
      const swarmTelemetry = JSON.parse(event.data);
      setSwarmData(swarmTelemetry);

      const timestamp = new Date().toLocaleTimeString([], { hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" });

      setHistoryMap((prevHistory) => {
        const updatedHistory = { ...prevHistory };

        Object.keys(swarmTelemetry).forEach((droneId) => {
          const droneMetrics = swarmTelemetry[droneId];
          const previousPoints = updatedHistory[droneId] || [];

          updatedHistory[droneId] = [
            ...previousPoints.slice(-25),
            { time: timestamp, altitude: droneMetrics.altitude, temp: droneMetrics.temperature }
          ];
        });

        return updatedHistory;
      });
    };

    return () => ws.close();
  }, []);

  const availableDrones = Object.keys(swarmData);
  const activeCount = availableDrones.length;

  const activeTelemetry = swarmData[selectedDrone] || {
    drone_id: selectedDrone,
    battery: 0,
    altitude: 0.0,
    pitch: 0,
    roll: 0,
    yaw: 0,
    temperature: 0.0,
  };

  const activeHistory = historyMap[selectedDrone] || [];
  const isOnline = activeTelemetry.battery > 0;

  return (
    <div style={styles.container}>
      {/* Top Header */}
      <header style={styles.header}>
        <div style={styles.brandGroup}>
          <div style={styles.logoIcon}>🛸</div>
          <div>
            <h1 style={styles.title}>DRONE-SWARM <span style={styles.subTitle}>GCS</span></h1>
            <div style={styles.statusRow}>
              <span style={{
                ...styles.statusDot,
                backgroundColor: activeCount > 0 ? "#10b981" : "#eab308",
                boxShadow: activeCount > 0 ? "0 0 10px #10b981" : "0 0 10px #eab308"
              }}></span>
              <span style={styles.statusText}>
                {activeCount > 0 ? `${activeCount} UNIT(S) ACTIVE` : "SEARCHING FOR BROADCASTS..."}
              </span>
            </div>
          </div>
        </div>

        {/* Unit Selector */}
        <div style={styles.selectorGroup}>
          <span style={styles.selectorLabel}>TARGET DRONE</span>
          <select
            value={selectedDrone}
            onChange={(e) => setSelectedDrone(e.target.value)}
            style={styles.selectInput}
          >
            {availableDrones.length > 0 ? (
              availableDrones.map((droneId) => (
                <option key={droneId} value={droneId}>
                  {droneId.toUpperCase()}
                </option>
              ))
            ) : (
              <option value="tello_01">NO DRONES CONNECTED</option>
            )}
          </select>
        </div>
      </header>

      {/* Main Content Layout */}
      <main style={styles.mainContent}>
        {/* Telemetry Metric Cards */}
        <div style={styles.metricsGrid}>
          <MetricCard
            label="BATTERY LEVEL"
            value={`${activeTelemetry.battery}%`}
            color={activeTelemetry.battery < 20 ? "#ef4444" : "#10b981"}
            subtext={activeTelemetry.battery < 20 ? "CRITICAL" : "HEALTHY"}
          />
          <MetricCard
            label="ALTITUDE"
            value={`${activeTelemetry.altitude.toFixed(2)} m`}
            color="#3b82f6"
            subtext="TOF SENSOR"
          />
          <MetricCard
            label="ATTITUDE (P / R)"
            value={`${activeTelemetry.pitch}° / ${activeTelemetry.roll}°`}
            color="#06b6d4"
            subtext="PITCH & ROLL"
          />
          <MetricCard
            label="HEADING (YAW)"
            value={`${activeTelemetry.yaw}°`}
            color="#a855f7"
            subtext="COMPASS"
          />
          <MetricCard
            label="TEMPERATURE"
            value={`${activeTelemetry.temperature.toFixed(1)} °C`}
            color={activeTelemetry.temperature > 50 ? "#f97316" : "#f59e0b"}
            subtext={activeTelemetry.temperature > 50 ? "OVERHEAT RISK" : "NOMINAL"}
          />
        </div>

        {/* Primary Views: Video & Telemetry Stream */}
        <div style={styles.viewsGrid}>
          {/* Live Camera Feed Card */}
          <div style={styles.card}>
            <div style={styles.cardHeader}>
              <span style={styles.cardTitle}>📹 OPTICAL STREAM — {selectedDrone.toUpperCase()}</span>
              <span style={{
                ...styles.badge,
                color: isOnline ? "#10b981" : "#64748b",
                borderColor: isOnline ? "rgba(16, 185, 129, 0.3)" : "#334155"
              }}>
                {isOnline ? "LIVE FEED" : "OFFLINE"}
              </span>
            </div>
            <div style={styles.videoContainer}>
              <img
                key={selectedDrone}
                src={`http://localhost:8000/video_feed/${selectedDrone}`}
                alt={`Stream - ${selectedDrone}`}
                style={styles.videoStream}
                onError={(e) => {
                  e.target.style.display = "none";
                }}
              />
              {!isOnline && (
                <div style={styles.offlineOverlay}>
                  <div style={{ fontSize: "32px", marginBottom: "8px" }}>📡</div>
                  <span style={{ color: "#94a3b8", fontSize: "14px", fontWeight: "600" }}>
                    SIGNAL LOST / DISCONNECTED
                  </span>
                  <span style={{ color: "#64748b", fontSize: "12px", marginTop: "4px" }}>
                    Awaiting UDP packets on port 8890
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Real-Time Chart Card */}
          <div style={styles.card}>
            <div style={styles.cardHeader}>
              <span style={styles.cardTitle}>📊 ALTITUDE TELEMETRY LOG</span>
              <span style={styles.chartSubtext}>2Hz REAL-TIME STREAM</span>
            </div>
            <div style={{ width: "100%", height: "280px" }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={activeHistory} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <XAxis dataKey="time" stroke="#475569" tick={{ fill: "#64748b", fontSize: 11 }} />
                  <YAxis stroke="#475569" tick={{ fill: "#64748b", fontSize: 11 }} domain={[0, 'auto']} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#090d16",
                      borderColor: "#1e293b",
                      borderRadius: "6px",
                      color: "#f8fafc"
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="altitude"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    dot={false}
                    isAnimationActive={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function MetricCard({ label, value, color, subtext }) {
  return (
    <div style={{ ...styles.card, ...styles.metricCard, borderTop: `3px solid ${color}` }}>
      <span style={styles.metricLabel}>{label}</span>
      <div style={{ ...styles.metricValue, color }}>{value}</div>
      <span style={styles.metricSubtext}>{subtext}</span>
    </div>
  );
}

// Styling Dictionary
const styles = {
  container: {
    backgroundColor: "#070a11",
    color: "#f8fafc",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    minHeight: "100vh",
    padding: "24px 32px",
    boxSizing: "border-box",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    borderBottom: "1px solid #1e293b",
    paddingBottom: "20px",
    marginBottom: "28px",
  },
  brandGroup: {
    display: "flex",
    alignItems: "center",
    gap: "16px",
  },
  logoIcon: {
    fontSize: "28px",
    backgroundColor: "rgba(59, 130, 246, 0.1)",
    border: "1px solid rgba(59, 130, 246, 0.3)",
    padding: "10px 14px",
    borderRadius: "10px",
  },
  title: {
    margin: 0,
    fontSize: "22px",
    fontWeight: "800",
    letterSpacing: "1px",
    color: "#f8fafc",
  },
  subTitle: {
    color: "#3b82f6",
    fontWeight: "400",
  },
  statusRow: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    marginTop: "4px",
  },
  statusDot: {
    width: "8px",
    height: "8px",
    borderRadius: "50%",
  },
  statusText: {
    color: "#94a3b8",
    fontSize: "11px",
    fontWeight: "700",
    letterSpacing: "0.5px",
  },
  selectorGroup: {
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-end",
    gap: "6px",
  },
  selectorLabel: {
    fontSize: "11px",
    fontWeight: "700",
    color: "#64748b",
    letterSpacing: "1px",
  },
  selectInput: {
    backgroundColor: "#0f172a",
    color: "#f8fafc",
    border: "1px solid #334155",
    padding: "10px 16px",
    borderRadius: "8px",
    fontSize: "13px",
    fontWeight: "600",
    cursor: "pointer",
    outline: "none",
    minWidth: "200px",
  },
  mainContent: {
    display: "flex",
    flexDirection: "column",
    gap: "24px",
  },
  metricsGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "16px",
  },
  card: {
    backgroundColor: "#0d1322",
    borderRadius: "12px",
    border: "1px solid #1e293b",
    padding: "20px",
    boxShadow: "0 4px 20px rgba(0, 0, 0, 0.25)",
  },
  metricCard: {
    display: "flex",
    flexDirection: "column",
    padding: "16px 20px",
  },
  metricLabel: {
    fontSize: "11px",
    fontWeight: "700",
    color: "#64748b",
    letterSpacing: "0.5px",
  },
  metricValue: {
    fontSize: "26px",
    fontWeight: "800",
    margin: "8px 0 2px 0",
  },
  metricSubtext: {
    fontSize: "10px",
    color: "#475569",
    fontWeight: "700",
    letterSpacing: "0.5px",
  },
  viewsGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "24px",
  },
  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "16px",
  },
  cardTitle: {
    fontSize: "13px",
    fontWeight: "700",
    color: "#cbd5e1",
    letterSpacing: "0.5px",
  },
  badge: {
    fontSize: "10px",
    fontWeight: "800",
    padding: "4px 8px",
    borderRadius: "4px",
    border: "1px solid",
    letterSpacing: "0.5px",
  },
  chartSubtext: {
    fontSize: "10px",
    color: "#64748b",
    fontWeight: "700",
  },
  videoContainer: {
    width: "100%",
    height: "280px",
    backgroundColor: "#050811",
    borderRadius: "8px",
    overflow: "hidden",
    position: "relative",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    border: "1px solid #1e293b",
  },
  videoStream: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
  },
  offlineOverlay: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    position: "absolute",
    textAlign: "center",
  },
};