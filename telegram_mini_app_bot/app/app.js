// Function to sign in the user
async function signInUser() {
    const tg = window.Telegram.WebApp;
    const tgUser = tg.initDataUnsafe.user;

    if (!tgUser) {
        alert('Please open this page in Telegram Mini App.');
        return;
    }

    const tg_id = tgUser.id;
    const TUNNEL_URL = window.TUNNEL_URL;

    if (!TUNNEL_URL) {
        console.error("TUNNEL_URL is not defined.");
        alert("Internal error. Please try again later.");
        return;
    }

    try {
        const response = await fetch(`${TUNNEL_URL}/sign_in`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ tg_id })
        });

        console.log("Response status:", response.status);
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(`${response.status}: ${errData.detail}`);
        }

        const data = await response.json();
        console.log("User signed in:", data);
        alert("Sign in successful!");

        // Redirect based on user role
        redirectUser(data.role);
    } catch (error) {
        console.error("Error:", error);
        alert(`An error occurred: ${error.message}`);
    }
}

// Function to register a new user
async function registerUser() {
    const tg = window.Telegram.WebApp;
    const tgUser = tg.initDataUnsafe.user;

    if (!tgUser) {
        alert('Please open this page in Telegram Mini App.');
        return;
    }

    const tg_id = tgUser.id;
    const first_name = document.getElementById('first-name').value.trim();
    const last_name = document.getElementById('last-name').value.trim();
    const email = document.getElementById('email').value.trim();
    const role = document.getElementById('role').value.trim();
    const TUNNEL_URL = window.TUNNEL_URL;

    if (!TUNNEL_URL) {
        console.error("TUNNEL_URL is not defined.");
        alert("Internal error. Please try again later.");
        return;
    }

    // Validate input fields
    if (!first_name || !last_name || !email || !role) {
        alert("Please fill in all fields.");
        return;
    }

    try {
        const response = await fetch(`${TUNNEL_URL}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                tg_id,
                first_name,
                last_name,
                email,
                role
            })
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(`${response.status}: ${errData.detail}`);
        }

        const data = await response.json();
        console.log("User registered:", data);
        alert("Registration successful!");

        // Redirect based on user role
        redirectUser(role);
    } catch (error) {
        console.error("Error:", error);
        alert(`An error occurred: ${error.message}`);
    }
}

// Function to redirect users based on their role
function redirectUser(role) {
    switch (role) {
        case "co_builder":
            location.href = "/co_builder";
            break;
        case "founder":
            location.href = "/founder";
            break;
        default:
            alert("Role not found");
            break;
    }
}

// Adding TUNNEL_URL to global scope for use in other scripts
document.addEventListener("DOMContentLoaded", () => {
    window.TUNNEL_URL = "{{ TUNNEL_URL }}";
});