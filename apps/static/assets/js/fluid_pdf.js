async function fetchData() {
    const url = '/boletim_json/';

    try {
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        console.log(data); // Aqui, você pode processar os dados conforme necessário

        const cliente = data.context.clientNm;
        document.getElementById('cliente').textContent = cliente;
        
        const firstDate = data.context.date_1;
        const lastDate  = data.context.date_2;

        document.getElementById('firstDate2').textContent = firstDate;
        document.getElementById('lastDate2').textContent = lastDate;

        //Grafico de barras
        const t_coletas = data.context.t_coletas;
        const labelsbar = t_coletas.map(item => item[1]);
        const databar = t_coletas.map(item => item[2]);

        const colorsbar = databar.map(() => 'rgba(54, 162, 235, 0.2)');

        const $chartElement = $("#grafico_barras_coletas");
        initChartbar($chartElement, labelsbar, databar, colorsbar, true,'Coleta');
        
        //Grafico de pizza
        const labelsClasses = ['Fraude', 'Inconsistente', 'Ponto Suspeito', 'Sem Vazamento', 'Sem Acesso', 'Consumo', 'Pendente', 'Vazamento Visível'];
        const dataPieRaw = data.context.classes[0];  // Considerando que este é o seu conjunto de dados
        const [, ...dataPie] = dataPieRaw;  // Usando desestruturação para ignorar o primeiro elemento e pegar o restante
        console.log(dataPie);
        const barColorsClasses = labelsClasses.map(getColorForLabelClasses);
        
        const $chartPieElement = $("#grafico_pizza_amostras");  // Lembre-se de atualizar com o ID correto do seu elemento canvas
        initChartpie($chartPieElement, labelsClasses, dataPie, barColorsClasses, 'Coleta', true, 'right');
        updateTableWithValues(labelsClasses, dataPie);
        
        //Acuracia
        const pontos = data.context.pontos;
        const dataBar = {
            "Ponto Não Confirmado": pontos["Ponto Não Confirmado"],
            "Pontos Confirmados": pontos["Pontos Confirmados"]
        };
        const labelspontos = Object.keys(dataBar);
        const valuespontos = Object.values(dataBar);
        const $chartBarElement = $("#grafico_barras_acuracia");
        const colorspontos = ['red', 'green'];
        initChartbar($chartBarElement, labelspontos, valuespontos, colorspontos, false);
        updateTable(dataBar);
        updatePendentesValue(pontos);


    } catch (error) {
        console.log('Fetch error: ', error);
    }
}

// Chamar a função para buscar os dados:
fetchData();

function updateTableWithValues(labels, values) {
    let tbody = document.getElementById("tabela-valores");
    tbody.innerHTML = ''; // Limpa o conteúdo atual da tbody

    // Insere cada label e valor na tabela
    labels.forEach((label, index) => {
        let row = tbody.insertRow();
        let cell1 = row.insertCell(0);
        let cell2 = row.insertCell(1);
        cell1.textContent = label;
        cell2.textContent = values[index];
    });

    // Calcula o total e insere na última linha
    let total = values.reduce((a, b) => a + b, 0);
    let row = tbody.insertRow();
    let cell1 = row.insertCell(0);
    let cell2 = row.insertCell(1);
    cell1.textContent = "Total";
    cell1.style.fontWeight = "bold"; // Faz o texto "Total" em negrito
    cell2.textContent = total;
}
function getColorForLabelClasses(label) {
    switch(label) {
        case 'Sem Vazamento':
            return 'rgba(0, 128, 0, 0.2)';
        case 'Ponto Suspeito':
            return 'rgba(255, 0, 0, 0.2)';
        case 'Fraude':
            return 'rgba(0, 0, 0, 0.2)';
        case 'Sem Acesso':
            return 'rgba(169, 169, 169, 0.2)';
        case 'Consumo':
            return 'rgba(54, 162, 235, 0.2)';
        case 'Inconsistente':
            return 'rgba(0, 0, 128, 1)';
        case 'Pendente':
            return 'rgba(255, 255, 0, 1)';
        case 'Vazamento Visível':
            return 'rgba(128, 0, 128, 0.2)'; 
        default:
            return 'black';
    }
}
function updateTable(dataBar) {
    const tbody = document.getElementById("tabela-valores-pontos");
    
    // Limpe o conteúdo atual do tbody
    tbody.innerHTML = "";
    
    const totalValues = Object.values(dataBar).reduce((a, b) => a + b, 0);

    for (const [label, value] of Object.entries(dataBar)) {
        const percentage = ((value / totalValues) * 100).toFixed(2) + '%';
        
        const row = tbody.insertRow();
        const cell1 = row.insertCell(0);
        const cell2 = row.insertCell(1);
        const cell3 = row.insertCell(2);

        cell1.innerText = label;
        cell2.innerText = value;
        cell3.innerText = percentage;
    }
}
function updatePendentesValue(pontos) {
    const pendentesElement = document.getElementById("pendentes_value");
    pendentesElement.textContent = pontos["Pendente"];
}