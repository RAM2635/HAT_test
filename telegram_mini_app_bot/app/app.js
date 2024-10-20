function startOnboarding() {
    // Пример функции для запуска процесса онбординга
    console.log("Онбординг начат...");

    // Пример отправки данных на backend
    fetch("http://localhost:8000/submit_data", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({step: "initial"})  // данные для отправки на backend
    })
        .then(response => response.json())
        .then(data => {
            console.log("Ответ от backend:", data);
            // Можно добавить логику для отображения следующего шага на основе данных
        })
        .catch(error => console.error("Ошибка:", error));
}
