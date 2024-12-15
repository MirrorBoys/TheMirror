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
    document.getElementById('usernameTextbox').value = tagId;
    document.getElementById('passwordTextbox').value = tagData;
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
window.onload = loginWithNfc;