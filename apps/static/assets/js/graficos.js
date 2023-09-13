Chart.plugins.register({
    afterDraw: function(chart) {
        if (chart.config.type === 'pie') {
            return; // Se o tipo de gráfico for 'pie', saia da função e não faça nada.
        }
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

function initChartbar($chartElement, labels, data, colors, legend_onoff = true ,legend = 'Sales') {
    var ordersChart = new Chart($chartElement, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: legend,
                data: data,
                backgroundColor: colors, 
                borderColor: colors,  
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
            },
            legend: {
                display: legend_onoff,
            },
            tooltips: {
                enabled: false
            }
        }
    });

    $chartElement.data('chart', ordersChart);
}

function initChartpie($chartElement, labels, data, colors,legend_onoff = true,  legend = 'Sales',legend_local = 'bottom') {
    var ordersChart = new Chart($chartElement, {
        type: 'pie',
        data: {
            labels: labels.map(function(label, index) {
                return label + " (" + data[index] + ")";  // Adiciona valores aos rótulos.
            }),
            datasets: [{
                label: legend,
                data: data,
                backgroundColor: colors, 
                borderColor: colors,  
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    display: false  // Remove o eixo Y, pois não é necessário em gráficos de pizza.
                }
            },
            legend: {
                display: legend_onoff,  // Mostra a legenda.
                position: legend_local  // Define a posição da legenda.
            },
            tooltips: {
                enabled: false
            }
        }
    });

    $chartElement.data('chart', ordersChart);
}

function initChartline($chartElement, labels, data, colors, legend_onoff = true ,legend = 'Sales') {
    var ordersChart = new Chart($chartElement, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: legend,
                data: data,
                backgroundColor: colors, 
                borderColor: colors,  
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
            },
            legend: {
                display: legend_onoff,
            },
            tooltips: {
                enabled: false
            }
        }
    });

    $chartElement.data('chart', ordersChart);
}