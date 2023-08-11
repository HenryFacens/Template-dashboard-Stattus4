Chart.plugins.register({
    afterDraw: function(chart) {
        var ctx = chart.ctx;

        ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
        ctx.textAlign = 'center';
        ctx.textBaseline = 'bottom';

        chart.data.datasets.forEach(function(dataset, i) {
            var meta = chart.getDatasetMeta(i);
            meta.data.forEach(function(bar, index) {
                var data = dataset.data[index];
                ctx.fillText(data, bar._model.x, bar._model.y - 5);
            });
        });
    }
});

function initChart($chartElement, labels, data) {
    var ordersChart = new Chart($chartElement, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Sales',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)', 
                borderColor: 'rgba(75, 192, 192, 1)',  
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            tooltips: {
                enabled: false
            }
        }
    });

    $chartElement.data('chart', ordersChart);
}
