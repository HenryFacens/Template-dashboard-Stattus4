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

        const cliente = data.context.sector_names;
        document.getElementById('cliente').textContent = cliente;

        const firstDate = data.context.date_1;
        const lastDate  = data.context.date_2;

        document.getElementById('firstDate2').textContent = firstDate;
        document.getElementById('lastDate2').textContent = lastDate;


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

        let { datasets, sortedDates } = buildDatasets(data.context.hidraulioc.mvn_hydraulic_load);
        let ctx = $('#grafico_hidraulic');
        initChartLine(ctx, sortedDates, datasets, false);
        
        function buildDatasetss(pressaoData) {
            let categorizedData = {};
            let allDates = new Set();
        
            pressaoData.forEach(entry => {
                let serialNumber = entry[0];
                let date = formatDate(entry[1]); // Use the formatDate function here
                allDates.add(date);
            
                if (!categorizedData[serialNumber]) {
                    categorizedData[serialNumber] = [];
                }
                categorizedData[serialNumber].push([serialNumber, date, entry[2]]);
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

        
        let { datasetss, sortedDatess } = buildDatasetss(data.context.pressao);
        let ctxx = $('#grafico_press');
        initChartLine(ctxx, sortedDatess, datasetss, false, false);

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

        const $chartElement = document.getElementById("grafico_alarmes");  // Assuming you have a canvas element with this ID.
        initChartpie($chartElement, labels, datass, colors, false, "Vazamentos", "bottom");



    } catch (error) {
        console.log('Fetch error: ', error);
    }
}

fetchData();
