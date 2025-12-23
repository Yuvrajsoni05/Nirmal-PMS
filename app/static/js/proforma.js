document.addEventListener("DOMContentLoaded", function () {
    const invoiceNoInput = document.getElementById("invoice_no");
    const invoiceNoError = document.getElementById("invoice_no_error");

    const QuantityInput = document.getElementById("quantity");
    const QuantityError = document.getElementById("quantity_error");

    const PRPCInput = document.getElementById("prpc_price");
    const PRPCError = document.getElementById("prpc_price_error");

    const invoiceDateInput = document.getElementById("invoice_date");
    const invoiceDateError = document.getElementById("invoice_date_error");

    const modePaymentInput = document.getElementById("mode_payment");
    const modePaymentError = document.getElementById("mode_payment_error");

    const PartyNameInput = document.getElementById("party_name");
    const PartyNameError = document.getElementById("party_name_error");

    const PartyContactInput = document.getElementById("party_contact");
    const PartyContactError = document.getElementById("party_contact_error");

    const PartyEmailInput = document.getElementById("party_email");
    const PartyEmailError = document.getElementById("party_email_error");

    const billingAddressInput = document.getElementById("billing_address_select");
    const billingAddressError = document.getElementById(
        "billing_address_error"
    );

    const billingStateNameInput = document.getElementById("billing_state_name");
    const billingStateNameError = document.getElementById(
        "billing_state_name_error"
    );

    const billingGstinNoInput = document.getElementById("billing_gstin_no");
    const billingGstinNoError = document.getElementById(
        "billing_gstin_no_error"
    );

    const termsInput = document.getElementById("terms");
    const termsError = document.getElementById("terms_error");

    const taxableValueInput = document.getElementById("taxable_value");
    const taxableValueError = document.getElementById("taxable_value_error");

    const totalAmountInput = document.getElementById("total_amount");
    const totalAmountError = document.getElementById("total_amount_error");

    const bankDetailsInput = document.getElementById("bank_details");
    const bankDetailsError = document.getElementById("bank_details_error");

    const InvoiceStatusInput = document.getElementById("invoice_status");
    const InvoiceStatusError = document.getElementById("order_status_error");

    const TitleInput = document.getElementById("title");
    const TitleError = document.getElementById("title_input_error");

    const jobNameInput = document.getElementById("job_name");
    const newJobInput = document.querySelector(".new-job");
    const jobNameError = document.querySelector(".job-name-error");

    const cylinder_diameter_Input =
        document.getElementById("cylinder_diameter");
    const cylinder_diameter_Error = document.getElementById(
        "cylinder_diameter_error"
    );

    const cylinder_height_Input = document.getElementById("cylinder_height");
    const cylinder_height_Error = document.getElementById(
        "cylinder_height_error"
    );

    const pouch_open_diameter_Input = document.getElementById(
        "pouch_open_size_diameter"
    );
    const pouch_open_diameter_Error = document.getElementById(
        "pouch_open_diameter_error"
    );

    const pouch_open_height_Input = document.getElementById(
        "pouch_open_size_height"
    );
    const pouch_open_height_Error = document.getElementById(
        "pouch_open_height_error"
    );

    const proformaForm = document.getElementById("proformaInvoiceForm");

    // Validation Functions
    function validateInvoiceNo() {
        if (invoiceNoInput.value.trim() === "") {
            invoiceNoError.style.display = "block";
            return false;
        } else {
            invoiceNoError.style.display = "none";
            return true;
        }
    }

    function validateJobName() {
        if (
            jobNameInput.value === "" ||
            (jobNameInput.value === "others" && newJobInput.value.trim() === "")
        ) {
            jobNameError.style.display = "block";
            return false;
        } else {
            jobNameError.style.display = "none";
            return true;
        }
    }

    function validatePRPCPrice() {
        if (PRPCInput.value.trim() === "") {
            PRPCError.style.display = "block";
            return false;
        } else {
            PRPCError.style.display = "none";
            return true;
        }
    }

    function validateQuantity() {
        if (QuantityInput.value.trim() === "") {
            QuantityError.style.display = "block";
            return false;
        } else {
            QuantityError.style.display = "none";
            return true;
        }
    }

    function validateInvoiceDate() {
        if (invoiceDateInput.value.trim() === "") {
            invoiceDateError.style.display = "block";
            return false;
        } else {
            invoiceDateError.style.display = "none";
            return true;
        }
    }

    function validateModePayment() {
        if (modePaymentInput.value.trim() === "") {
            modePaymentError.style.display = "block";
            return false;
        } else {
            modePaymentError.style.display = "none";
            return true;
        }
    }

    function validatePartyName() {
        if (PartyNameInput.value.trim() === "") {
            PartyNameError.style.display = "block";
            return false;
        } else {
            PartyNameError.style.display = "none";
            return true;
        }
    }

    function validateTitle() {
        if (TitleInput.value.trim() === "") {
            TitleError.style.display = "block";
            return false;
        } else {
            TitleError.style.display = "none";
            return true;
        }
    }

    function validatePartyContact() {
        const contact = PartyContactInput.value.trim();
        const contactPattern = /^\d{10}$/;
        if (contact === "" || !contactPattern.test(contact)) {
            PartyContactError.style.display = "block";
            return false;
        } else {
            PartyContactError.style.display = "none";
            return true;
        }
    }

    function validatePartyEmail() {
        const email = PartyEmailInput.value.trim();
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (email === "" || !emailPattern.test(email)) {
            PartyEmailError.style.display = "block";
            return false;
        } else {
            PartyEmailError.style.display = "none";
            return true;
        }
    }

    function validateBillingAddress() {
        if (billingAddressInput.value.trim() === "") {
            billingAddressError.style.display = "block";
            return false;
        } else {
            billingAddressError.style.display = "none";
            return true;
        }
    }

    function validateBillingStateName() {
        if (billingStateNameInput.value.trim() === "") {
            billingStateNameError.style.display = "block";
            return false;
        } else {
            billingStateNameError.style.display = "none";
            return true;
        }
    }

    function validateBillingGstinNo() {
        if (billingGstinNoInput.value.trim() === "") {
            billingGstinNoError.style.display = "block";
            return false;
        } else {
            billingGstinNoError.style.display = "none";
            return true;
        }
    }

    function validateInvoiceStatus() {
        if (InvoiceStatusInput.value.trim() === "") {
            InvoiceStatusError.style.display = "block";
            return false;
        } else {
            InvoiceStatusError.style.display = "none";
            return true;
        }
    }

    function validateTerms() {
        if (termsInput.value.trim() === "") {
            termsError.style.display = "block";
            return false;
        } else {
            termsError.style.display = "none";
            return true;
        }
    }

    function validateTaxableValue() {
        if (taxableValueInput.value.trim() === "") {
            taxableValueError.style.display = "block";
            return false;
        } else {
            taxableValueError.style.display = "none";
            return true;
        }
    }

    function validateTotalAmount() {
        if (totalAmountInput.value.trim() === "") {
            totalAmountError.style.display = "block";
            return false;
        } else {
            totalAmountError.style.display = "none";
            return true;
        }
    }

    function validateBankDetails() {
        if (bankDetailsInput.value.trim() === "") {
            bankDetailsError.style.display = "block";
            return false;
        } else {
            bankDetailsError.style.display = "none";
            return true;
        }
    }

    function validateCylinderDiameter() {
        if (cylinder_diameter_Input && cylinder_diameter_Error) {
            if (cylinder_diameter_Input.value.trim() === "") {
                cylinder_diameter_Error.style.display = "block";
                return false;
            } else {
                cylinder_diameter_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validateCylinderHeight() {
        if (cylinder_height_Input && cylinder_height_Error) {
            if (cylinder_height_Input.value.trim() === "") {
                cylinder_height_Error.style.display = "block";
                return false;
            } else {
                cylinder_height_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validatePouchOpenDiameter() {
        if (pouch_open_diameter_Input && pouch_open_diameter_Error) {
            if (pouch_open_diameter_Input.value.trim() === "") {
                pouch_open_diameter_Error.style.display = "block";
                return false;
            } else {
                pouch_open_diameter_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validatePouchOpenHeight() {
        if (pouch_open_height_Input && pouch_open_height_Error) {
            if (pouch_open_height_Input.value.trim() === "") {
                pouch_open_height_Error.style.display = "block";
                return false;
            } else {
                pouch_open_height_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validateForm() {
        const isInvoiceStatus = validateInvoiceStatus();
        const isTitleValid = validateTitle();
        const isJobNameValid = validateJobName();
        const isPRPCValid = validatePRPCPrice();
        const isInvoiceNoValid = validateInvoiceNo();
        const isInvoiceDateValid = validateInvoiceDate();
        const isModePaymentValid = validateModePayment();
        const isPartyNameValid = validatePartyName();
        const isPartyContactValid = validatePartyContact();
        const isPartyEmailValid = validatePartyEmail();
        const isBillingAddressValid = validateBillingAddress();
        const isBillingStateNameValid = validateBillingStateName();
        const isBillingGstinNoValid = validateBillingGstinNo();
        const isTermsValid = validateTerms();
        const isQuantityValid = validateQuantity();
        const isTaxableValueValid = validateTaxableValue();
        const isTotalAmountValid = validateTotalAmount();
        const isBankDetailsValid = validateBankDetails();
        const isvalidateCylinderDiameter = validateCylinderDiameter();
        const isvalidateCylinderHeigh = validateCylinderHeight();

        const isvalidatePouchOpenDiameter = validatePouchOpenDiameter();
        const isvalidatePouchOpenHeight = validatePouchOpenHeight();

        return (
            isInvoiceNoValid &&
            isInvoiceDateValid &&
            isModePaymentValid &&
            isPartyNameValid &&
            isPartyContactValid &&
            isPartyEmailValid &&
            isBillingAddressValid &&
            isBillingStateNameValid &&
            isBillingGstinNoValid &&
            isTermsValid &&
            isTaxableValueValid &&
            isTotalAmountValid &&
            isBankDetailsValid &&
            isQuantityValid &&
            isPRPCValid &&
            isJobNameValid &&
            isvalidateCylinderDiameter &&
            isvalidateCylinderHeigh &&
            isvalidatePouchOpenHeight &&
            isvalidatePouchOpenDiameter &&
            isTitleValid &&
            isInvoiceStatus
        );
    }

    jobNameInput.addEventListener("change", validateJobName);
    newJobInput.addEventListener("input", validateJobName);
    invoiceNoInput.addEventListener("input", validateInvoiceNo);
    invoiceDateInput.addEventListener("input", validateInvoiceDate);
    modePaymentInput.addEventListener("input", validateModePayment);
    PartyNameInput.addEventListener("input", validatePartyName);
    PartyContactInput.addEventListener("input", validatePartyContact);
    PartyEmailInput.addEventListener("input", validatePartyEmail);
    billingAddressInput.addEventListener("input", validateBillingAddress);
    billingStateNameInput.addEventListener("input", validateBillingStateName);
    billingGstinNoInput.addEventListener("input", validateBillingGstinNo);
    termsInput.addEventListener("input", validateTerms);
    taxableValueInput.addEventListener("input", validateTaxableValue);
    totalAmountInput.addEventListener("input", validateTotalAmount);
    QuantityInput.addEventListener("input", validateQuantity);
    bankDetailsInput.addEventListener("input", validateBankDetails);
    PRPCInput.addEventListener("input", validatePRPCPrice);
    cylinder_diameter_Input.addEventListener("input", validateCylinderDiameter);
    cylinder_height_Input.addEventListener("input", validateCylinderHeight);
    TitleInput.addEventListener("input", validateTitle);
    pouch_open_diameter_Input.addEventListener(
        "input",
        validatePouchOpenDiameter
    );
    pouch_open_height_Input.addEventListener("input", validatePouchOpenHeight);
    InvoiceStatusInput.addEventListener("input", validateInvoiceStatus);

    const loaderOverlay = document.getElementById("loader-overlay");
    proformaForm.addEventListener("submit", function (event) {
        event.preventDefault();

        if (validateForm()) {
            if (loaderOverlay) {
                loaderOverlay.style.display = "flex";
            }
            requestAnimationFrame(() => {
                proformaForm.submit();
            });
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
