function normalizeString(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

// Função para filtrar nomes dos clientes e sub-clientes
function filterClients() {
    let filter = normalizeString(this.value);

    // Itera sobre todos os clientes
    document.querySelectorAll('.accordion > div').forEach(function(clientContainer) {
        let mainClientName = normalizeString(clientContainer.querySelector('[data-name]').getAttribute('data-name'));
        let subClients = clientContainer.querySelectorAll('.list-group-item');
        
        let hasSubClientMatch = false;

        subClients.forEach(function(subClient) {
            let subClientName = normalizeString(subClient.getAttribute('data-name'));

            if (subClientName.includes(filter)) {
                subClient.style.display = "";
                hasSubClientMatch = true;
            } else {
                subClient.style.display = "none";
            }
        });

        // Se o nome do cliente principal ou qualquer sub-cliente corresponder, mostre o cliente principal
        if (mainClientName.includes(filter) || hasSubClientMatch) {
            clientContainer.style.display = "";
        } else {
            clientContainer.style.display = "none";
        }
    });
}

// Adiciona evento para filtragem ao digitar
document.getElementById("clienteSearch").addEventListener("input", filterClients);

// Adiciona evento para evitar que Enter submeta o formulário
document.getElementById("clienteSearch").addEventListener('keydown', function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        return false;
    }
});


function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}
function sendClientId(element) {

    var clientId = element.getAttribute('data-id');
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
                initChartbar($chartElementAmostras, labelsAmostras, dataValuesAmostras,null ,false);
            }

            const labelsPontos = Object.keys(data.pontos);
            const barColorsPontos = labelsPontos.map(getColorForLabelPontos);
            const dataValuesPontos = Object.values(data.pontos);
        
            var $chartElementPontos = $('#bar-chart-pontos');
            var existingChart = $chartElementPontos.data('chart');
            if (existingChart) {
                // Se o gráfico já existe, apenas atualize os dados e o re-renderize.
                existingChart.data.labels = labelsPontos;
                existingChart.data.datasets[0].data = dataValuesPontos;
                existingChart.data.datasets[0].backgroundColor = barColorsPontos;  // Definindo as cores aqui
                existingChart.update();
            } else {
                // Se não, inicialize um novo gráfico.
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
            
            const [clientId, ...dataValuesClassesRaw] = data.classes[0];

            const labelsClasses = ['Fraude', 'Inconsistente', 'Ponto Suspeito', 'Sem Vazamento', 'Sem Acesso', 'Consumo', 'Pendente', 'Vazamento Visível'];
    
            // Como você não quer o ID do cliente, não precisamos mudar labelsClasses.
            const dataValuesClasses = dataValuesClassesRaw;
            const barColorsClasses = labelsClasses.map(getColorForLabelClasses);
    
            var $chartElementClasses = $('#pie-chart');
            var existingChart = $chartElementClasses.data('chart');
    
            // Função para criar rótulos com valores
            function generateLabelsWithValues(labels, data) {
                return labels.map(function(label, index) {
                    return label + " (" + data[index] + ")";
                });
            }

            // Dentro do fetch ou onde você lida com a atualização
            if (existingChart) {
                // Se o gráfico já existe, apenas atualize os dados e o re-renderize.
                existingChart.data.labels = generateLabelsWithValues(labelsClasses, dataValuesClasses);
                existingChart.data.datasets[0].data = dataValuesClasses;
                existingChart.data.datasets[0].backgroundColor = barColorsClasses;
                existingChart.update();
            } else {
                // Se não, inicialize um novo gráfico.
                initChartpie($chartElementClasses, labelsClasses, dataValuesClasses, barColorsClasses);
            }
        

        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
