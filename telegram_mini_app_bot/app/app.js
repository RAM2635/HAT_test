// app/app.js
function submitOnboarding() {
    const formData = {
        startupName: document.getElementById("startup-name").value,
        problemSolving: document.getElementById("problem-solving").value
    };

    // Используем публичный URL от Cloudflare Tunnel
    fetch("https://dramatically-therapeutic-academy-ef.trycloudflare.com/submit_data", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Ответ от backend:", data);
            alert("Данные успешно отправлены!");
        })
        .catch(error => console.error("Ошибка:", error));
}
