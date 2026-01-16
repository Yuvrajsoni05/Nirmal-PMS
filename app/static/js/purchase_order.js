// ---------- POUCH SIZE (Height x Diameter) ----------
$(document).on(
    "input",
    "[name='pouch_height'], [name='pouch_diameter']",
    function () {
        const block = $(this).closest(".job-block");

        if (!block.length) return;

        const h = block.find("[name='pouch_height']").val() || "";
        const d = block.find("[name='pouch_diameter']").val() || "";

        block.find("[name='pouch_size']").val(h && d ? `${h} x ${d}` : "");
       
    }
);

// ---------- POUCH COMBINATION (L1+L2+L3+L4) ----------
$(document).on(
    "input",
    "[name='pouch_combination1'], [name='pouch_combination2'], [name='pouch_combination3'], [name='pouch_combination4']",
    function () {
        const block = $(this).closest(".job-block");

        const values = [
            block.find("[name='pouch_combination1']").val() || "0",
            block.find("[name='pouch_combination2']").val() || "0",
            block.find("[name='pouch_combination3']").val() || "0",
            block.find("[name='pouch_combination4']").val() || "0",
        ]
            .map((v) => v.trim())
            .filter((v) => v !== "");

        const combined = values.length ? values.join(" + ") : "";

        block.find("[name='pouch_combination']").val(combined);

        console.log("pouch_combination =", combined);
    }
);

document.addEventListener("DOMContentLoaded", function () {

    const partySelect = document.getElementById("party_name");
    const newParty = document.getElementById("new_party_name");
    const newPartyError = document.getElementById("new_party_error");

    partySelect.addEventListener("change", function () {
        if (this.value === "others") {
            newParty.classList.remove("d-none");
            newParty.required = true;
        } else {
            newParty.classList.add("d-none");
            newParty.required = false;
            newParty.value = "";
            newPartyError.classList.add("d-none");
        }
    });

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

// ---------- PARTY EMAIL → OTHERS ----------
$(document).on("change", "#party_email", function () {
    const newPartyEmail = $("#new_party_email");

    if ($(this).val() === "others") {
        newPartyEmail.removeClass("d-none").prop("required", true).focus();
    } else {
        newPartyEmail
            .addClass("d-none")
            .prop("required", false)
            .val("")
            .removeClass("is-invalid");
    }
});

$(document).on("input", "#new_party_email", function () {
    if ($("#party_email").val() === "others" && $(this).val().trim() === "") {
        $(this).addClass("is-invalid");
    } else {
        $(this).removeClass("is-invalid");
    }
});

// ---------- JOB NAME → OTHERS (PER JOB BLOCK) ----------

$(document).on("change", ".job-block select.job_name", function () {
    const block = $(this).closest(".job-block");
    const select = $(this);
    const newJob = block.find(".new_job_name");

    if (select.val() === "others") {
        // show input
        newJob.removeClass("d-none").prop("required", true).focus();

        // move name attr to input so it is submitted
        select.data("orig-name", select.attr("name"));
        select.removeAttr("name");

        newJob.attr("name", "job_name");
    } else {
        // hide input
        newJob
            .addClass("d-none")
            .prop("required", false)
            .val("")
            .removeClass("is-invalid");

        // give name back to select
        if (!select.attr("name")) {
            select.attr("name", select.data("orig-name"));
        }

        newJob.removeAttr("name");
    }
});

// live validation
$(document).on("input", ".job-block .new_job_name", function () {
    const block = $(this).closest(".job-block");
    const select = block.find(".job_name");

    if (select.val() === "others" && $(this).val().trim() === "") {
        $(this).addClass("is-invalid");
    } else {
        $(this).removeClass("is-invalid");
    }
});
