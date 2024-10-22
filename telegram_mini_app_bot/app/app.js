function registerUser() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const registrationData = {
        username: username,
        email: email,
        password: password
    };

    fetch("https://ваш_туннель.trycloudflare.com/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(registrationData)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Пользователь зарегистрирован:", data);
            alert("Регистрация прошла успешно!");
        })
        .catch(error => console.error("Ошибка:", error));
}

function submitOnboarding() {
    const startupNameValue = document.getElementById("startup-name").value;
    const problemSolvingValue = document.getElementById("problem-solving").value;

    const formData = {
        startupName: startupNameValue,
        problemSolving: problemSolvingValue
    };

    console.log("Данные формы:", formData);

    // Отправка данных на сервер через Cloudflare Tunnel
    fetch("https://ваш_туннель.trycloudflare.com/submit_data", {
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
