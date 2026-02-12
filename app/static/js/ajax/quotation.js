// ---------------- GLOBAL CONTROL ----------------
let ajaxTimer = null;
let ajaxRunning = false;

// ---------------- MAIN FUNCTION ----------------
function runPouchAjax() {

    clearTimeout(ajaxTimer);

    ajaxTimer = setTimeout(function () {

        const party = $("#party_name").val();
        if (!party || ajaxRunning) return;

        ajaxRunning = true;
        console.log("🔥 AJAX RUNNING FOR:", party);

        // ---------- PARTY EMAIL & CONTACT ----------
        $.ajax({
            url: pouchRateAjaxUrl,
            type: "GET",
            data: { party_name: party },
            success: function (response) {

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
            },
            complete: function () {
                ajaxRunning = false;
            }
        });

        // ---------- PER JOB BLOCK ----------
        $(".job-block").each(function () {
            const block = $(this);

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

                    block.find(".per_pouch_rate_basic").val(response.per_pouch_rate_basic || 0);
                    block.find(".final_rate").val(response.final_rate || 0);
                    // block.find(".minimum_quantity").val(response.minimum_quantity || 0);

                    // JOB SELECT
                    if (response.jobs?.length) {
                        const jobSelect = block.find(".job_name");
                        const prevJob = jobSelect.val();

                        jobSelect.empty().append('<option value="">Select Job Name</option>');
                        response.jobs.forEach(j => {
                            jobSelect.append(`<option value="${j.job_name}">${j.job_name}</option>`);
                        });
                        jobSelect.append('<option value="others">Others</option>');
                        if (prevJob) jobSelect.val(prevJob);
                    }
                }
            });
        });

    }, 200); // debounce
}

// ---------------- EVENT BINDINGS ----------------

// Party select
$(document).on("change", "#party_name", runPouchAjax);

// Input fields
$(document).on(
    "input",
    ".purchase_rate_per_kg, .no_of_pouch_kg, .purchase_rate_unit, .pouch_charge, .zipper_cost",
    runPouchAjax
);

// ---------------- PAGE LOAD TRIGGER ----------------
$(document).ready(function () {
    runPouchAjax(); // 🔥 fires on page load
});
