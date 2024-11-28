function updateClock() {
    const timezone = "CET";
    fetch(`/api/time/fetch/${timezone}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('current-time').textContent = data.current_time;
        })
        .catch(error => console.error('Error fetching current time:', error));
}

function synchronizeClock() {
    updateClock();
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

// Start the clock synchronization when the page loads
window.onload = synchronizeClock;