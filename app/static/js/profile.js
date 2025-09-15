function togglePassword(inputId, button) {
    var input = document.getElementById(inputId);
    var icon = button.querySelector("i");

    // Toggle input type between password and text
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        input.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}

const emailInput = document.getElementById("email");
const emailFeedback = document.getElementById("email_error");

const emailRegex =
    /^(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

function validateEmail() {
    const emailValue = emailInput.value;

    if (emailRegex.test(emailValue)) {
        emailFeedback.style.display = "none";
    } else {
        emailFeedback.style.display = "block";
    }
}

emailInput.addEventListener("input", validateEmail);

const usernameInput = document.getElementById("username");
const usernameError = document.getElementById("username_error");

function validateUser() {
    const usernameValue = usernameInput.value;
    if (usernameValue === "") {
        usernameError.style.display = "block";
    } else {
        usernameError.style.display = "none";
    }
}

usernameInput.addEventListener("input", validateUser);
usernameInput.addEventListener("blur", validateUser);

const lastnameInput = document.getElementById("last_name");
const lastnameError = document.getElementById("lastname_error");

function validateLastName() {
    const lastNameValue = lastnameInput.value;
    if (lastNameValue === "") {
        lastnameError.style.display = "block";
    } else {
        lastnameError.style.display = "none";
    }
}

lastnameInput.addEventListener("input", validateLastName);
lastnameInput.addEventListener("blur", validateLastName);

const FirstInput = document.getElementById("first_name");
const FirstError = document.getElementById("firstname_error");

function validateFirstName() {
    const FirstNameValue = FirstInput.value;
    if (FirstNameValue === "") {
        FirstError.style.display = "block";
    } else {
        FirstError.style.display = "none";
    }
}

FirstInput.addEventListener("input", validateFirstName);
FirstInput.addEventListener("blur", validateFirstName);

document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.getElementById("new_password");
    const passwordError = document.getElementById("new_password_error");

    const confirmPasswordInput = document.getElementById("confirm_password");
    const confirmPasswordError = document.getElementById(
        "confirm_password_error"
    );

    const myForm = document.getElementById("password_form");

    function validatePassword() {
        if (passwordInput.value.trim() === "") {
            passwordError.style.display = "block";
            return false;
        } else {
            passwordError.style.display = "none";
            return true;
        }
    }

    function validateConfirmPassword() {
        if (confirmPasswordInput.value.trim() !== passwordInput.value.trim()) {
            confirmPasswordError.style.display = "block";
            return false;
        } else {
            confirmPasswordError.style.display = "none";
            return true;
        }
    }

    function validateForm() {
        const isPasswordValid = validatePassword();
        const isConfirmPasswordValid = validateConfirmPassword();

        return isPasswordValid && isConfirmPasswordValid;
    }

    passwordInput.addEventListener("input", validatePassword);
    confirmPasswordInput.addEventListener("input", validateConfirmPassword);

    passwordInput.addEventListener("blur", validatePassword);
    confirmPasswordInput.addEventListener("blur", validateConfirmPassword);

    myForm.addEventListener("submit", function (event) {
        event.preventDefault();

        if (validateForm()) {
            myForm.submit();
        } else {
            const firstError = document.querySelector(
                '[style*="display: block"]'
            );
            if (firstError) {
                firstError.scrollIntoView({ behavior: "smooth" });
            }
        }
    });
});
