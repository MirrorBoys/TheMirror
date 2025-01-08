// NOTE: Some referred functions are defined in TheMirror/src/smartMirrorProject/globalStatic/global_script.js

/**
 * Populates the NFC tag ID and data into the corresponding input fields on the login page.
 *
 * @param {string} tagId - The ID of the NFC tag.
 */
function enterNfcData(tagId) {
    document.getElementById('nfc_tag_id').value = tagId;
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
        enterNfcData(data.tagId);
        login();
    }
}

// On load, check if current system is a Raspberry Pi. If so, enable login with NFC functionality.
window.onload = async function () {
    const isRaspberryPi = await isRunningOnRaspberryPi();
    if (isRaspberryPi) {
        loginWithNfc();
    }
}