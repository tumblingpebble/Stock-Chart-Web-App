const chart = LightweightCharts.createChart(document.getElementById('chart'), {
    width: 800,
    height: 500,
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
});

const lineSeries = chart.addLineSeries();
lineSeries.setData([
    { time: '2024-05-21', value: 34.48 },
    { time: '2024-05-22', value: 34.78 },
    { time: '2024-05-23', value: 34.74 },
    { time: '2024-05-24', value: 34.59 },
]);

function takeScreenshot() {
    chart.takeScreenshot().then((image) => {
        const base64Image = image.split(',')[1]; // remove data:image/png;base64
        const symbol = 'AAPL'; // example symbol

        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: base64Image, symbol: symbol }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('analysis').textContent = data.analysis;
        });
    });
}
