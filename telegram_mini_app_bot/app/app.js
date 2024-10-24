let TUNNEL_URL = "";

// Функция для получения TUNNEL_URL с сервера
function loadTunnelUrl() {
    return fetch("/get_tunnel_url")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            TUNNEL_URL = data.tunnel_url;
        })
        .catch(error => console.error("Error loading TUNNEL_URL:", error));
}

// Функция для регистрации пользователя
function registerUser() {
    const email = document.getElementById("email").value;
    const firstName = document.getElementById("first-name").value;
    const lastName = document.getElementById("last-name").value;
    const role = document.getElementById("role").value;

    const registrationData = {
        email: email,
        first_name: firstName,
        last_name: lastName,
        role: role
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
                throw new Error(`HTTP Error: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("User registered:", data);
            alert("Registration successful!");

            // Переход на страницу в зависимости от роли пользователя
            if (role === "co_builder") {
                location.href = "co_builder.html";
            } else {
                location.href = "founder.html";
            }
        })
        .catch(error => console.error("Error:", error));
}

// Загружаем URL туннеля перед началом работы
window.onload = function () {
    loadTunnelUrl().then(() => {
        console.log("TUNNEL_URL loaded:", TUNNEL_URL);
    });
};