document.getElementById("ingestForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    
    let formData = new FormData();
    formData.append("file", document.getElementById("file").files[0]);

    const response = await fetch("/ingest", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    alert(data.message);
});

document.getElementById("queryForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const query = document.getElementById("query").value;
    const response = await fetch(`/query?query=${query}`, {
        method: "GET",
    });

    const data = await response.json();
    document.getElementById("queryResults").innerHTML = JSON.stringify(data.query_results, null, 2);
});
