// Functions for actions gestures (temporary place)

// Page reload with 'r' key
document.addEventListener('keydown', function(event) {
    if (event.key == 'r' || event.key == 'R') {
        window.location.reload();
    }
});

// Go to news link with 'n' key
document.addEventListener('keydown', function(event) {
    if (event.key == 'n' || event.key == 'N') {
        const newsLink = document.getElementById('news-link');
        if (newsLink) {
            newsLink.click();
        }
    }
});

// Spotify pause/play with ' ' key
document.addEventListener('keydown', function(event) {
    if (event.key == ' ') {
        const playPauseButton = document.getElementById('togglePlay');
        if (playPauseButton) {
            playPauseButton.click();
        }
    }
});

// Spotify skip track with 'ArrowUp' key
document.addEventListener('keydown', function(event) {
    if (event.key == 'ArrowUp') {
        const nextButton = document.getElementById('skipTrack');
        if (nextButton) {
            nextButton.click();
        }
    }
});

// Spotify login/logout with 'l' key
document.addEventListener('keydown', function(event) {
    if (event.key == 'l' || event.key == 'L') {
        const loginButton = document.getElementById('login');
        const logoutButton = document.getElementById('logout');
        if (loginButton) {
            loginButton.click();
        } else if (logoutButton) {
            logoutButton.click();
        }
    }
});

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