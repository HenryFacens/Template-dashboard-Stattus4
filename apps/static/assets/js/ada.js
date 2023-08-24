
var map = L.map('map').setView([-23.46958528542014, -47.417883846037455], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var markersGroup = L.layerGroup().addTo(map);

var cal = new CalHeatMap();
cal.init({
    domain: 'month',
    subDomain: 'x_day',
    range: 3,
    cellSize: 15,
    verticalOrientation: true,
    subDomainTextFormat: '%d',
    legendVerticalPosition: 'center',
    legendHorizontalPosition: 'right',
    legendOrientation: 'vertical',
    legendMargin: [0, 0, 0, 20],
});

// pegada do Cookie para aprovacao do CSRFToken
function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

// pegada dos clietes
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
            // passar os Setores para a tabela
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

// posSetores

function sendSectorIdToBackend(sectorId) {
    fetch('/dash-ada/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ sectorId: sectorId })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // mapaConectividade  
        markersGroup.clearLayers();

        data.devices.forEach(device => {
            var marker = L.marker([device.lat, device.long])
                .bindPopup(`<b>ID do Dispositivo:</b> ${device.device_id}<br>
                            <b>Tipo:</b> ${device.type}<br>
                            <b>Número de série:</b> ${device.serial_number}`)
                .openPopup();

            markersGroup.addLayer(marker);
        });


        if (data.devices.length > 0) {
            var lastDevice = data.devices[data.devices.length - 1];
            map.setView([lastDevice.lat, lastDevice.long], 13); // 13 é o nível de zoom, ajuste conforme necessário
        }


    })
    .catch(error => {
        console.error('Erro ao enviar o sectorId:', error);
    });
}