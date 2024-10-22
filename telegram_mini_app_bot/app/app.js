let TUNNEL_URL = "";

// Функция для получения TUNNEL_URL с сервера
function loadTunnelUrl() {
    return fetch("/get_tunnel_url")
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            TUNNEL_URL = data.tunnel_url;
        })
        .catch(error => console.error("Ошибка загрузки TUNNEL_URL:", error));
}

// Функция регистрации пользователя
function registerUser() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const registrationData = {
        username: username,
        email: email,
        password: password
    };

    fetch(`${TUNNEL_URL}/register`, {
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

            // Показываем форму онбординга и скрываем форму регистрации
            document.getElementById("registration-form").style.display = "none";
            document.getElementById("onboarding-container").style.display = "block";
        })
        .catch(error => console.error("Ошибка:", error));
}

// Функция отправки данных онбординга
function submitOnboarding() {
    const startupNameValue = document.getElementById("startup-name").value;
    const problemSolvingValue = document.getElementById("problem-solving").value;

    const formData = {
        startupName: startupNameValue,
        problemSolving: problemSolvingValue
    };

    console.log("Данные формы:", formData);

    // Отправка данных на сервер через Cloudflare Tunnel
    fetch(`${TUNNEL_URL}/submit_data`, {
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

// Загружаем URL туннеля перед началом работы
window.onload = function () {
    loadTunnelUrl().then(() => {
        console.log("TUNNEL_URL загружен:", TUNNEL_URL);
    });
};
