function getRandomColor() {
        const r = Math.floor(Math.random() * 256);
        const g = Math.floor(Math.random() * 256);
        const b = Math.floor(Math.random() * 256);
        return `rgb(${r}, ${g}, ${b})`;
    }

function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}
document.addEventListener('DOMContentLoaded', function() {
    const placeholderSelect = document.getElementById('id_placeholder');

    placeholderSelect.addEventListener('change', function() {
        const selectedClientId = this.value;

        if (!selectedClientId) return;

        fetch('/dash-ada/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ 
                id_cliente: selectedClientId 
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
        function buildDatasets(hidrauliocData) {
            let categorizedData = {};
            let allDates = new Set();

            hidrauliocData.forEach(entry => {
                let sensorId = entry[0];
                let date = entry[1];
                allDates.add(date);

                if (!categorizedData[sensorId]) {
                    categorizedData[sensorId] = [];
                }
                categorizedData[sensorId].push(entry);
            });

            let sortedDates = [...allDates].sort();

            let datasets = [];
            for (let sensorId in categorizedData) {
                let dataMap = new Map(categorizedData[sensorId].map(entry => [entry[1], entry[2]]));
                let dataValues = sortedDates.map(date => dataMap.get(date) || null);

                let randomColor = getRandomColor();

                datasets.push({
                    label: `Sensor: ${sensorId}`,
                    data: dataValues,
                    backgroundColor: randomColor,
                    borderColor: randomColor,
                    borderWidth: 1
                });
            }

            return { datasets, sortedDates };
        }

        let { datasets, sortedDates } = buildDatasets(data.hidraulioc.mvn_hydraulic_load);
        let ctx = $('#carga_hidraulica');
        initChartLine(ctx, sortedDates, datasets, false);

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
        
        function buildDatasetss(pressaoData) {
            let categorizedData = {};
            let allDates = new Set();
        
            pressaoData.forEach(entry => {
                let serialNumber = entry[0];
                let date = entry[1];
                allDates.add(date);
        
                if (!categorizedData[serialNumber]) {
                    categorizedData[serialNumber] = [];
                }
                categorizedData[serialNumber].push(entry);
            });
        
            let sortedDatess = [...allDates].sort();
        
            let datasetss = [];
            for (let serialNumber in categorizedData) {
                let dataMap = new Map(categorizedData[serialNumber].map(entry => [entry[1], entry[2]]));
                let dataValues = sortedDatess.map(date => dataMap.get(date) || null);
        
                let randomColor = getRandomColor();
        
                datasetss.push({
                    label: `Serial Number: ${serialNumber}`,
                    data: dataValues,
                    backgroundColor: randomColor,
                    borderColor: randomColor,
                    borderWidth: 1
                });
            }
        
            return { datasetss, sortedDatess };
        }

        
        let { datasetss, sortedDatess } = buildDatasetss(data.pressao);
        let ctxx = $('#serie_pressao');
        initChartLine(ctxx, sortedDatess, datasetss, false, false);
        
        
    })
    .catch(error => {
        console.error('Erro ao enviar o sectorId:', error);
    });
}