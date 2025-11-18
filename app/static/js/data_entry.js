$(document).on(
    "input",
    "[name='cylinder_diameter[]'], [name='cylinder_height[]']",
    function () {
        const section = $(this).closest(".col-12"); // parent container for each row
        const height = section.find("[name='cylinder_height[]']").val();
        const diameter = section.find("[name='cylinder_diameter[]']").val();

        if (height && diameter) {
            // If both diameter and height are provided, store the formatted size
            const cylinderSize = `${height} x ${diameter}`;
            section.find("[name='cylinder_size[]']").val(cylinderSize);
        }
    }
);

$(document).on(
    "input",
    "[name='pouch_diameter[]'], [name='pouch_height[]']",
    function () {
        const section = $(this).closest(".col-12"); // parent container for each row
        const pouch_height = section.find("[name='pouch_height[]']").val();
        const pouch_diameter = section.find("[name='pouch_diameter[]']").val();

        if (pouch_height && pouch_diameter) {
            const pouchSize = `${pouch_height} x ${pouch_diameter}`;
            section.find("[name='pouch_size[]']").val(pouchSize);
        }
    }
);

$(document).on(
    "input",
    "[name='pouch_open_height[]'], [name='pouch_open_diameter[]']",
    function () {
        const section = $(this).closest(".col-12");
        const pouch_open_height = section
            .find("[name='pouch_open_height[]']")
            .val();
        const pouch_open_diameter = section
            .find("[name='pouch_open_diameter[]']")
            .val();

        if (pouch_open_height && pouch_open_diameter) {
            const pouch_open_Size = `${pouch_open_height} x ${pouch_open_diameter}`;
            section.find("[name='pouch_open_size[]']").val(pouch_open_Size);
        }
    }
);

$(document).on(
    "input",
    "[name='pouch_combination1[]'] , [name='pouch_combination2[]'],[name='pouch_combination3[]'], [name='pouch_combination4[]']",
    function () {
        const section = $(this).closest(".col-12");
        const pouch_combination1 = section
            .find("[name='pouch_combination1[]']")
            .val();
        const pouch_combination2 = section
            .find("[name='pouch_combination2[]']")
            .val();
        const pouch_combination3 = section
            .find("[name='pouch_combination3[]']")
            .val();
        const pouch_combination4 = section
            .find("[name='pouch_combination3[]']")
            .val();

        if (
            pouch_combination1 &&
            pouch_combination2 &&
            pouch_combination3 &&
            pouch_combination4
        ) {
            const pouch_combination = `${pouch_combination1} + ${pouch_combination2} + ${pouch_combination3} + ${pouch_combination4}`;
            section.find("[name='pouch_combination[]']").val(pouch_combination);
        }
    }
);

function formatNumberWithCommas(input) {
    let value = input.value;

    value = value.replace(/,/g, "");

    value = value.replace(/[^0-9.]/g, "");

    const parts = value.split(".");
    if (parts.length > 2) {
        value = parts[0] + "." + parts.slice(1).join("");
    }

    if (value === "") {
        input.value = "";
        return;
    }

    if (value === ".") {
        input.value = ".";
        return;
    }

    const [integerPart, decimalPart] = value.split(".");

    if (!integerPart) {
        input.value = decimalPart !== undefined ? "." + decimalPart : "";
        return;
    }

    const formattedInteger = parseInt(integerPart).toLocaleString("en-IN");

    if (decimalPart !== undefined) {
        input.value = formattedInteger + "." + decimalPart;
    } else {
        input.value = formattedInteger;
    }
}
document.addEventListener("DOMContentLoaded", function () {
    const proformaForm   = document.getElementById("job_detail_form");
    const loaderOverlay  = document.getElementById("loader-overlay");

    // Basic Information
    const jobDate        = document.getElementById("job_date");
    const jobDateError   = document.getElementById("job_date_error");

    const billInput      = document.getElementById("bill_no");
    const billError      = document.getElementById("bill_no_error");

    const companyName        = document.getElementById("company_name");
    const companyNameError   = document.getElementById("company_name_error");
    const newCompanyInput    = document.getElementById("new_company");

    // Job Details (first job-section)
    const jobName        = document.getElementById("job_name");
    const jobNameError   = document.getElementById("job_name_error");

    const jobType        = document.getElementById("job_type");
    const jobTypeError   = document.getElementById("job_type_error");

    const nocInput       = document.getElementById("noc");
    const nocError       = document.getElementById("noc_error");

    // Cylinder Information
    const prpcPurchase       = document.getElementById("prpc_purchase");
    const prpcPurchaseError  = document.getElementById("prpc_purchase_error");

    const prpcSell       = document.getElementById("prpc_sell");
    const prpcSellError  = document.getElementById("prpc_sell_error");

    const cylinderDiameter      = document.querySelector('input[name="cylinder_diameter[]"]');
    const cylinderDiameterError = document.querySelector('div[name="cylinder_diameter_error"]');

    const cylinderHeight        = document.querySelector('input[name="cylinder_height[]"]');
    const cylinderHeightError   = document.querySelector('div[name="cylinder_height_error"]');

    const cylinderMadeIn        = document.getElementById("cylinder_made_in");
    const cylinderMadeInError   = document.getElementById("cylinder_made_in_error");
    const cylinderMadeInOther   = document.getElementById("cylinder_made_in_company_name");

    const cylinderDate      = document.getElementById("cylinder_dates");
    const cylinderDateError = document.getElementById("cylinder_date_error");

    const cylinderBillNo      = document.getElementById("cylinder_bill_no");
    const cylinderBillNoError = document.getElementById("cylinder_bill_no_error");

    // Pouch Information
    const pouchDiameter      = document.getElementById("pouch_diameter");
    const pouchDiameterError = document.getElementById("pouch_diameter_error");

    const pouchHeight        = document.getElementById("pouch_height");
    const pouchHeightError   = document.getElementById("pouch_height_error");

    const pouchOpenDiameter      = document.getElementById("pouch_open_diameter");
    const pouchOpenDiameterError = document.getElementById("pouch_open_diameter_error");

    const pouchOpenHeight        = document.getElementById("pouch_open_height");
    const pouchOpenHeightError   = document.getElementById("pouch_open_height_error");

    const pouchCombination1      = document.getElementById("pouch_combination1");
    const pouchCombination1Error = document.getElementById("pouch_combination1_error");

    const pouchCombination2      = document.getElementById("pouch_combination2");
    const pouchCombination2Error = document.getElementById("pouch_combination2_error");

    // Job Status
    const jobStatus      = document.getElementById("job_status");
    const jobStatusError = document.getElementById("job_status_error"); // add this div in HTML

    // ---------- BASIC VALIDATIONS ----------

    function validateJobDate() {
        if (!jobDate || jobDate.value.trim() === "") {
            jobDateError.style.display = "block";
            return false;
        }
        jobDateError.style.display = "none";
        return true;
    }

    function validateInvoiceNo() {
        if (!billInput || billInput.value.trim() === "") {
            billError.style.display = "block";
            return false;
        }
        billError.style.display = "none";
        return true;
    }

    function validateCompanyName() {
        if (!companyName) return true;

        const value = companyName.value.trim();

        // If nothing selected
        if (value === "") {
            companyNameError.style.display = "block";
            newCompanyInput.style.display = "none";
            return false;
        }

        // If "other" selected, new_company required
        if (value === "other") {
            newCompanyInput.style.display = "block";
            if (newCompanyInput.value.trim() === "") {
                companyNameError.textContent = "Please provide New Company Name.";
                companyNameError.style.display = "block";
                return false;
            }
        } else {
            newCompanyInput.style.display = "none";
        }

        companyNameError.textContent = "Please provide Company Name.";
        companyNameError.style.display = "none";
        return true;
    }

    function validateJobName() {
        if (!jobName || jobName.value.trim() === "") {
            jobNameError.style.display = "block";
            return false;
        }
        jobNameError.style.display = "none";
        return true;
    }

    function validateJobType() {
        if (!jobType || jobType.value.trim() === "") {
            jobTypeError.style.display = "block";
            return false;
        }
        jobTypeError.style.display = "none";
        return true;
    }

    function validateNoc() {
        if (!nocInput || nocInput.value.trim() === "") {
            nocError.style.display = "block";
            return false;
        }
        nocError.style.display = "none";
        return true;
    }

    function validatePrpcPurchase() {
        if (!prpcPurchase || prpcPurchase.value.trim() === "") {
            prpcPurchaseError.style.display = "block";
            return false;
        }
        prpcPurchaseError.style.display = "none";
        return true;
    }

    function validatePrpcSell() {
        if (!prpcSell || prpcSell.value.trim() === "") {
            prpcSellError.style.display = "block";
            return false;
        }
        prpcSellError.style.display = "none";
        return true;
    }

    function validateCylinderDiameter() {
        if (!cylinderDiameter || cylinderDiameter.value.trim() === "") {
            if (cylinderDiameterError) cylinderDiameterError.style.display = "block";
            return false;
        }
        if (cylinderDiameterError) cylinderDiameterError.style.display = "none";
        return true;
    }

    function validateCylinderHeight() {
        if (!cylinderHeight || cylinderHeight.value.trim() === "") {
            if (cylinderHeightError) cylinderHeightError.style.display = "block";
            return false;
        }
        if (cylinderHeightError) cylinderHeightError.style.display = "none";
        return true;
    }

    function validateCylinderMadeIn() {
        if (!cylinderMadeIn) return true;

        const value = cylinderMadeIn.value.trim();

        if (value === "") {
            cylinderMadeInError.style.display = "block";
            cylinderMadeInOther.style.display = "none";
            return false;
        }

        if (value === "others") {
            cylinderMadeInOther.style.display = "block";
            if (cylinderMadeInOther.value.trim() === "") {
                cylinderMadeInError.textContent = "Please provide Cylinder Made In company name.";
                cylinderMadeInError.style.display = "block";
                return false;
            }
        } else {
            cylinderMadeInOther.style.display = "none";
        }

        cylinderMadeInError.textContent = "Please provide Cylinder Made In";
        cylinderMadeInError.style.display = "none";
        return true;
    }

    function validateCylinderDate() {
        if (!cylinderDate || cylinderDate.value.trim() === "") {
            cylinderDateError.style.display = "block";
            return false;
        }
        cylinderDateError.style.display = "none";
        return true;
    }

    function validateCylinderBillNo() {
        if (!cylinderBillNo || cylinderBillNo.value.trim() === "") {
            cylinderBillNoError.style.display = "block";
            return false;
        }
        cylinderBillNoError.style.display = "none";
        return true;
    }

    function validatePouchDiameter() {
        if (!pouchDiameter || pouchDiameter.value.trim() === "") {
            pouchDiameterError.style.display = "block";
            return false;
        }
        pouchDiameterError.style.display = "none";
        return true;
    }

    function validatePouchHeight() {
        if (!pouchHeight || pouchHeight.value.trim() === "") {
            pouchHeightError.style.display = "block";
            return false;
        }
        pouchHeightError.style.display = "none";
        return true;
    }

    function validatePouchOpenDiameter() {
        if (!pouchOpenDiameter || pouchOpenDiameter.value.trim() === "") {
            pouchOpenDiameterError.style.display = "block";
            return false;
        }
        pouchOpenDiameterError.style.display = "none";
        return true;
    }

    function validatePouchOpenHeight() {
        if (!pouchOpenHeight || pouchOpenHeight.value.trim() === "") {
            pouchOpenHeightError.style.display = "block";
            return false;
        }
        pouchOpenHeightError.style.display = "none";
        return true;
    }

    function validatePouchCombination1() {
        if (!pouchCombination1 || pouchCombination1.value.trim() === "") {
            pouchCombination1Error.style.display = "block";
            return false;
        }
        pouchCombination1Error.style.display = "none";
        return true;
    }

    function validatePouchCombination2() {
        if (!pouchCombination2 || pouchCombination2.value.trim() === "") {
            pouchCombination2Error.style.display = "block";
            return false;
        }
        pouchCombination2Error.style.display = "none";
        return true;
    }

    function validateJobStatus() {
        if (!jobStatus || jobStatus.value.trim() === "") {
            if (jobStatusError) jobStatusError.style.display = "block";
            return false;
        }
        if (jobStatusError) jobStatusError.style.display = "none";
        return true;
    }

    // ---------- FORM VALIDATION WRAPPER ----------

    function validateForm() {
        const vJobDate          = validateJobDate();
        const vInvoice          = validateInvoiceNo();
        const vCompany          = validateCompanyName();

        const vJobName          = validateJobName();
        const vJobType          = validateJobType();
        const vNoc              = validateNoc();

        const vPrpcPurchase     = validatePrpcPurchase();
        const vPrpcSell         = validatePrpcSell();
        const vCylDia           = validateCylinderDiameter();
        const vCylHeight        = validateCylinderHeight();
        const vCylMadeIn        = validateCylinderMadeIn();
        const vCylDate          = validateCylinderDate();
        const vCylBill          = validateCylinderBillNo();

        const vPouchDia         = validatePouchDiameter();
        const vPouchHeight      = validatePouchHeight();
        const vPouchOpenDia     = validatePouchOpenDiameter();
        const vPouchOpenHeight  = validatePouchOpenHeight();
        const vPouchComb1       = validatePouchCombination1();
        const vPouchComb2       = validatePouchCombination2();

        const vJobStatus        = validateJobStatus();

        return (
            vJobDate &&
            vInvoice &&
            vCompany &&
            vJobName &&
            vJobType &&
            vNoc &&
            vPrpcPurchase &&
            vPrpcSell &&
            vCylDia &&
            vCylHeight &&
            vCylMadeIn &&
            vCylDate &&
            vCylBill &&
            vPouchDia &&
            vPouchHeight &&
            vPouchOpenDia &&
            vPouchOpenHeight &&
            vPouchComb1 &&
            vPouchComb2 &&
            vJobStatus
        );
    }

    // ---------- LIVE VALIDATION EVENTS ----------

    if (jobDate) jobDate.addEventListener("change", validateJobDate);
    if (billInput) billInput.addEventListener("input", validateInvoiceNo);

    if (companyName) companyName.addEventListener("change", validateCompanyName);
    if (newCompanyInput) newCompanyInput.addEventListener("input", validateCompanyName);

    if (jobName) jobName.addEventListener("change", validateJobName);
    if (jobType) jobType.addEventListener("change", validateJobType);
    if (nocInput) nocInput.addEventListener("input", validateNoc);

    if (prpcPurchase) prpcPurchase.addEventListener("input", validatePrpcPurchase);
    if (prpcSell) prpcSell.addEventListener("input", validatePrpcSell);

    if (cylinderDiameter) cylinderDiameter.addEventListener("input", validateCylinderDiameter);
    if (cylinderHeight) cylinderHeight.addEventListener("input", validateCylinderHeight);
    if (cylinderMadeIn) cylinderMadeIn.addEventListener("change", validateCylinderMadeIn);
    if (cylinderMadeInOther) cylinderMadeInOther.addEventListener("input", validateCylinderMadeIn);
    if (cylinderDate) cylinderDate.addEventListener("change", validateCylinderDate);
    if (cylinderBillNo) cylinderBillNo.addEventListener("input", validateCylinderBillNo);

    if (pouchDiameter) pouchDiameter.addEventListener("input", validatePouchDiameter);
    if (pouchHeight) pouchHeight.addEventListener("input", validatePouchHeight);
    if (pouchOpenDiameter) pouchOpenDiameter.addEventListener("input", validatePouchOpenDiameter);
    if (pouchOpenHeight) pouchOpenHeight.addEventListener("input", validatePouchOpenHeight);
    if (pouchCombination1) pouchCombination1.addEventListener("input", validatePouchCombination1);
    if (pouchCombination2) pouchCombination2.addEventListener("input", validatePouchCombination2);

    if (jobStatus) jobStatus.addEventListener("change", validateJobStatus);

    // ---------- FORM SUBMIT ----------

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
            const firstError = document.querySelector(".invalid-feedback[style*='display: block']");
            if (firstError) {
                firstError.scrollIntoView({ behavior: "smooth", block: "center" });
            }
        }
    });
});
