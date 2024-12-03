let timezone; // The timezone of the user sent by function fetchSessionData()

function updateClock() {
    // let timezone = document.getElementById('timezone').getAttribute('timezone');
    // console.log('Timezone:', timezone);
    fetch(`/api/time/fetch/${timezone}`)	
        .then(response => response.json())
        .then(data => {
            document.getElementById('current-time').textContent = data.current_time;
        })
        .catch(error => console.error('Error fetching current time:', error));
}

//Fetches timezone once at the start of the page
function fetchSessionData() {
    fetch('/api/session/fetch-session-timezone/')
        .then(response => response.json())
        .then(data => {
            timezone = data.timezone;
        })
        .catch(error => console.error('Error fetching session timezone:', error));
}

function synchronizeClock() {
    const now = new Date(); // Get the current time
    const delay = ((60 - now.getSeconds()) * 1000) - now.getMilliseconds(); // Calculate the delay to the start of the next minute
    setTimeout(function() {
        updateClock(); // Update the clock
        setInterval(updateClock, 60000); // Update the clock every 60 seconds
    }, delay); // Delay the first update at first page load to the start of the next minute
}

window.onload = function() {
    synchronizeClock(); // Synchronize the clock to the start of the next minute
    fetchSessionData(); // Fetch the timezone of the user
}