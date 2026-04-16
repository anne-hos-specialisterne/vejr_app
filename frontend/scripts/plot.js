 async function loadData() {
    const response = await fetch("http://localhost:8000/data");
    const data = await response.json();

    const times = data.map(d => d[5]);
    const values = data.map(d => d[6]);
    const trace = {
            x: times,
            y: values,
            mode: "lines+markers",
            type: "scatter"
        };

        const layout = {
            title: "Time vs Value",
            xaxis: { title: "Time" },
            yaxis: { title: "Value" },
            margin: { t: 40 }
        };

    Plotly.newPlot("plot", [trace], layout);
}

loadData();