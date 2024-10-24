// telegram_mini_app_bot/app/app.js

// Function to sign in the user
function signInUser() {
    const tg = window.Telegram.WebApp;
    const tgUser = tg.initDataUnsafe.user;

    if (!tgUser) {
        alert('Please open this page in Telegram Mini App.');
        return;
    }

    const tg_id = tgUser.id;

    fetch(`${TUNNEL_URL}/sign_in`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({tg_id: tg_id})
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

            // Redirect based on user role
            if (data.role === "co_builder") {
                location.href = "/co_builder";
            } else if (data.role === "founder") {
                location.href = "/founder";
            } else {
                alert("Role not found");
            }
        })
        .catch(error => console.error("Error:", error));
}

// Function to register a new user
function registerUser() {
    const tg = window.Telegram.WebApp;
    const tgUser = tg.initDataUnsafe.user;

    if (!tgUser) {
        alert('Please open this page in Telegram Mini App.');
        return;
    }

    const tg_id = tgUser.id;
    const first_name = document.getElementById('first-name').value;
    const last_name = document.getElementById('last-name').value;
    const email = document.getElementById('email').value;
    const role = document.getElementById('role').value;

    fetch(`${TUNNEL_URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            tg_id: tg_id,
            first_name: first_name,
            last_name: last_name,
            email: email,
            role: role
        })
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

            // Redirect based on user role
            if (role === "co_builder") {
                location.href = "/co_builder";
            } else if (role === "founder") {
                location.href = "/founder";
            } else {
                alert("Role not found");
            }
        })
        .catch(error => console.error("Error:", error));
}
