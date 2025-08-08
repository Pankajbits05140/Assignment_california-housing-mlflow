document.getElementById("predictForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        MedInc: parseFloat(document.getElementById("MedInc").value),
        HouseAge: parseFloat(document.getElementById("HouseAge").value),
        AveRooms: parseFloat(document.getElementById("AveRooms").value),
        AveBedrms: parseFloat(document.getElementById("AveBedrms").value),
        Population: parseFloat(document.getElementById("Population").value),
        AveOccup: parseFloat(document.getElementById("AveOccup").value),
        Latitude: parseFloat(document.getElementById("Latitude").value),
        Longitude: parseFloat(document.getElementById("Longitude").value)
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        if (result.prediction !== undefined) {
            document.getElementById("result").innerHTML = `Predicted Median House Value: <b>${result.prediction.toFixed(3)}</b>`;
        } else {
            document.getElementById("result").innerHTML = `Error: ${result.error || "Unknown error"}`;
        }
    } catch (error) {
        document.getElementById("result").innerHTML = `Request failed: ${error}`;
    }
});