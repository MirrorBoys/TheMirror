/**
 * Asynchronously retrieves NFC data from the server.
 *
 * This function sends a GET request to the '/api/nfc/fetch/' to fetch NFC data of a NFC-tag.
 *
 * @async
 * @function retrieveNfcData
 * @returns {Promise<Object|null>}
 */
async function retrieveNfcData() {
    try {
        const response = await fetch('/api/nfc/fetch/');
        const data = await response.json();
        if (response.ok) {
            return data;
        } else {
            console.error('Error fetching NFC data:', data.error);
        }
    } catch (error) {
        console.error('Error fetching NFC data:', error);
    }
    return null;
}

/**
 * Checks if the current system is a Raspberry Pi.
 *
 * This function sends a request to the endpoint '/api/nfc/isPi/' to determine
 * if the current system is a Raspberry Pi.
 *
 * @returns {Promise<boolean>} A promise that resolves to `true` if the system is a Raspberry Pi, otherwise `false`.
 */
async function isRunningOnRaspberryPi() {
    try {
        const response = await fetch('/api/nfc/isPi/');
        const data = await response.json();
        return data.is_raspberry_pi;
    } catch (error) {
        console.error('Error checking system info:', error);
        return false;
    }
}