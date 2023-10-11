function getRandomColor() {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return `rgb(${r}, ${g}, ${b})`;
}
function formatDate(inputDate) {
    let date = new Date(inputDate);
    let year = date.getUTCFullYear();
    let month = (date.getUTCMonth() + 1).toString().padStart(2, '0'); // padStart ensures we get '01' instead of '1'
    let day = date.getUTCDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
}

async function fetchData() {
    const url = '/boletim_json_ada/';

    try {
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log(data);

        const cliente = data.context.client_name;
        document.getElementById('cliente').textContent = cliente;

        const firstDate = data.context.date_1;
        const lastDate  = data.context.date_2;

        document.getElementById('firstDate2').textContent = firstDate;
        document.getElementById('lastDate2').textContent = lastDate;
        

        document.querySelectorAll(".color-box").forEach(box => {
            box.style.backgroundColor = box.getAttribute("data-color");
        });

        let vazamentoCount = 0;
        let faltaAguaCount = 0;
        let fechamentoRegistroCount = 0;
        let misturaSetorCount = 0;
        let suspeitaFraudeCount = 0;
        let reparoVazamentoCount = 0;

        data.context.alarmes.forEach(alarm => {
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

        const alarmDataCells = document.querySelectorAll("#tabela-valores-pontos td:nth-child(2)");

        alarmDataCells[0].textContent = vazamentoCount;
        alarmDataCells[1].textContent = faltaAguaCount;
        alarmDataCells[2].textContent = fechamentoRegistroCount;
        alarmDataCells[3].textContent = misturaSetorCount;
        alarmDataCells[4].textContent = suspeitaFraudeCount;
        alarmDataCells[5].textContent = reparoVazamentoCount;

        const labels = [
            "Vazamento",
            "Falta de Água",
            "Fechamento de registro de rede",
            "Mistura de setor",
            "Suspeita de fraude ou usos não medidos",
            "Reparo de vazamento"
        ];
        
        const datass = [
            vazamentoCount,
            faltaAguaCount,
            fechamentoRegistroCount,
            misturaSetorCount,
            suspeitaFraudeCount,
            reparoVazamentoCount
        ];
        const colors = [
            "#FF5733",  // Color for Vazamento
            "#33FF57",  // Color for Falta de Água
            "#5733FF",  // Color for Fechamento de registro de rede
            "#FF33A1",  // Color for Mistura de setor
            "#33A1FF",  // Color for Suspeita de fraude ou usos não medidos
            "#A133FF"   // Color for Reparo de vazamento
        ];

        const $chartElement = $("#grafico_alarmes");  // Assuming you have a canvas element with this ID.
        console.log("TESTE")

        initChartpie($chartElement, labels, datass, colors, false, "Vazamentos", "bottom");

        var communicationData = data.context.comunication;

        var $chartElemente = $("#grafico_quantidades");  // Substitua pelo ID do seu elemento de gráfico
        // Processar os dados:
        var labelss = [];
        var dataValues = [];
        var colorss = [];

        for (var key in communicationData) {
            dataValues.push(key);
            labelss.push(communicationData[key]);
            if (communicationData[key] === "Comunicou") {
                colorss.push('green');
            } else if (communicationData[key] === "Nao Comunicou") {
                colorss.push('red');
            } else {
                colorss.push('blue');
            }
        }

        // Selecione o elemento do gráfico:

        // Verifique se o gráfico já foi inicializado:
        var existingChart = $chartElemente.data('chart');

        if (existingChart) {
            // Atualize os dados do gráfico existente:
            existingChart.data.labels = labelss;
            existingChart.data.datasets[0].data = dataValues;
            existingChart.data.datasets[0].backgroundColor = colorss;
            existingChart.data.datasets[0].borderColor = colorss;
            existingChart.update();
        } else {
            // Inicialize o gráfico:
            initChartbar($chartElemente, labelss, dataValues, colorss, true, ' ');
        }
        
        var totalDevicesKey = Object.keys(communicationData).find(key => communicationData[key] === "Total de Dispositivos");
        var totalDevices = totalDevicesKey;
        
        document.getElementById("pontos").value = totalDevices;
        


    } catch (error) {
        console.log('Fetch error: ', error);
    }
}

fetchData();
