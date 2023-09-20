Chart.plugins.register({
    afterDraw: function(chart) {
        if (chart.config.type === 'pie') {
            return; // Se o tipo de gráfico for 'pie', saia da função e não faça nada.
        }
        if (chart.config.type === 'line') {
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
function randomRGB() {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return `rgb(${r}, ${g}, ${b})`;
}

function initChartLine($chartElement, labels, datasets, legend_onoff = true) {

    let minValues = datasets.map(dataset => Math.min(...dataset.data.filter(Boolean)));
    let minValue = Math.min(...minValues);

    // 1. Extraia a configuração de yAxes para uma variável
    const yAxesConfig = [{
        gridLines: {
            lineWidth: 3,
            color: 'gray',
            zeroLineColor: 'gray'
        },
        ticks: {
            beginAtZero: false,
            min: minValue - 20,
            callback: function(value) {
                if (!(value % 10)) {
                    return value + ' mca';
                }
            }
        }
    }];

    let existingChart = $($chartElement).data('chart');

    if (existingChart) {
        existingChart.data.labels = labels;
        existingChart.data.datasets = datasets.map(dataset => ({
            ...dataset,
            fill: false,
            borderWidth: 3,
            pointRadius: 4,  // Adiciona pontos aos valores
            pointBackgroundColor: dataset.data.map(() => randomRGB())
        }));

        // 2. Atualize também as opções de escala
        existingChart.options.scales.yAxes = yAxesConfig;
        
        // 3. Chame update() no gráfico existente
        existingChart.update();
        return existingChart;
    } else {
        let salesChart = new Chart($chartElement, {
            type: 'line',
            options: {
                scales: {
                    yAxes: [{
                        gridLines: {
                            lineWidth: 3,
                            color: 'gray',
                            zeroLineColor: 'gray'
                        },
                        ticks: {
                            beginAtZero: false,
                            min: minValue - 20,
                            callback: function(value) {
                                if (!(value % 10)) {
                                    return value + ' mca';
                                }
                            }
                        }
                    }]
                },
                tooltips: {
                    callbacks: {
                        mode: 'point',      // Define a exibição do tooltip apenas para o ponto sob o mouse
                        intersect: true,    // Garante que apenas o ponto sob o mouse seja destacado
                        label: function(item, data) {
                            var label = data.datasets[item.datasetIndex].label || '';
                            var yLabel = item.yLabel;
                            var content = '';
                            content += label + ": " + yLabel + " mca";
                            return content;
                        }
                    }
                },
                legend: {
                    display: legend_onoff,
                }
            },
            data: {
                labels: labels,
                datasets: datasets.map(dataset => ({
                    ...dataset,
                    fill: false,
                    borderWidth: 3,
                    pointRadius: 4,  // Adiciona pontos aos valores
                    pointBackgroundColor: dataset.data.map(() => randomRGB())  // Gera uma cor aleatória para cada ponto
                }))
            }
        });
        $($chartElement).data('chart', salesChart);
        return salesChart;
    }
}
