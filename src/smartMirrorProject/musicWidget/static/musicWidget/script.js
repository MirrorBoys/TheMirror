// Spotify Web Playback SDK

// Initialize Spotify Player, global so this can be used everywhere inside this file
let player;

function initializeSpotifyPlayer(token) {
    if (token) {
        player = new Spotify.Player({
            name: 'Web Playback SDK Quick Start Player',
            getOAuthToken: cb => { cb(token); },
        });

        // Show current and next track
        player.addListener('player_state_changed', state => {
            if (!state) {
                return;
            }

            const currentTrack = state.track_window.current_track;
            const nextTrack = state.track_window.next_tracks[0];

            document.getElementById('current-track').innerText = `Now Playing: ${currentTrack.name} by ${currentTrack.artists[0].name}`;
            document.getElementById('next-track').innerText = `Next: ${nextTrack ? nextTrack.name : 'None'} by ${nextTrack ? nextTrack.artists[0].name : 'N/A'}`;
        });

        // Ready
        player.addListener('ready', ({ device_id }) => {
            console.log('Ready with Device ID', device_id);
        });

        // Not Ready
        player.addListener('not_ready', ({ device_id }) => {
            console.log('Device ID has gone offline', device_id);
        });

        player.addListener('initialization_error', ({ message }) => {
            console.error(message);
        });

        player.addListener('authentication_error', ({ message }) => {
            console.error(message);
        });

        player.addListener('account_error', ({ message }) => {
            console.error(message);
        });

        player.connect();
    }

}

// Was first inside the initializeSpotifyPlayer function, but moved it outside so the inputs for the buttons and keys can be recognized
document.addEventListener('DOMContentLoaded', () => {
    // Toggle play with button
    document.getElementById('togglePlay').onclick = function () {
        player.togglePlay();
    };

    // Toggle play with space key
    document.addEventListener('keydown', function (event) {
        if (event.key == ' ') {
            player.getCurrentState().then(state => {
                if (state.paused) {
                    player.resume().then(() => {
                        document.getElementById('togglePlay').innerText = 'Playing';
                    });
                } else {
                    player.pause().then(() => {
                        document.getElementById('togglePlay').innerText = 'Paused';
                    });
                }
            });
        }
    });

    // Skip track with button
    document.getElementById('skipTrack').onclick = function () {
        player.nextTrack().then(() => {
            console.log('Skipped to next track!');
        });
    };

    // Skip track with arrow up key
    document.addEventListener('keydown', function (event) {
        if (event.key == 'ArrowUp') {
            player.nextTrack().then(() => {
                console.log('Skipped to next track!');
            });
        }
    });

    // Add song to queue
    document.getElementById('add-to-queue').onclick = function () {
        const trackUri = document.getElementById('track-uri').value;
        fetch(`/musicWidget/spotify-add-song/?track_uri=${trackUri}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('queue-message').innerText = `Error: ${data.error}`;
                } else {
                    document.getElementById('queue-message').innerText = data.message;
                }
            })
            .catch(error => {
                document.getElementById('queue-message').innerText = `Error: ${error}`;
            });
    };
});