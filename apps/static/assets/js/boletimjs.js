
function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}
function sendClientId(element) {

    var clientId = element.getAttribute('data-id');
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

    console.log(clientId);

    fetch('/boletim-fluid/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            id: clientId,
            date_1: date1Value,
            date_2: date2Value
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            function getColorForLabel(label) {
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
            
            const labelsAmostras = data.t_coletas.map(item => item[1]);
            const dataValuesAmostras = data.t_coletas.map(item => item[2]);
        
            var $chartElementAmostras = $('#bar-chart-amostras');
            var existingChart = $chartElementAmostras.data('chart');
            if (existingChart) {
                // Se o gráfico já existe, apenas atualize os dados e o re-renderize.
                existingChart.data.labels = labelsAmostras;
                existingChart.data.datasets[0].data = dataValuesAmostras;
                existingChart.update();
            } else {
                // Se não, inicialize um novo gráfico.
                initChartbar($chartElementAmostras, labelsAmostras, dataValuesAmostras);
            }

            const labelsPontos = Object.keys(data.pontos);
            const barColors = labelsPontos.map(getColorForLabel);
            const dataValuesPontos = Object.values(data.pontos);
        
            var $chartElementPontos = $('#bar-chart-pontos');
            var existingChart = $chartElementPontos.data('chart');
            if (existingChart) {
                // Se o gráfico já existe, apenas atualize os dados e o re-renderize.
                existingChart.data.labels = labelsPontos;
                existingChart.data.datasets[0].data = dataValuesPontos;
                existingChart.data.datasets[0].backgroundColor = barColors;  // Definindo as cores aqui
                existingChart.update();
            } else {
                // Se não, inicialize um novo gráfico.
                initChartbar($chartElementPontos, labelsPontos, dataValuesPontos, barColors);
            }
        

        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
