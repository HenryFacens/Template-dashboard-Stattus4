



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

        const labels = data.t_coletas.map(item => item[1]);
        const dataValues = data.t_coletas.map(item => item[2]);
        
        var $chart = $('#bar-chart');
        if ($chart.length) {

        initChart($chart, labels, dataValues);
        
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

