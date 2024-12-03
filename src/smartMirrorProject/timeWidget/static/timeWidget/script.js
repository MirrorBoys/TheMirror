let timezone; // The timezone of the user sent by function fetchSessionData()
// console.log('Timezone:', timezone);

function updateClock() {
    // let timezone = document.getElementById('timezone').getAttribute('timezone');
    // decoded_timezone = timezone.replace("/", "-");
    // console.log('Timezone:', decoded_timezone);
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
    // Calculate the time remaining until the next minute starts
    const now = new Date();
    const delay = ((60 - now.getSeconds()) * 1000) - now.getMilliseconds();
    // Set a timeout to update the clock at the start of the next minute
    setTimeout(() => {
        updateClock();
        // Set an interval to update the clock every minute
        setInterval(updateClock, 60000);
    }, delay);
}

document.addEventListener('DOMContentLoaded', (event) => {
    synchronizeClock();
    fetchSessionData();
});