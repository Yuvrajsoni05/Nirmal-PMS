document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("cdr_form");

    const PartyNameSelect = document.getElementById("party_name");
    const newPartyNameSelect = document.getElementById("new_party_name");
    const partyNameError = document.getElementById("party_name_error");

    const partyEmailSelect = document.getElementById("party_email");
    const newPartyEmailInput = document.getElementById("new_party_email");
    const PartyEmailError = document.getElementById("party_email_error");

    const job_nameSelect = document.getElementById("job_name");
    const new_job_nameInput = document.getElementById("new_job_name");
    const job_name_Error = document.getElementById("job_name_error");

    const partyContactSelect = document.getElementById("party_contact_used");
    const newPartyContactInput = document.getElementById("new_party_contact");
    const partyContactError = document.getElementById("party_contact_error");

    const cdrDateInput = document.getElementById("cdr_upload_date");
    const cdrDateError = document.getElementById("cdr_upload_date_error");

    const cdrFilesInput = document.getElementById("cdr_files");
    const cdrFilesError = document.getElementById("cdr_files_error");

    job_nameSelect.addEventListener("change", function () {
        if (this.value === "others") {
            new_job_nameInput.style.display = "block";
            new_job_nameInput.focus();
        } else {
            new_job_nameInput.style.display = "none";
            new_job_nameInput.value = "";
            job_name_Error.style.display = "none";
        }
    });

    new_job_nameInput.addEventListener("input", function () {
        if (this.value.trim() !== "") {
            job_name_Error.style.display = "none";
        }
    });

    PartyNameSelect.addEventListener("change", function () {
        if (this.value === "others") {
            newPartyNameSelect.style.display = "block";
            newPartyNameSelect.focus();
        } else {
            newPartyNameSelect.style.display = "none";
            newPartyNameSelect.value = "";
            partyNameError.style.display = "none";
        }
    });

    newPartyNameSelect.addEventListener("input", function () {
        if (this.value.trim() !== "") {
            partyNameError.style.display = "none";
        }
    });

    partyContactSelect.addEventListener("change", function () {
        if (this.value === "others") {
            newPartyContactInput.style.display = "block";
            newPartyContactInput.focus();
        } else {
            newPartyContactInput.style.display = "none";
            newPartyContactInput.value = "";
            partyContactError.style.display = "none";
        }
    });

    newPartyContactInput.addEventListener("input", function () {
        if (this.value.trim() !== "") {
            partyContactError.style.display = "none";
        }
    });

    partyEmailSelect.addEventListener("change", function () {
        if (this.value === "other") {
            newPartyEmailInput.style.display = "block";
            newPartyEmailInput.focus();
        } else {
            newPartyEmailInput.style.display = "none";
            newPartyEmailInput.value = "";
            PartyEmailError.style.display = "none";
        }
    });

    newPartyEmailInput.addEventListener("input", function () {
        if (this.value.trim() !== "") {
            PartyEmailError.style.display = "none";
        }
    });

    function validateEmail(email) {
        const pattern =
            /(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return pattern.test(email);
    }

    function validateContact(contact) {
        const contactPattern =
            /^((091|\+91)?|(\(091\)|\(+91\))|(91)?|\(91\)|0)?[ ]?[6-9]\d{9}$/;
        return contactPattern.test(contact);
    }

    function validateForm() {
        let isValid = true;

        if (PartyNameSelect.value === "others") {
            if (newPartyNameSelect.value.trim() === "") {
                partyNameError.style.display = "block";
                isValid = false;
            }
        } else if (PartyNameSelect.value === "") {
            partyNameError.style.display = "block";
            isValid = false;
        }

        if (job_nameSelect.value === "others") {
            if (new_job_nameInput.value.trim() === "") {
                job_name_Error.style.display = "block";
                isValid = false;
            }
        } else if (job_nameSelect.value === "") {
            job_name_Error.style.display = "block";
            isValid = false;
        }

        if (partyEmailSelect.value === "other") {
            if (
                newPartyEmailInput.value.trim() === "" ||
                !validateEmail(newPartyEmailInput.value)
            ) {
                PartyEmailError.style.display = "block";
                isValid = false;
            }
        } else if (partyEmailSelect.value === "") {
            PartyEmailError.style.display = "block";
            isValid = false;
        }

        if (partyContactSelect.value === "others") {
            if (
                newPartyContactInput.value.trim() === "" ||
                !validateContact(newPartyContactInput.value)
            ) {
                partyContactError.style.display = "block";
                isValid = false;
            }
        } else if (partyContactSelect.value === "") {
            partyContactError.style.display = "block";
            isValid = false;
        }

        if (cdrDateInput.value.trim() === "") {
            cdrDateError.style.display = "block";
            isValid = false;
        }

        if (cdrFilesInput.value.trim() === "") {
            cdrFilesError.style.display = "block";
            isValid = false;
        }

        return isValid;
    }

    form.addEventListener("submit", function (e) {
        const loaderOverlay = document.getElementById("loader-overlay");

        if (!validateForm()) {
            e.preventDefault();

            // Scroll to first visible error
            const firstError = document.querySelector(
                '[style*="display: block"]'
            );
            if (firstError) {
                firstError.scrollIntoView({ behavior: "smooth" });
            }
        } else {
            loaderOverlay.style.display = "flex";
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll(".cdr-form");
    const loaderOverlay = document.getElementById("loader-overlay");

    forms.forEach((form) => {
        form.addEventListener("submit", function () {
            loaderOverlay.style.display = "flex";
        });
    });
});

let formIdToSubmit;

// Delete Form Handler
document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".btn-outline-danger");
    deleteButtons.forEach((button) => {
        button.addEventListener("click", function () {
            formIdToSubmit = this.dataset.id;
        });
    });
});

function submitForm() {
    document.getElementById("delete-form-" + formIdToSubmit).submit();
}

// Update Form Validation
function validateUpdateForm(form) {
    let valid = true;
    let requiredFields = [form.cdr_upload_date, form.company_email];

    requiredFields.forEach(function (field) {
        if (field && !field.value.trim()) {
            field.classList.add("is-invalid");
            valid = false;
        } else if (field) {
            field.classList.remove("is-invalid");
        }
    });

    let errorMsg = form.querySelector("#updateFormError");
    if (!valid) {
        if (errorMsg) errorMsg.style.display = "block";
        return false;
    } else {
        if (errorMsg) errorMsg.style.display = "none";
        return true;
    }
}
