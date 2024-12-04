function updateClock() {
    let timezone = document.getElementById('timezone').getAttribute('timezone');
    let decoded_timezone = timezone.replace("/", "-");
    $.ajax({
        url: `/api/time/fetch/${decoded_timezone}`,
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            document.getElementById('current-time').textContent = data.current_time;
        },
        error: function(error) {
            console.error('Error fetching current time:', error);
        }
    });
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

synchronizeClock();