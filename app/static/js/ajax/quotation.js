// ---------------- PAGE LOAD ----------------
$(document).ready(function () {
    $(".job-block").each(function () {
        runPouchAjax($(this), true);
    });
});


// ---------------- EVENT BINDINGS ----------------
$(document).on(
    "input change",
    "#party_name, .party_email, .purchase_rate_per_kg, .no_of_pouch_kg, .purchase_rate_unit, .pouch_charge, .zipper_cost",
    function () {

        const isPartyChange = $(this).attr("id") === "party_name";

        if (isPartyChange) {
            $(".job-block").each(function () {
                runPouchAjax($(this), true);
            });
            return;
        }

        const block = $(this).closest(".job-block");
        if (block.length) {
            runPouchAjax(block, false);
        }
    }
);


// ---------------- MAIN FUNCTION ----------------
function runPouchAjax(block, isPartyChange = false) {

    const party = $("#party_name").val();
    if (!party) return;

    $.ajax({
        url: pouchRateAjaxUrl,
        type: "GET",
        data: {
            party_name: party,
            per_pouch_rate_basic: block.find(".per_pouch_rate_basic").val(),
            purchase_rate_per_kg: block.find(".purchase_rate_per_kg").val(),
            no_of_pouch_kg: block.find(".no_of_pouch_kg").val(),
            purchase_rate_unit: block.find(".purchase_rate_unit").val(),
            pouch_charge: block.find(".pouch_charge").val(),
            zipper_cost: block.find(".zipper_cost").val(),
        },

        success: function (response) {

            // ---------- RATE FIELDS ----------
            block.find(".per_pouch_rate_basic").val(response.per_pouch_rate_basic || 0);
            block.find(".final_rate").val(response.final_rate || 0);


            // ---------- PARTY EMAIL & CONTACT (ONLY ON PARTY CHANGE) ----------
            if (isPartyChange) {

                // PARTY EMAIL
                const $partyEmail = $("#party_email");
                const prevEmail = $partyEmail.val();

                $partyEmail.empty().append('<option value="">Select Party Email</option>');

                response.party_emails?.forEach(e => {
                    $partyEmail.append(`<option value="${e.email}">${e.email}</option>`);
                });

                $partyEmail.append('<option value="others">Others</option>');

                if (prevEmail) $partyEmail.val(prevEmail);


                // PARTY CONTACT
                const $partyContact = $("#party_contact");
                const prevContact = $partyContact.val();

                $partyContact.empty().append('<option value="">Select Party Contact</option>');

                response.party_contacts?.forEach(c => {
                    $partyContact.append(`<option value="${c.party_number}">${c.party_number}</option>`);
                });

                $partyContact.append('<option value="others">Others</option>');

                if (prevContact) $partyContact.val(prevContact);
            }


            // ---------- JOB SELECT ----------
            // ---------- JOB SELECT ----------
            const jobSelect = block.find(".job_name");

            if (jobSelect.length) {

                const prevJob = jobSelect.val();

                jobSelect.empty().append('<option value="">Select Job Name</option>');

                response.jobs?.forEach(j => {
                    jobSelect.append(
                        `<option value="${j.job_name}">${j.job_name}</option>`
                    );
                });

                jobSelect.append('<option value="others">Others</option>');

                // Restore only if exists in new list
                if (
                    prevJob &&
                    jobSelect.find(`option[value="${prevJob}"]`).length
                ) {
                    jobSelect.val(prevJob);
                }
            }
        },

        error: function (xhr) {
            console.log("AJAX ERROR:", xhr.responseText);
        }
    });
}