
const ctx = document.getElementById('syscallChart').getContext('2d');
const labels = [];
const data = {
  labels: labels,
  datasets: [{
    label: 'Syscall Return Values',
    backgroundColor: '#007BFF',
    borderColor: '#007BFF',
    data: [],
    fill: false,
    tension: 0.3
  }]
};

const config = {
  type: 'line',
  data: data,
  options: {
    responsive: true,
    animation: false,
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
};

const syscallChart = new Chart(ctx, config);

function fetchSyscalls() {
  fetch('/get_syscalls')
    .then(res => res.json())
    .then(syscall => {
      if (labels.length >= 10) {
        labels.shift();
        syscallChart.data.datasets[0].data.shift();
      }
      labels.push(syscall.timestamp);
      syscallChart.data.datasets[0].data.push(syscall.return);
      syscallChart.update();
    });
}

setInterval(fetchSyscalls, 2000);
