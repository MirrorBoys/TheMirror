// Functions for actions gestures can perform
async function fetchGesture() {
    try {
        const response = await fetch('api/gesture/fetch');
        const data = await response.json();
        if (response.ok) {
            return data.gesture;
        } else {
            console.error('Error fetching gesture data:', data.error);
        }
    }
    catch (error) {
        console.error('Error fetching gesture data:', error);
    }
    return null;
}

async function executeGesture() {
    const gesture = await fetchGesture();
    if (gesture == 'PAUSE') {
        document.getElementById('gesture-feedback').innerText = 'Gebaar: Pauzeren';
        pauseMusic();
    } else if (gesture == 'PLAY') {
        document.getElementById('gesture-feedback').innerText = 'Gebaar: Afspelen';
        playMusic();
    } else if (gesture == 'SKIP') {
        document.getElementById('gesture-feedback').innerText = 'Gebaar: Overslaan';
        skipMusic();
    } else if (gesture == 'LOGIN') {
        document.getElementById('gesture-feedback').innerText = 'Gebaar: Inloggen';
        loginLogout();
    } else if (gesture == 'REFRESH') {
        document.getElementById('gesture-feedback').innerText = 'Gebaar: Verversen';
        refreshPage();
    } else if (gesture == 'LOGOUT') {
        document.getElementById('gesture-feedback').innerText = 'Gebaar: Uitloggen';
        logoutMirror();
    }
}

setInterval(executeGesture, 1000); // Check every second

function logoutMirror() {
    document.getElementById('logout-button').click();
}

// Page reload
function refreshPage() {
    window.location.reload();
}

// Pause music
function pauseMusic() {
    player.pause();
    document.getElementById('togglePlay').innerText = 'Gepauzeerd';
}


// Play music
function playMusic() {
    player.resume();
    document.getElementById('togglePlay').innerText = 'Afspelen';
}

// Skip music
function skipMusic() {
    player.nextTrack()
}

// Spotify login/logout
function loginLogout() {
    const loginButton = document.getElementById('login');
    const logoutButton = document.getElementById('logout');
    if (loginButton) {
        loginButton.click();
    } else if (logoutButton) {
        logoutButton.click();
    }
}
