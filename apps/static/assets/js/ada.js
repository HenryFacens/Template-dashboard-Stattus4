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
            console.log(data);
            const tableBody = document.getElementById('clientTable').querySelector('tbody');
            tableBody.innerHTML = '';  // limpa as linhas existentes
        
data.sector_names.forEach(sector => {
    const row = tableBody.insertRow();
    const cellSectorName = row.insertCell(0);
    
    // Criando um elemento button com a classe btn-link
    const sectorButton = document.createElement('button');
    sectorButton.textContent = sector.sectorName;
    sectorButton.classList.add('btn', 'btn-link', 'clickable-sector');
    sectorButton.dataset.sectorId = sector.sectorId;
    
    // Adiciona o event listener para lidar com o clique
    sectorButton.addEventListener('click', function() {
        sendSectorIdToBackend(this.dataset.sectorId);
    });
    
    // Adiciona o button na célula da tabela
    cellSectorName.appendChild(sectorButton);
});
            
        })
        .catch(error => {
            console.error('Erro ao enviar o ID do cliente:', error);
        });
    });
});

function sendSectorIdToBackend(sectorId) {
    fetch('/dash-ada/', {  // Substitua '/sua-url-aqui/' pela URL do backend que deve receber o sectorId
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
    })
    .catch(error => {
        console.error('Erro ao enviar o sectorId:', error);
    });
}