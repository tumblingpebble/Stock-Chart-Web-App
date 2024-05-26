const chart = LightweightCharts.createChart(document.getElementById('chart'), {
    layout: {
        backgroundColor: '#ffffff',
        textColor: '#000000',
    },
    grid: {
        vertLines: {
            color: '#e0e0e0',
        },
        horzLines: {
            color: '#e0e0e0',
        },
    },
    timeScale: {
        timeVisible: true,
        secondsVisible: true,
    },
    watermark: {
        color: 'rgba(0, 0, 0, 0.1)',
        visible: true,
        text: 'Stock Chart',
        fontSize: 24,
        horzAlign: 'left',
        vertAlign: 'top',
    },
});

const lineSeries = chart.addLineSeries();

function fetchAndRenderData() {
    const ticker = document.getElementById('ticker').value;
    const interval = document.getElementById('interval').value;
    const errorMessage = document.getElementById('error-message');

    fetch(`/stock-data?ticker=${ticker}&interval=${interval}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => { throw new Error(error.error); });
            }
            return response.json();
        })
        .then(data => {
            errorMessage.style.display = 'none';
            const formattedData = data.map(item => ({
                time: new Date(item.time).getTime() / 1000, // convert to Unix timestamp
                value: item.value
            }));
            lineSeries.setData(formattedData);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            errorMessage.textContent = `Error: ${error.message}`;
            errorMessage.style.display = 'block';
        });
}

// Initial load
fetchAndRenderData();

document.getElementById('updateChart').addEventListener('click', fetchAndRenderData);
document.getElementById('interval').addEventListener('change', fetchAndRenderData);
