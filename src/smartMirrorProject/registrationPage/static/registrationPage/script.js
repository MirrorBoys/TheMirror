document.addEventListener("DOMContentLoaded", function () {
    const usernameInput = document.getElementById("id_username");
    const password1Input = document.getElementById("id_password1");
    const password2Input = document.getElementById("id_password2");
    const nfcTagIdInput = document.getElementById("nfc_tag_id");
    const registerButton = document.getElementById("register-button");

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

    // Initial check
    toggleRegisterButton();

    // Add event listeners to check the input fields on change
    usernameInput.addEventListener("input", toggleRegisterButton);
    password1Input.addEventListener("input", toggleRegisterButton);
    password2Input.addEventListener("input", toggleRegisterButton);
    nfcTagIdInput.addEventListener("input", toggleRegisterButton);
});