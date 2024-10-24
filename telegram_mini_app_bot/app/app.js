// Функция для входа пользователя
function signInUser() {
    const tg_id = document.getElementById("tg_id").value;

    fetch(`${TUNNEL_URL}/sign_in`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ tg_id: tg_id })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("User signed in:", data);
            alert("Sign in successful!");

            // Перенаправление на страницу в зависимости от роли пользователя
            if (data.role === "co_builder") {
                location.href = "co_builder.html";
            } else if (data.role === "founder") {
                location.href = "founder.html";
            } else {
                alert("Role not found");
            }
        })
        .catch(error => console.error("Error:", error));
}
