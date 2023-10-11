function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}
document.addEventListener('DOMContentLoaded', function() {
    const placeholderSelect = document.getElementById('id_placeholder');

    placeholderSelect.addEventListener('change', function() {
        const selectedClientId = this.value;
        const selectedClientName = this.options[this.selectedIndex].getAttribute('data-nome');

        if (!selectedClientId || !selectedClientName) return;

        fetch('/boletim-ada/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ 
                id_cliente: selectedClientId,
                nome_cliente: selectedClientName
                })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            const sectorIds = data.sector_names.map(item => item.sectorId);
            sendSectorIdToBackend(sectorIds)
            
        })
        .catch(error => {
            console.error('Erro ao enviar o ID do cliente:', error);
        });
    });
});

function sendSectorIdToBackend(sectorId) {
    var date1Value = document.getElementById('id_date_1').value;
    var date2Value = document.getElementById('id_date_2').value;
    console.log(date1Value)
    fetch('/boletim-ada/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ sectorId: sectorId,
                                date_1: date1Value,
                                date_2: date2Value
                                })
    })
    .then(response => response.json())
    .then(data => {console.log(data)
        

        let vazamentoCount = 0;
        let faltaAguaCount = 0;
        let fechamentoRegistroCount = 0;
        let misturaSetorCount = 0;
        let suspeitaFraudeCount = 0;
        let reparoVazamentoCount = 0;

        // Contar os alarmes de cada tipo
        data.alarmes.forEach(alarm => {
            switch (alarm.alarmTypeName) {
                case "Vazamento":
                    vazamentoCount++;
                    break;
                case "Falta de Água":
                    faltaAguaCount++;
                    break;
                case "Fechamento de registro de rede":
                    fechamentoRegistroCount++;
                    break;
                case "Mistura de setor":
                    misturaSetorCount++;
                    break;
                case "Suspeita de fraude ou usos não medidos":
                    suspeitaFraudeCount++;
                    break;
                case "Reparo de vazamento":
                    reparoVazamentoCount++;
                    break;
            }
        });

        // Definindo a variável alarmDataCells
        const alarmDataCells = document.querySelectorAll("#alarmData td p");

        // Atualizar a tabela com os totais
        alarmDataCells[0].textContent = vazamentoCount;
        alarmDataCells[1].textContent = faltaAguaCount;
        alarmDataCells[2].textContent = fechamentoRegistroCount;
        alarmDataCells[3].textContent = misturaSetorCount;
        alarmDataCells[4].textContent = suspeitaFraudeCount;
        alarmDataCells[5].textContent = reparoVazamentoCount;
        
        // Suponha que você tenha recebido 'data.communication' do lado do servidor:
        var communicationData = data.comunication;

        // Processar os dados:
        var labels = [];
        var dataValues = [];
        var colors = [];

        for (var key in communicationData) {
            dataValues.push(key);
            labels.push(communicationData[key]);
            if (communicationData[key] === "Comunicou") {
                colors.push('green');
            } else if (communicationData[key] === "Nao Comunicou") {
                colors.push('red');
            } else {
                colors.push('blue');
            }
        }

        // Inicializar o gráfico:
        var $chartElement = $("#conexao_dispositivos");  // Substitua pelo ID do seu elemento de gráfico
        initChartbar($chartElement, labels, dataValues, colors, false, 'Comunicação');

    })
    .catch(error => {
        console.error('Erro ao enviar o sectorId:', error);
    });
}