/**
 * Hides the NFC help text.
 */
function hideNfcHelptext() {
    document.getElementById("helptext-nfc").style.display = 'none';
}

/**
 * Retrieves NFC data and populates the NFC tag ID input field with the retrieved tag ID and hides NFC helptext.
 * 
 * @function enterNfcTagId
 * @returns {Promise<void>} A promise that resolves when the NFC data has been retrieved and processed.
 */
async function enterNfcTagId() {
    const data = await retrieveNfcData();
    if (data) {
        document.getElementById('nfc_tag_id').value = data.tagId;
        // Manually trigger an input event to simulate human input. Needed for eventListener which enabled submit button
        document.getElementById('nfc_tag_id').dispatchEvent(new Event('input'));
        hideNfcHelptext();
    }
}

// On load, check if current system is a Raspberry Pi. If so, enable functionality to add NFC-tag to registration form.
window.onload = async function () {
    const isRaspberryPi = await isRunningOnRaspberryPi();
    if (isRaspberryPi) {
        enterNfcTagId();
    }
}

// Wait until entire HTML is loaded before executing this code. 
document.addEventListener("DOMContentLoaded", function () {
    const usernameInput = document.getElementById("id_username");
    const password1Input = document.getElementById("id_password1");
    const password2Input = document.getElementById("id_password2");
    const nfcTagIdInput = document.getElementById("nfc_tag_id");
    const registerButton = document.getElementById("register-button");

    /**
     * Toggle the register button based on the input fields' values. 
     */
    function toggleRegisterButton() {
        if (
            usernameInput.value.trim() !== "" &&
            password1Input.value.trim() !== "" &&
            password2Input.value.trim() !== "" &&
            nfcTagIdInput.value.trim() !== ""
        ) {
            registerButton.disabled = false;
            registerButton.classList.remove("disabled");
            registerButton.classList.add("enabled");
        } else {
            registerButton.disabled = true;
            registerButton.classList.remove("enabled");
            registerButton.classList.add("disabled");
        }
    }

    // Run this function at start
    toggleRegisterButton();

    // Add event listeners to check the input fields on change
    usernameInput.addEventListener("input", toggleRegisterButton);
    password1Input.addEventListener("input", toggleRegisterButton);
    password2Input.addEventListener("input", toggleRegisterButton);
    nfcTagIdInput.addEventListener("input", toggleRegisterButton);
});