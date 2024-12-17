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
function enterNfcData(tagId, tagData) {
    document.getElementById('nfc_tag_id').value = tagId;
    document.getElementById('nfc_tag_data').value = tagData;
}
function login() {
    document.getElementById('loginButton').click();
}
async function loginWithNfc() {
    const data = await retrieveNfcData();
    if (data) {
        enterNfcData(data.tagId, data.tagData);
        login();
    }
}
// Call the function to login with NFC when the page loads
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

window.onload = async function () {
    const isRaspberryPi = await isRunningOnRaspberryPi();
    if (isRaspberryPi) {
        loginWithNfc();
    }
};