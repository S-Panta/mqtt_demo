import mqtt from "mqtt";
import Chart from "chart.js/auto";
import "chartjs-adapter-date-fns";

const brokerUrl = "ws://localhost:9081";
const waterLevelTopic = "waterlevel";
const alertTopic = "alerts";

const client = mqtt.connect(brokerUrl);

client.on("connect", () => {
  console.log("Connected to MQTT broker");
  client.subscribe(waterLevelTopic);
  client.subscribe(alertTopic); 
});

client.on("message", (topic, message) => {
  try {
    const data = JSON.parse(message.toString());

    if (topic === waterLevelTopic) {
      const timestamp = new Date(data.timestamp * 1000);
      const level = data.river_level;
      addDataPoint(timestamp, level);
    }

    if (topic === alertTopic && data.alert === "FLOOD WARNING") {
      const alertTime = new Date(data.timestamp * 1000);
      addAlertAnnotation(alertTime);
      showAlertMessage("FLOOD WARNING: River level is " + data.river_level + " m");
    }

  } catch (err) {
    console.error("Invalid message", err);
  }
});

const ctx = document.getElementById("riverChart");

const chartData = {
  labels: [],
  datasets: [
    {
      label: "River Level (m)",
      data: [],
      borderColor: "blue",
      fill: false,
      tension: 0.1,
    },
  ],
};

const alertLines = [];

const config = {
  type: "line",
  data: chartData,
  options: {
    responsive: true,
    scales: {
      x: {
        type: "time",
        time: {
          tooltipFormat: "HH:mm:ss",
          unit: "second",
          displayFormats: { second: "HH:mm:ss" },
        },
        title: { display: true, text: "Time" },
      },
      y: {
        beginAtZero: true,
        title: { display: true, text: "River Level (m)" },
      },
    },
    plugins: {
      annotation: {
        annotations: alertLines,
      },
    },
  },
};

const riverChart = new Chart(ctx, config);

function addDataPoint(time, level) {
  chartData.labels.push(time);
  chartData.datasets[0].data.push(level);

  if (chartData.labels.length > 50) {
    chartData.labels.shift();
    chartData.datasets[0].data.shift();
  }

  riverChart.update();
}

function addAlertAnnotation(time) {
  const id = `alert-line-${time.getTime()}`;
  alertLines.push({
    type: "line",
    scaleID: "x",
    value: time,
    borderColor: "red",
    borderWidth: 2,
    label: {
      content: "FLOOD WARNING",
      enabled: true,
      position: "top",
      backgroundColor: "rgba(255,0,0,0.7)",
      color: "white",
    },
    id: id,
  });

  riverChart.options.plugins.annotation.annotations = alertLines;
  riverChart.update();
}

function showAlertMessage(msg) {
  const alertBox = document.getElementById("alertBox");
  if (alertBox) {
    alertBox.textContent = msg;
    alertBox.style.display = "block";
    setTimeout(() => {
      alertBox.style.display = "none";
    }, 10000); 
  }
}
