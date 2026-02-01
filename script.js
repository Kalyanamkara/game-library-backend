


const API_URL = "https://game-library-backend-enzy.onrender.com"; 

let authToken = localStorage.getItem("token"); 
let allGames = []; 

document.addEventListener("DOMContentLoaded", () => {
    if (authToken) {
        toggleScreens(true);
        fetchGames();
    }
});



async function handleLogin() {
    const usernameInput = document.getElementById("username").value;
    const passwordInput = document.getElementById("password").value;

    const formData = new URLSearchParams();
    formData.append("username", usernameInput);
    formData.append("password", passwordInput);

    try {
        const response = await fetch(`${API_URL}/token`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            localStorage.setItem("token", authToken);
            
            document.getElementById("error-message").innerText = "";
            toggleScreens(true);
            fetchGames();
        } else {
            const errorText = await response.text();
            document.getElementById("error-message").innerText = "Giriş başarısız!";
        }
    } catch (error) {
        console.error("Login Error:", error);
        document.getElementById("error-message").innerText = "Bağlantı hatası!";
    }
}

function handleLogout() {
    localStorage.removeItem("token");
    authToken = null;
    toggleScreens(false);
}



async function handleRegister() {
    const regUser = document.getElementById("reg-username").value;
    const regPass = document.getElementById("reg-password").value;

    if (!regUser || !regPass) {
        document.getElementById("reg-error-message").innerText = "Please fill all fields";
        return;
    }

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: regUser, password: regPass })
        });

        if (response.ok) {
            alert("Registration Successful! Please Login.");
            showLoginScreen();
            document.getElementById("reg-username").value = "";
            document.getElementById("reg-password").value = "";
        } else {
            const errorText = await response.text();
            document.getElementById("reg-error-message").innerText = "Failed: " + errorText;
        }
    } catch (error) {
        document.getElementById("reg-error-message").innerText = "Connection Error";
    }
}


function renderGames(gameList) {
    const listContainer = document.getElementById("game-list");
    listContainer.innerHTML = ""; 

    if (gameList.length === 0) {
        listContainer.innerHTML = '<p style="color: #94a3b8; text-align: center; width: 100%;">No games found.</p>';
        return;
    }

    gameList.forEach(game => {
        
        const publisherName = game.yapımcı || game.yapimci || "Unknown";

        listContainer.innerHTML += `
            <div class="game-card">
                <h3>${game.isim}</h3>
                <p style="color:#94a3b8;">${game.tur}</p>
                <p><strong>Publisher:</strong> ${publisherName}</p>
                <div class="game-score">${game.puan} Puan</div>
                
                <div style="display: flex; gap: 10px; margin-top: 15px; justify-content: center;">
                    <button onclick="openEditModal(${game.id})" class="btn btn-primary" style="padding: 8px 15px;">✏️ Edit</button>
                    <button onclick="deleteGame(${game.id})" class="btn btn-danger" style="padding: 8px 15px;">🗑️ Delete</button>
                </div>
            </div>
        `;
    });
}


async function fetchGames() {
    try {
        const response = await fetch(`${API_URL}/oyunlar`, {
            headers: { "Authorization": `Bearer ${authToken}` }
        });
        
        if (response.status === 401) {
            handleLogout();
            return;
        }

        const games = await response.json();
        allGames = games; 
        renderGames(allGames); 
    } catch (error) {
        console.error("Error fetching games:", error);
    }
}


function searchGames() {
    const searchText = document.getElementById("search-box").value.toLowerCase();

    const filteredGames = allGames.filter(game => {
        
        const pName = game.yapımcı || game.yapimci || "";
        return (
            game.isim.toLowerCase().includes(searchText) || 
            game.tur.toLowerCase().includes(searchText) ||
            pName.toLowerCase().includes(searchText)
        );
    });

    renderGames(filteredGames);
}



async function addGame() {
    const nameVal = document.getElementById("new-name").value;
    const catVal = document.getElementById("new-category").value;
    const pubVal = document.getElementById("new-publisher").value;
    const scoreVal = document.getElementById("new-score").value;

    if (!nameVal || !catVal || !pubVal || !scoreVal) {
        alert("Please fill all fields");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/oyun-ekle`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${authToken}`
            },
            body: JSON.stringify({ 
                isim: nameVal, 
                tur: catVal, 
                yapımcı: pubVal, 
                puan: parseInt(scoreVal) 
            })
        });

        if (response.ok) {
            document.getElementById("new-name").value = "";
            document.getElementById("new-category").value = "";
            document.getElementById("new-publisher").value = "";
            document.getElementById("new-score").value = "";
            fetchGames();
        } else {
            alert("Failed to add game");
        }
    } catch (error) {
        console.error("Error adding game:", error);
    }
}

async function deleteGame(id) {
    if(confirm("Are you sure?")) {
        try {
            await fetch(`${API_URL}/oyun-sil/${id}`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${authToken}` }
            });
            fetchGames();
        } catch (error) {
            console.error("Delete error:", error);
        }
    }
}



function openEditModal(id) {
    const gameToEdit = allGames.find(g => g.id === id);
    if (!gameToEdit) return;

    document.getElementById("edit-id").value = gameToEdit.id;
    document.getElementById("edit-name").value = gameToEdit.isim;
    document.getElementById("edit-category").value = gameToEdit.tur;
    
    document.getElementById("edit-publisher").value = gameToEdit.yapımcı || gameToEdit.yapimci;
    document.getElementById("edit-score").value = gameToEdit.puan;

    document.getElementById("edit-modal").style.display = "flex";
}

function closeEditModal() {
    document.getElementById("edit-modal").style.display = "none";
}

async function submitUpdate() {
    const id = document.getElementById("edit-id").value;
    const name = document.getElementById("edit-name").value;
    const cat = document.getElementById("edit-category").value;
    const pub = document.getElementById("edit-publisher").value;
    const score = document.getElementById("edit-score").value;

    try {
        const response = await fetch(`${API_URL}/oyun-guncelle/${id}`, {
            method: "PUT",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${authToken}`
            },
            body: JSON.stringify({ 
                isim: name, 
                tur: cat, 
                yapimci: pub, 
                puan: parseInt(score)
            })
        });

        if (response.ok) {
            closeEditModal();
            fetchGames();
        } else {
            alert("Update Failed");
        }
    } catch (error) {
        alert("Connection Error");
    }
}


function showRegisterScreen() {
    document.getElementById("login-panel").style.display = "none";
    document.getElementById("register-panel").style.display = "block";
    document.getElementById("error-message").innerText = "";
}

function showLoginScreen() {
    document.getElementById("register-panel").style.display = "none";
    document.getElementById("login-panel").style.display = "block";
    document.getElementById("reg-error-message").innerText = "";
}

function toggleScreens(isLoggedIn) {
    if (isLoggedIn) {
        document.getElementById("dashboard").style.display = "block";
        document.getElementById("login-panel").style.display = "none";
        document.getElementById("register-panel").style.display = "none";
    } else {
        document.getElementById("dashboard").style.display = "none";
        document.getElementById("login-panel").style.display = "block";
        document.getElementById("register-panel").style.display = "none";
    }
}
