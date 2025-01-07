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
 * Populates the NFC tag ID and data into the corresponding input fields on the login page.
 *
 * @param {string} tagId - The ID of the NFC tag.
 * @param {string} tagData - The data associated on the NFC tag.
 */
function enterNfcData(tagId, tagData) {
    document.getElementById('nfc_tag_id').value = tagId;
    document.getElementById('nfc_tag_data').value = tagData;
}

/**
 * Triggers a click event on the login button.
 */
function login() {
    document.getElementById('loginButton').click();
}

/**
 * Asynchronously handles the login using NFC.
 * Retrieves NFC data, enters the data, and triggers the login process.
 *
 * @async
 * @function loginWithNfc
 * @returns {Promise<void>} A promise that resolves when the login process is complete.
 */
async function loginWithNfc() {
    const data = await retrieveNfcData();
    if (data) {
        enterNfcData(data.tagId, data.tagData);
        login();
    }
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
        console.log(data)
        return data.is_raspberry_pi
    } catch (error) {
        console.error('Error checking system info:', error);
        return false;
    }
}

// On load, check if current system is a Raspberry Pi. If so, enable login with NFC functionality.
window.onload = async function () {
    const isRaspberryPi = await isRunningOnRaspberryPi();
    if (isRaspberryPi) {
        loginWithNfc();
    }
}