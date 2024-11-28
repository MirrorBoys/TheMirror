function updateClock() {
    let timezone = document.getElementById('current-time').getAttribute('timezone');
    fetch(`/api/time/fetch/${timezone}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('current-time').textContent = data.current_time;
        })
        .catch(error => console.error('Error fetching current time:', error));
}

function synchronizeClock() {
    // Show the clock immediately after the page loads
    updateClock();
    // Calculate the time remaining until the next minute starts
    const now = new Date();
    const delay = ((60 - now.getSeconds()) * 1000) - now.getMilliseconds();

    // Set a timeout to update the clock at the start of the next minute
    setTimeout(() => {
        updateClock();

        // Set an interval to update the clock every minute
        setInterval(updateClock, 60000);
    }, delay); // Delay the first update at first page load to the start of the next minute
}

// Start the clock synchronization when the page loads
window.onload = synchronizeClock;