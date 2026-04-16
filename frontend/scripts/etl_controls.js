


async function getAPI(task) {

    const endpoint = "http://localhost:5000/".concat(task)
    return(endpoint)
}

document.getElementById("startETL").addEventListener("click", async () => {
    const url = await getAPI("start-etl")
    
    const response = await fetch(url);
    const data = await response.json();

    console.log(data);
    alert(data.message);
});

document.getElementById("stopETL").addEventListener("click", async () => {
    const url = await getAPI("stop-etl")
    
    const response = await fetch(url);
    const data = await response.json();

    console.log(data);
    alert(data.message);
});

document.getElementById("clear_db").addEventListener("click", async () => {
    const url = await getAPI("clear-db")
    
    const response = await fetch(url);
    const data = await response.json();

    console.log(data);
    alert(data.message);
});

document.getElementById("resumeETL").addEventListener("click", async () => {
    const url = await getAPI("resume-etl")
    
    const response = await fetch(url);
    const data = await response.json();

    console.log(data);
    alert(data.message);
});