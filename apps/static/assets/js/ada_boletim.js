    // random colors    
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

            // passando os Setores para a tabela
            const tableBody = document.getElementById('clientTable').querySelector('tbody');
            tableBody.innerHTML = '';
        
            data.sector_names.forEach(sector => {
                const row = tableBody.insertRow();
                const cellSectorName = row.insertCell(0);
                
                const sectorButton = document.createElement('button');
                sectorButton.textContent = sector.sectorName;
                sectorButton.classList.add('btn', 'btn-link', 'clickable-sector');
                sectorButton.dataset.sectorId = sector.sectorId;
                
                sectorButton.addEventListener('click', function() {
                    sendSectorIdToBackend(this.dataset.sectorId); // Chamda da funcao para posSetores
                });
                
                cellSectorName.appendChild(sectorButton);

            });
            
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
        
        
    })
    .catch(error => {
        console.error('Erro ao enviar o sectorId:', error);
    });
}