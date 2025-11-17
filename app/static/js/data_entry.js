$(document).on(
    "input",
    "[name='cylinder_diameter[]'], [name='cylinder_height[]']",
    function () {
        const section = $(this).closest(".col-12"); // parent container for each row
        const height = section.find("[name='cylinder_height[]']").val();
        const diameter = section.find("[name='cylinder_diameter[]']").val();

        if (height && diameter) {
            // If both diameter and height are provided, store the formatted size
            const cylinderSize = `${diameter} x ${height}`;
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

const mySelect = document.getElementById("company_name");
const new_company = document.getElementById("new_company");

const cylinder_select = document.getElementById("cylinder_made_in");
const new_company_cylinder = document.getElementById(
    "cylinder_made_in_company_name"
);
const otherCompanyError = document.getElementById("otherCompanyError");

if (cylinder_select && new_company_cylinder) {
    cylinder_select.addEventListener("change", function () {
        if (this.value === "others") {
            new_company_cylinder.style.display = "block";
            new_company_cylinder.focus();

            if (otherCompanyError) {
                otherCompanyError.style.display = "none";
            }
        } else {
            new_company_cylinder.style.display = "none";
            new_company_cylinder.value = "";
            if (otherCompanyError) {
                otherCompanyError.style.display = "none";
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const Cylinder_Bill_no = document.getElementById("cylinder_bill_no");
    const Cylinder_Bill_no_Error = document.getElementById(
        "cylinder_bill_no_error"
    );

    const Cylinder_Date_Input = document.getElementById("cylinder_dates");
    const Cylinder_Date_Error = document.getElementById("cylinder_date_error");

    const JobInput = document.getElementById("job_date");
    const JobError = document.getElementById("job_date_error");

    const BillInput = document.getElementById("bill_no");
    const BillError = document.getElementById("bill_no_error");

    const CompanyInput = document.getElementById("company_name");
    const CompanyError = document.getElementById("company_name_error");

    const Job_Name_Input = document.getElementById("job_name");

    const new_job_name = document.getElementById("new_job_name");
    const Job_Name_Error = document.getElementById("job_name_error");

    const Job_Type_Input = document.getElementById("job_type");
    const Job_Type_Error = document.getElementById("job_type_error");

    const NOC_Input = document.getElementById("noc");
    const NOC_Error = document.getElementById("noc_error");

    const prpc_purchase_Input = document.getElementById("prpc_purchase");
    const prpc_purchase_Error = document.getElementById("prpc_purchase_error");

    const prpc_sell_Input = document.getElementById("prpc_sell");
    const prpc_sell_Error = document.getElementById("prpc_sell_error");

    const cylinder_diameter_Input =
        document.getElementById("cylinder_diameter");
    const cylinder_diameter_Error = document.getElementById(
        "cylinder_diameter_error"
    );

    const cylinder_height_Input = document.getElementById("cylinder_height");
    const cylinder_height_Error = document.getElementById(
        "cylinder_height_error"
    );

    const pouch_diameter_Input = document.getElementById("pouch_diameter");
    const pouch_diameter_Error = document.getElementById(
        "pouch_diameter_error"
    );

    const pouch_height_Input = document.getElementById("pouch_height");
    const pouch_height_Error = document.getElementById("pouch_height_error");

    const pouch_open_diameter_Input = document.getElementById(
        "pouch_open_diameter"
    );
    const pouch_open_diameter_Error = document.getElementById(
        "pouch_open_diameter_error"
    );

    const pouch_open_height_Input =
        document.getElementById("pouch_open_height");
    const pouch_open_height_Error = document.getElementById(
        "pouch_open_height_error"
    );

    const cylinder_made_in_Input = document.getElementById("cylinder_made_in");
    const cylinder_made_in_Error = document.getElementById(
        "cylinder_made_in_error"
    );

    const pouch_combination1_Input =
        document.getElementById("pouch_combination1");
    const pouch_combination1_Error = document.getElementById(
        "pouch_combination1_error"
    );

    const pouch_combination2_Input =
        document.getElementById("pouch_combination2");
    const pouch_combination2_Error = document.getElementById(
        "pouch_combination2_error"
    );

    const myForm = document.getElementById("job_detail_form");

    function validateCompany() {
        if (CompanyInput && CompanyError) {
            if (CompanyInput.value === "other") {
                if (new_company && new_company.value.trim() === "") {
                    CompanyError.style.display = "block";
                    return false;
                } else {
                    CompanyError.style.display = "none";
                    return true;
                }
            } else if (CompanyInput.value.trim() === "") {
                CompanyError.style.display = "block";
                return false;
            } else {
                CompanyError.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validateJobName() {
        if (Job_Name_Input && Job_Name_Error) {
            if (Job_Name_Input.value === "others") {
                if (new_job_name && new_job_name.value.trim() === "") {
                    Job_Name_Error.style.display = "block";
                    return false;
                } else {
                    Job_Name_Error.style.display = "none";
                    return true;
                }
            } else if (Job_Name_Input.value.trim() === "") {
                Job_Name_Error.style.display = "block";
                return false;
            } else {
                Job_Name_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }
    if (Job_Name_Input) {
        Job_Name_Input.addEventListener("change", function () {
            if (this.value === "others") {
                new_job_name.style.display = "block";
                new_job_name.focus();
                Job_Name_Error.style.display = "none";
            } else {
                new_job_name.style.display = "none";
                new_job_name.value = "";
                Job_Name_Error.style.display = "none";
            }
        });
    }
    function validateJob() {
        if (JobInput && JobError) {
            if (JobInput.value.trim() === "") {
                JobError.style.display = "block";
                return false;
            } else {
                JobError.style.display = "none";
                return true;
            }
        }
        return true;
    }

    if (CompanyInput) {
        CompanyInput.addEventListener("change", function () {
            if (this.value === "other") {
                new_company.style.display = "block";
                new_company.focus();
                CompanyError.style.display = "none";
            } else {
                new_company.style.display = "none";
                new_company.value = "";
                CompanyError.style.display = "none";
            }
        });
    }

    function validateCylinderBillNo() {
        if (Cylinder_Bill_no && Cylinder_Bill_no_Error) {
            if (Cylinder_Bill_no.value.trim() === "") {
                Cylinder_Bill_no_Error.style.display = "block";
                return false;
            } else {
                Cylinder_Bill_no_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validateCylinderDate() {
        if (Cylinder_Date_Input && Cylinder_Date_Error) {
            if (Cylinder_Date_Input.value.trim() === "") {
                Cylinder_Date_Error.style.display = "block";
                return false;
            } else {
                Cylinder_Date_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validateBill() {
        if (BillInput && BillError) {
            if (BillInput.value.trim() === "") {
                BillError.style.display = "block";
                return false;
            } else {
                BillError.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validateCompany() {
        if (CompanyInput && CompanyError) {
            if (CompanyInput.value === "other") {
                const newCompanyInput = document.getElementById("new_company");
                if (newCompanyInput && newCompanyInput.value.trim() === "") {
                    CompanyError.style.display = "block";
                    return false;
                } else {
                    CompanyError.style.display = "none";
                    return true;
                }
            } else if (CompanyInput.value.trim() === "") {
                CompanyError.style.display = "block";
                return false;
            } else {
                CompanyError.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validateJobName() {
        if (Job_Name_Input && Job_Name_Error) {
            if (Job_Name_Input.value === "others") {
                const newJobInput = document.getElementById("new_job_name");
                if (newJobInput && newJobInput.value.trim() === "") {
                    Job_Name_Error.style.display = "block";
                    return false;
                } else {
                    Job_Name_Error.style.display = "none";
                    return true;
                }
            } else if (Job_Name_Input.value.trim() === "") {
                Job_Name_Error.style.display = "block";
                return false;
            } else {
                Job_Name_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validateJobType() {
        if (Job_Type_Input && Job_Type_Error) {
            if (Job_Type_Input.value.trim() === "") {
                Job_Type_Error.style.display = "block";
                return false;
            } else {
                Job_Type_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validateNOC() {
        if (NOC_Input && NOC_Error) {
            if (NOC_Input.value.trim() === "") {
                NOC_Error.style.display = "block";
                return false;
            } else {
                NOC_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validatePrpcPurchase() {
        if (prpc_purchase_Input && prpc_purchase_Error) {
            if (prpc_purchase_Input.value.trim() === "") {
                prpc_purchase_Error.style.display = "block";
                return false;
            } else {
                prpc_purchase_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validatePrpcSell() {
        if (prpc_sell_Input && prpc_sell_Error) {
            if (prpc_sell_Input.value.trim() === "") {
                prpc_sell_Error.style.display = "block";
                return false;
            } else {
                prpc_sell_Error.style.display = "none";
                return true;
            }
        }
        return true;
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

    function validatePouchDiameter() {
        if (pouch_diameter_Input && pouch_diameter_Error) {
            if (pouch_diameter_Input.value.trim() === "") {
                pouch_diameter_Error.style.display = "block";
                return false;
            } else {
                pouch_diameter_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validatePouchHeight() {
        if (pouch_height_Input && pouch_height_Error) {
            if (pouch_height_Input.value.trim() === "") {
                pouch_height_Error.style.display = "block";
                return false;
            } else {
                pouch_height_Error.style.display = "none";
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

    function validateCylinderMade() {
        if (cylinder_made_in_Input && cylinder_made_in_Error) {
            if (cylinder_made_in_Input.value === "others") {
                const newCylinderCompanyInput = document.getElementById(
                    "cylinder_made_in_company_name"
                );
                if (
                    newCylinderCompanyInput &&
                    newCylinderCompanyInput.value.trim() === ""
                ) {
                    cylinder_made_in_Error.style.display = "block";
                    return false;
                } else {
                    cylinder_made_in_Error.style.display = "none";
                    return true;
                }
            } else if (cylinder_made_in_Input.value.trim() === "") {
                cylinder_made_in_Error.style.display = "block";
                return false;
            } else {
                cylinder_made_in_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validatePouchCombination1() {
        if (pouch_combination1_Input && pouch_combination1_Error) {
            if (pouch_combination1_Input.value.trim() === "") {
                pouch_combination1_Error.style.display = "block";
                return false;
            } else {
                pouch_combination1_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validatePouchCombination2() {
        if (pouch_combination2_Input && pouch_combination2_Error) {
            if (pouch_combination2_Input.value.trim() === "") {
                pouch_combination2_Error.style.display = "block";
                return false;
            } else {
                pouch_combination2_Error.style.display = "none";
                return true;
            }
        }
        return true;
    }

    function validateForm() {
        const validators = [
            validateCylinderBillNo(),
            validateCylinderDate(),
            validateJob(),
            validateBill(),
            validateCompany(),
            validateJobName(),
            validateJobType(),
            validateNOC(),
            validatePrpcPurchase(),
            validatePrpcSell(),
            validateCylinderDiameter(),
            validateCylinderHeight(),
            validatePouchDiameter(),
            validatePouchHeight(),
            validatePouchOpenDiameter(),
            validatePouchOpenHeight(),
            validateCylinderMade(),
            validatePouchCombination1(),
            validatePouchCombination2(),
        ];

        return validators.every((isValid) => isValid);
    }

    if (Cylinder_Bill_no) {
        Cylinder_Bill_no.addEventListener("input", validateCylinderBillNo);
        Cylinder_Bill_no.addEventListener("blur", validateCylinderBillNo);
    }

    if (Cylinder_Date_Input) {
        Cylinder_Date_Input.addEventListener("input", validateCylinderDate);
        Cylinder_Date_Input.addEventListener("blur", validateCylinderDate);
    }

    if (JobInput) {
        JobInput.addEventListener("input", validateJob);
        JobInput.addEventListener("blur", validateJob);
    }

    if (BillInput) {
        BillInput.addEventListener("input", validateBill);
        BillInput.addEventListener("blur", validateBill);
    }

    if (CompanyInput) {
        CompanyInput.addEventListener("input", validateCompany);
        CompanyInput.addEventListener("blur", validateCompany);
    }

    if (Job_Name_Input) {
        Job_Name_Input.addEventListener("input", validateJobName);
        Job_Name_Input.addEventListener("blur", validateJobName);
    }

    if (Job_Type_Input) {
        Job_Type_Input.addEventListener("input", validateJobType);
        Job_Type_Input.addEventListener("blur", validateJobType);
    }

    if (NOC_Input) {
        NOC_Input.addEventListener("input", validateNOC);
        NOC_Input.addEventListener("blur", validateNOC);
    }

    if (prpc_purchase_Input) {
        prpc_purchase_Input.addEventListener("input", validatePrpcPurchase);
        prpc_purchase_Input.addEventListener("blur", validatePrpcPurchase);
    }

    if (prpc_sell_Input) {
        prpc_sell_Input.addEventListener("input", validatePrpcSell);
        prpc_sell_Input.addEventListener("blur", validatePrpcSell);
    }

    if (cylinder_diameter_Input) {
        cylinder_diameter_Input.addEventListener(
            "input",
            validateCylinderDiameter
        );
        cylinder_diameter_Input.addEventListener(
            "blur",
            validateCylinderDiameter
        );
    }

    if (cylinder_height_Input) {
        cylinder_height_Input.addEventListener("input", validateCylinderHeight);
        cylinder_height_Input.addEventListener("blur", validateCylinderHeight);
    }

    if (pouch_diameter_Input) {
        pouch_diameter_Input.addEventListener("input", validatePouchDiameter);
        pouch_diameter_Input.addEventListener("blur", validatePouchDiameter);
    }

    if (pouch_height_Input) {
        pouch_height_Input.addEventListener("input", validatePouchHeight);
        pouch_height_Input.addEventListener("blur", validatePouchHeight);
    }

    if (pouch_open_diameter_Input) {
        pouch_open_diameter_Input.addEventListener(
            "input",
            validatePouchOpenDiameter
        );
        pouch_open_diameter_Input.addEventListener(
            "blur",
            validatePouchOpenDiameter
        );
    }

    if (pouch_open_height_Input) {
        pouch_open_height_Input.addEventListener(
            "input",
            validatePouchOpenHeight
        );
        pouch_open_height_Input.addEventListener(
            "blur",
            validatePouchOpenHeight
        );
    }

    if (cylinder_made_in_Input) {
        cylinder_made_in_Input.addEventListener("input", validateCylinderMade);
        cylinder_made_in_Input.addEventListener("blur", validateCylinderMade);
    }

    if (pouch_combination1_Input) {
        pouch_combination1_Input.addEventListener(
            "input",
            validatePouchCombination1
        );
        pouch_combination1_Input.addEventListener(
            "blur",
            validatePouchCombination1
        );
    }

    const newCompanyInput = document.getElementById("new_company");
    const newJobNameInput = document.getElementById("new_job_name");
    const newCylinderCompanyInput = document.getElementById(
        "cylinder_made_in_company_name"
    );

    if (newCompanyInput) {
        newCompanyInput.addEventListener("input", validateCompany);
        newCompanyInput.addEventListener("blur", validateCompany);
    }

    if (newJobNameInput) {
        newJobNameInput.addEventListener("input", validateJobName);
        newJobNameInput.addEventListener("blur", validateJobName);
    }

    if (newCylinderCompanyInput) {
        newCylinderCompanyInput.addEventListener("input", validateCylinderMade);
        newCylinderCompanyInput.addEventListener("blur", validateCylinderMade);
    }

    if (myForm) {
        const loaderOverlay = document.getElementById("loader-overlay");

        myForm.addEventListener("submit", function (event) {
            event.preventDefault();

            if (validateForm()) {
                if (loaderOverlay) {
                    loaderOverlay.style.display = "flex";
                }

                requestAnimationFrame(() => {
                    myForm.submit();
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
    }
});
