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
            document.getElementById('gesture-feedback').innerText = 'Gesture: PAUSE';
            pauseMusic();
        } else if (gesture == 'PLAY') {
            document.getElementById('gesture-feedback').innerText = 'Gesture: PLAY';
            playMusic();
        } else if (gesture == 'SKIP') {
            document.getElementById('gesture-feedback').innerText = 'Gesture: SKIP';
            skipMusic();
        } else if (gesture == 'LOGIN') {
            document.getElementById('gesture-feedback').innerText = 'Gesture: LOGIN';
            loginLogout();
        } else if (gesture == 'REFRESH') {
            document.getElementById('gesture-feedback').innerText = 'Gesture: REFRESH';
            refreshPage();
        } else if (gesture == 'LOGOUT') {
            document.getElementById('gesture-feedback').innerText = 'Gesture: LOGOUT';
            logoutMirror();
    }
}

// Periodically check for gesture changes
setInterval(executeGesture, 1000); // Check every second

function logoutMirror() {
    document.getElementById('logout-button').click();
}

// Page reload
function refreshPage() {
    window.location.reload();
}

// Go to news link
function goToNewsLink() {
    const newsLink = document.getElementById('news-link');
    if (newsLink) {
        newsLink.click();
    }
}

// Pause music
function pauseMusic() {
    player.pause();
    document.getElementById('togglePlay').innerText = 'Paused';
}


// Play music
function playMusic() {
    player.resume();
    document.getElementById('togglePlay').innerText = 'Playing';
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

// Select grid items with arrow keys and focus on the selected widget
document.addEventListener('DOMContentLoaded', function() {
    let currentIndex = 0;
    const gridItems = document.querySelectorAll('.grid-item');

    function updateSelection() {
        gridItems.forEach((item, index) => {
            item.classList.toggle('selected', index == currentIndex);
            if (index == currentIndex) {
                item.style.border = '2px solid var(--yellow-color)';
                item.focus();
            } else {
                item.style.border = 'none';
            }
        });
        gridItems[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    document.addEventListener('keydown', function(event) {
        if (event.key == 'ArrowRight') {
            currentIndex = (currentIndex + 1) % gridItems.length;
            updateSelection();
        } else if (event.key == 'ArrowLeft') {
            currentIndex = (currentIndex - 1 + gridItems.length) % gridItems.length;
            updateSelection();
        }
    });

    updateSelection();
});