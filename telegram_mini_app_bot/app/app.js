// app/app.js
function submitOnboarding() {
    // Получаем данные из полей формы по их идентификаторам
    const startupNameValue = document.getElementById("startup-name").value;
    const problemSolvingValue = document.getElementById("problem-solving").value;

    // Формируем объект данных
    const formData = {
        startupName: startupNameValue,
        problemSolving: problemSolvingValue
    };

    // Проверяем, что данные захватываются корректно
    console.log("Данные формы:", formData);

    // Отправляем POST-запрос на сервер через публичный URL, предоставленный Tuna
    fetch("https://hylsmk-31-180-193-247.ru.tuna.am/submit_data", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)  // Преобразуем объект в JSON перед отправкой
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
