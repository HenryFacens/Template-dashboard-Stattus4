    // mapaConectividade 
    var comunicouIcon = L.icon({
        iconUrl: '/static/assets/img/stattus4/pins_mapa/pinVerde.6717c697.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });

    var naoComunicouIcon = L.icon({
        iconUrl: '/static/assets/img/stattus4/pins_mapa/pinVermelho.3da980e7.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });

    var intermediarioIcon = L.icon({
        iconUrl: '/static/assets/img/stattus4/pins_mapa/pinAmarelo.9872369c.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });
    var cal = new CalHeatMap();
    cal.init({
        start: new Date(),  // Inicia no mês atual
        domain: "month",  // Mostra um mês de cada vez
        subDomain: "x_day",  // Divide o mês em dias
        range: 1,  // Mostra apenas um mês
        cellSize: 15,  // Tamanho das células (ajuste conforme necessário)
        verticalOrientation: false,  // Orientação horizontal
        subDomainTextFormat: '%d',
        domainGutter: 10,  // Espaço entre os domínios
        domainMargin: [0, 0, 0, 0],  // Margem ao redor do domínio
        displayLegend: false,  // Oculta a legenda (ajuste conforme necessário)
        considerMissingDataAsZero: true,  // Dados ausentes são considerados como zero
        data: {},
        // Cores para 0 (não comunicou) e 1 (comunicou)
        colLimit: 2,
        legend: [1],
        legendColors: {
            min: "gray",
            max: "#00ff00",
            empty: "red"
        },
    });


// Iniciacao do Mapa
var map = L.map('map').setView([-23.46958528542014, -47.417883846037455], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var markersGroup = L.layerGroup().addTo(map);


// pegada do Cookie para aprovacao do CSRFToken
function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

// Get Custumers
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
        var markersBySerial = {};  // Dicionário para armazenar marcadores por serial_number

        console.log(data);
        markersGroup.clearLayers();
        
        // Retorna a data mais recente de comunicação de um dispositivo
        function getLatestCommunicationDate(communications) {
            const dates = Object.keys(communications);
            const latestDate = dates.sort((a, b) => new Date(b) - new Date(a))[0]; // Ordena do mais recente para o mais antigo e pega o mais recente
            return new Date(latestDate);
        }
        data.devices.forEach(device => {
            var markerIcon;

            // Encontra a correspondente taxa média de comunicação para o dispositivo atual
            var deviceConn = data.devices_conn.find(conn => conn.device_id === device.device_id);

            if (deviceConn && Object.keys(deviceConn.communications).length) {
                const latestDate = getLatestCommunicationDate(deviceConn.communications);
                const currentDate = new Date();
                const timeDifference = currentDate - latestDate; // Diferença em milissegundos
                const oneDay = 24 * 60 * 60 * 1000; // 24 horas em milissegundos
                const sevenDays = 7 * oneDay; // 7 dias em milissegundos

                if (timeDifference <= oneDay) {
                    markerIcon = comunicouIcon; // Comunicou nas últimas 24 horas
                } else if (timeDifference <= sevenDays) {
                    markerIcon = intermediarioIcon; // Comunicou entre 24 horas e 7 dias
                } else {
                    markerIcon = naoComunicouIcon; // Não comunica há mais de 7 dias
                }
            } else {
                markerIcon = naoComunicouIcon; // Se não houver dados de comunicação
            }
            var marker = L.marker([device.lat, device.long], { icon: markerIcon })
            .bindPopup(`<b>ID do Dispositivo:</b> ${device.device_id}<br>
                        <b>Tipo:</b> ${device.type}<br>
                        <b>Número de série:</b> ${device.serial_number}`)
            .openPopup();
        
        markersBySerial[device.serial_number] = marker;  // Adiciona o marcador ao dicionário usando serial_number como chave

                marker.on('click', function() {
                    const deviceConn = data.devices_conn.find(conn => conn.device_id === device.device_id);
                    let heatmapData = {};
                    
                    // Preenche todos os últimos 7 dias com 0 por padrão
                    for (let i = 0; i < 7; i++) {
                        const date = new Date(new Date().getTime() - i * 24 * 60 * 60 * 1000);
                        const formattedDate = date.toISOString().split('T')[0];
                        heatmapData[new Date(formattedDate).getTime() / 1000] = 0;
                    }
                    
                    if (deviceConn) {
                        for (let date in deviceConn.communications) {
                            heatmapData[new Date(date).getTime() / 1000] = deviceConn.communications[date] > 0 ? 1 : 0;
                        }
                    }
                    
                    // Atualiza o Cal-Heatmap com os novos dados
                    cal.update(heatmapData);
                });

            markersGroup.addLayer(marker);
        });

        if (data.devices.length > 0) {
            var lastDevice = data.devices[data.devices.length - 1];
            map.setView([lastDevice.lat, lastDevice.long], 13); // 13 é o nível de zoom, ajuste conforme necessário
        }
        // Ordena os dispositivos por avg_conn_rate do menor para o maior
        data.devices_conn.sort((a, b) => a.avg_conn_rate - b.avg_conn_rate);

        // Pega o elemento tbody da tabela
        const tbody = document.querySelector("#clientTableBelowHeatmap tbody");

        // Limpa o tbody (caso já contenha linhas)
        tbody.innerHTML = "";

        function centerMapOnDevice(serial) {
            const marker = markersBySerial[serial];
            if(marker) {
                map.setView(marker.getLatLng(), 17);  // 17 é um nível de zoom mais aproximado, ajuste conforme necessário
                marker.openPopup();  // Abre o pop-up do marcador
            }
        }
        // Para cada dispositivo, cria uma linha na tabela
        data.devices_conn.forEach(device => {
            // Cria elementos tr e td
            const tr = document.createElement('tr');
            const tdSerial = document.createElement('td');
            const tdAvgConnRate = document.createElement('td');

            // Preenche os td com serial_number e avg_conn_rate
            tdSerial.textContent = device.serial_number;
            tdAvgConnRate.textContent = device.avg_conn_rate.toFixed(2);  // Ajusta para mostrar apenas 2 casas decimais
            
            // Adiciona um evento de clique ao tdSerial
            tdSerial.addEventListener('click', () => {
                centerMapOnDevice(device.serial_number, data.devices);
            });

            // Adiciona os td ao tr e o tr ao tbody
            tr.appendChild(tdSerial);
            tr.appendChild(tdAvgConnRate);
            tbody.appendChild(tr);
        });

            })
            .catch(error => {
                console.error('Erro ao enviar o sectorId:', error);
            });
        }

