// ---------- POUCH SIZE (Height x Diameter) ----------
$(document).on(
    "input",
    "[name='pouch_height[]'], [name='pouch_diameter[]']",
    function () {
        const block = $(this).closest(".job-block");

        const h = block.find("[name='pouch_height[]']").val();
        const d = block.find("[name='pouch_diameter[]']").val();

        if (h && d) {
            block.find("[name='pouch_size[]']").val(`${h} x ${d}`);
        } else {
            block.find("[name='pouch_size[]']").val("");
        }
    }
);

// ---------- POUCH COMBINATION (L1+L2+L3+L4) ----------
$(document).on(
    "input",
    "[name='pouch_combination1[]'], [name='pouch_combination2[]'], [name='pouch_combination3[]'], [name='pouch_combination4[]']",
    function () {
        const block = $(this).closest(".job-block");

        const values = [
            block.find("[name='pouch_combination1[]']").val()?.trim(),
            block.find("[name='pouch_combination2[]']").val()?.trim(),
            block.find("[name='pouch_combination3[]']").val()?.trim(),
            block.find("[name='pouch_combination4[]']").val()?.trim(),
        ].filter((v) => v !== "" && v != null);

        const combined = values.length ? values.join(" + ") : "";

        block.find("[name='pouch_combination[]']").val(combined);
    }
);

// ---------- PARTY NAME → OTHERS ----------
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
            newParty.classList.add("is-invalid");
            newPartyError.classList.remove("d-none");
        } else {
            newParty.classList.remove("is-invalid");
            newPartyError.classList.add("d-none");
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

