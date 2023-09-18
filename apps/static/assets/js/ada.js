    // random colors    
    function getRandomColor() {
        const r = Math.floor(Math.random() * 256);
        const g = Math.floor(Math.random() * 256);
        const b = Math.floor(Math.random() * 256);
        return `rgb(${r}, ${g}, ${b})`;
    }

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
        start: new Date(new Date().getFullYear(), new Date().getMonth() - 1, 1), // Inicia no mês anterior
        domain: "month",
        subDomain: "x_day",
        range: 2,
        cellSize: 15,
        verticalOrientation: false,
        verticalOrientation: true,
        subDomainTextFormat: '%d',
        domainGutter: 10,
        domainMargin: [0, 0, 0, 0],
        displayLegend: false,
        considerMissingDataAsZero: true,
        data: {},
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
                    function hasNonNormalReason(deviceSerial, consistencia_dados) {
                        return (consistencia_dados[deviceSerial] && consistencia_dados[deviceSerial].reason !== "Valor normal");
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

                        // Supondo que você tem um elemento com o ID 'map' para o seu mapa:

                        var marker = L.marker([device.lat, device.long], { icon: markerIcon })
                        .bindPopup(`<b>ID do Dispositivo:</b> ${device.device_id}<br>
                                    <b>Tipo:</b> ${device.type}<br>
                                    <b>Número de série:</b> ${device.serial_number}
                                    <b>Lat:</b>${device.lat}<br>
                                    <b>Long:</b>${device.long}
                                    `)
                                    

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

                        if (hasNonNormalReason(device.serial_number, data.consistencia_dados)) {
                            // Posicione o ícone de exclamação próximo ao marcador principal.
                            // Ajuste o offset para posicionar o ícone exatamente onde você deseja.
                            const exclamationOffset = [10, 0];  // Por exemplo, 10 pixels à direita do marcador principal.
                            const exclamationPosition = [device.lat + exclamationOffset[0], device.long + exclamationOffset[1]];
                    
                            const exclamationIcon = L.icon({
                                iconUrl: '/static/assets/img/stattus4/pins_mapa/ponto-de-exclamacao.png',  // Substitua pelo caminho correto
                                iconSize: [25, 25],  // Ajuste o tamanho conforme necessário
                                iconAnchor: [0, 0]  // Posiciona o canto superior esquerdo do ícone sobre a localização do marcador.
                            });
                    
                            const exclamationMarker = L.marker(exclamationPosition, { icon: exclamationIcon });
                            markersGroup.addLayer(exclamationMarker);
                        }
                    });
                    
                    // Lista de dispositivos
                    function filterDatasetsBySerialNumber(serialNumber, datasets) {
                        return datasets.filter(dataset => dataset.label === `Sensor: ${serialNumber}`);
                    }
                    
                    
                    if (data.devices.length > 0) {
                        var lastDevice = data.devices[data.devices.length - 1];
                        map.setView([lastDevice.lat, lastDevice.long], 13);
                    }

                    data.devices_conn.sort((a, b) => a.avg_conn_rate - b.avg_conn_rate);

                    const tbody = document.querySelector("#clientTableBelowHeatmap tbody");

                    tbody.innerHTML = "";

                    function findDeviceInConn(serialNumber, devicesConn) {
                        return devicesConn.find(device => device.serial_number === serialNumber);
                    }

                    const addedSerials = new Set();

                    data.devices.forEach(device => {
                        if (addedSerials.has(device.serial_number)) {
                            return;
                        }

                        const tr = document.createElement('tr');
                        const tdSerial = document.createElement('td');
                        const tdAvgConnRate = document.createElement('td');
                        const tdConsistency = document.createElement('td');
                        const tdReason = document.createElement('td');
                        
                        tdSerial.textContent = device.serial_number;
                        
                        const deviceInConn = findDeviceInConn(device.serial_number, data.devices_conn);
                        
                        // Se encontrarmos o dispositivo em devices_conn, usamos seus dados. Caso contrário, usamos 0 como valor padrão.
                        if (deviceInConn) {
                            tdAvgConnRate.textContent = deviceInConn.avg_conn_rate.toFixed(2);
                        } else {
                            tdAvgConnRate.textContent = "0.00";  // Valor padrão se não estiver em devices_conn
                        }
                        
                        // Se o dispositivo tiver dados de consistência, usamos eles. Caso contrário, usamos valores padrão.
                        if (data.consistencia_dados[device.serial_number]) {
                            tdConsistency.textContent = data.consistencia_dados[device.serial_number].consistency;
                            tdReason.textContent = data.consistencia_dados[device.serial_number].reason;
                        } else {
                            tdConsistency.textContent = "Indisponível";
                            tdReason.textContent = "Sem dados";
                        }

                        // Adiciona um evento de clique ao tdSerial
                        tdSerial.addEventListener('click', () => {
                            centerMapOnDevice(device.serial_number);
                        });
                        
                        
                        // Adiciona os td ao tr e o tr ao tbody
                        tr.appendChild(tdSerial);
                        tr.appendChild(tdAvgConnRate);
                        tr.appendChild(tdConsistency);
                        tr.appendChild(tdReason);
                        tbody.appendChild(tr);

                        // Adiciona o serial_number ao conjunto de serial_numbers adicionados
                        addedSerials.add(device.serial_number);
                    });

                    // Função que constrói os datasets
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
                
                    
                    // ...
                    function centerMapOnDevice(serial) {
                        const marker = markersBySerial[serial];
                        if(marker) {
                            map.setView(marker.getLatLng(), 17);
                            marker.openPopup();
                        }
                    
                        let { datasets, sortedDates } = buildDatasets(data.hidraulioc.mvn_hydraulic_load);
                        const filteredDatasets = filterDatasetsBySerialNumber(serial, datasets);
                    
                        let ctx = $('#carga_hidraulica');
                        initChartLine(ctx, sortedDates, filteredDatasets, false);
                    }
                    
                                
                        })
                        .catch(error => {
                            console.error('Erro ao enviar o sectorId:', error);
                        });
                    }

