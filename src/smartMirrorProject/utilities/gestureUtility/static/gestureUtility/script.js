//Spotify login
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