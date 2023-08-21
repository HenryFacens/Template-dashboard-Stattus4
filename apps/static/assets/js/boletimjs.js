document.addEventListener('DOMContentLoaded', function () {
    const searchBox = document.getElementById('clienteSearch');
    
    searchBox.addEventListener('input', function () {
        const searchQuery = this.value.toLowerCase();
        
        // Loop through each client container
        document.querySelectorAll('.client-container').forEach(function (clientDiv) {
            const clientName = clientDiv.querySelector('span').textContent.toLowerCase();
            let hasMatchingSubClient = false;

            // Check each sub-client under the current client
            const subItems = clientDiv.querySelectorAll('.list-group-item');
            subItems.forEach(function (subItem) {
                if (subItem.textContent.toLowerCase().includes(searchQuery)) {
                    hasMatchingSubClient = true;
                    subItem.style.display = ''; // show
                } else {
                    subItem.style.display = 'none'; // hide
                }
            });
            
            if (clientName.includes(searchQuery) || hasMatchingSubClient) {
                clientDiv.style.display = ''; // show
            } else {
                clientDiv.style.display = 'none'; // hide
            }
        });
    });
});



function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}
function sendClientId(element) {

    var clientId = element.getAttribute('data-id');
    console.log(clientId)
    var clientName = element.getAttribute('data-name');
    var date1Value = document.getElementById('id_date_1').value;
    var date2Value = document.getElementById('id_date_2').value;

    if (!clientId) {
        alert("Por favor, selecione um cliente.");
        return;
    }

    if (!date1Value || !date2Value) {
        alert("Por favor, preencha ambas as datas.");
        return;
    }

    console.log(clientName);

    fetch('/boletim-fluid/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            id: clientId,
            name: clientName,
            date_1: date1Value,
            date_2: date2Value
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            function getColorForLabelPontos(label) {
                switch(label) {
                    case 'Ponto Não Confirmado':
                        return 'red';
                    case 'Pontos Confirmados':
                        return 'green';
                    case 'Pendente':
                        return 'yellow';
                    default:
                        return 'gray';  // Uma cor padrão caso haja outras categorias
                }
            }

            // Total Coletas
            const groupedData = data.t_coletas.reduce((acc, item) => {
                if (!acc[item[1]]) {
                    acc[item[1]] = item[2];
                } else {
                    acc[item[1]] += item[2];
                }
                return acc;
            }, {});

            const sortedArray = Object.entries(groupedData)
                .sort((a, b) => new Date(a[0]) - new Date(b[0]));

            const labelsAmostras = sortedArray.map(item => item[0]);
            const dataValuesAmostras = sortedArray.map(item => item[1]);

            var $chartElementAmostras = $('#bar-chart-amostras');
            var existingChart = $chartElementAmostras.data('chart');
            if (existingChart) {
                existingChart.data.labels = labelsAmostras;
                existingChart.data.datasets[0].data = dataValuesAmostras;
                existingChart.update();
            } else {
                initChartbar($chartElementAmostras, labelsAmostras, dataValuesAmostras, null, false);
            }
            
            // Classificao
            const labelsPontos = Object.keys(data.pontos);
            const barColorsPontos = labelsPontos.map(getColorForLabelPontos);
            const dataValuesPontos = Object.values(data.pontos);
        
            var $chartElementPontos = $('#bar-chart-pontos');
            var existingChart = $chartElementPontos.data('chart');
            if (existingChart) {
                existingChart.data.labels = labelsPontos;
                existingChart.data.datasets[0].data = dataValuesPontos;
                existingChart.data.datasets[0].backgroundColor = barColorsPontos;
                existingChart.update();
            } else {
                initChartbar($chartElementPontos, labelsPontos, dataValuesPontos, barColorsPontos, false);
            }

            function getColorForLabelClasses(label) {
                switch(label) {
                    case 'Sem Vazamento':
                        return 'green';
                    case 'Ponto Suspeito':
                        return 'red';
                    case 'Fraude':
                        return 'black';
                    case 'Sem Acesso':
                        return 'gray';
                    case 'Consumo':
                        return '#ADD8E6';  // Azul bebê em hexadecimal
                    case 'Inconsistente':
                        return 'darkblue'; // Azul escuro
                    case 'Pendente':
                        return 'yellow';
                    case 'Vazamento Visível':
                        return 'purple'; 
                    default:
                        return 'gray';  // Uma cor padrão caso haja outras categorias não listadas
                }
            }

            // Classificacao
            const dataValuesClassesRaw = data.classes;
            const dataValuesClasses = dataValuesClassesRaw.slice(0);
            const labelsClasses = ['Fraude', 'Inconsistente', 'Ponto Suspeito', 'Sem Vazamento', 'Sem Acesso', 'Consumo', 'Pendente', 'Vazamento Visível'];
            const barColorsClasses = labelsClasses.map(getColorForLabelClasses);
            var $chartElementClasses = $('#pie-chart');
            var existingChart = $chartElementClasses.data('chart');
            function generateLabelsWithValues(labels, data) {
                return labels.map(function(label, index) {
                    return label + " (" + data[index] + ")";
                });
            }
            if (existingChart) {
                existingChart.data.labels = generateLabelsWithValues(labelsClasses, dataValuesClasses);
                existingChart.data.datasets[0].data = dataValuesClasses;
                existingChart.data.datasets[0].backgroundColor = barColorsClasses;
                existingChart.update();
            } else {
                initChartpie($chartElementClasses, labelsClasses, dataValuesClasses, barColorsClasses);
            }
        

        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
