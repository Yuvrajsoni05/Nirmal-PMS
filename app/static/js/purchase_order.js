$(document).on(
    "input",
    "[name='pouch_height'], [name='pouch_diameter']",
    function () {
        const section = $(this).closest(".col-md-4");

        const pouch_open_height = section.find("[name='pouch_height']").val();

        const pouch_open_diameter = section
            .find("[name='pouch_diameter']")
            .val();

        let pouch_open_Size = "";

        if (pouch_open_height && pouch_open_diameter) {
            pouch_open_Size = `${pouch_open_height} x ${pouch_open_diameter}`;
            section.find("[name='pouch_size']").val(pouch_open_Size);
        }

        console.log(pouch_open_Size);
    }
);


$(document).on(
    "input",
    "[name='pouch_combination1'], [name='pouch_combination2'], [name='pouch_combination3'], [name='pouch_combination4']",
    function () {
        const section = $(this).closest(".col-md-8");

        const values = [
            section.find("[name='pouch_combination1']").val(),
            section.find("[name='pouch_combination2']").val(),
            section.find("[name='pouch_combination3']").val(),
            section.find("[name='pouch_combination4']").val(),
        ].filter((v) => v !== ""); // keep 0 but remove empty

        const combined = values.join("+");

        section.find("[name='pouch_combination']").val(combined);

        console.log(combined);
    }
);



// Show/Hide "New Party Name" field
document.addEventListener("DOMContentLoaded", function () {
    const partySelect = document.getElementById("party_name");
    const newParty = document.getElementById("new_party_name");
    const newPartyError = document.getElementById("new_party_error");

    partySelect.addEventListener("change", function () {
        if (this.value === "others") {
            newParty.classList.remove("d-none");
            newParty.setAttribute("required", true);
        } else {
            newParty.classList.add("d-none");
            newParty.removeAttribute("required");
            newParty.value = "";
            newPartyError.classList.add("d-none");
        }
    });

    // Validation for new party
    newParty.addEventListener("input", function () {
        if (partySelect.value === "others" && newParty.value.trim() === "") {
            newPartyError.classList.remove("d-none");
            newParty.classList.add("is-invalid");
        } else {
            newPartyError.classList.add("d-none");
            newParty.classList.remove("is-invalid");
        }
    });
});




document.addEventListener("DOMContentLoaded", function () {
    const jobSelect = document.getElementById("job_name");
    const newJob = document.getElementById("new_job_name");
    const newJobError = document.getElementById("new_job_error");

    // Show/Hide based on selection
    jobSelect.addEventListener("change", function () {
        if (this.value === "others") {
            newJob.classList.remove("d-none");
            newJob.setAttribute("required", true);
        } else {
            newJob.classList.add("d-none");
            newJob.removeAttribute("required");
            newJob.value = "";
            newJobError.classList.add("d-none");
        }
    });

    // Validation live check
    newJob.addEventListener("input", function () {
        if (jobSelect.value === "others" && newJob.value.trim() === "") {
            newJobError.classList.remove("d-none");
            newJob.classList.add("is-invalid");
        } else {
            newJobError.classList.add("d-none");
            newJob.classList.remove("is-invalid");
        }
    });
});
