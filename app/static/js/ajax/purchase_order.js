$(document).on(
    "input change",
    "#party_name, .party_email, .purchase_rate_per_kg, .no_of_pouch_kg, .purchase_rate_unit, .pouch_charge, .zipper_cost",
    function () {

        const isPartyChange = $(this).attr("id") === "party_name";

        if (isPartyChange) {
            $(".job-block, .job-block_data").each(function () {
                runAjax($(this), true);   
            });
            return;
        }

        const block = $(this).closest(".job-block, .job-block_data");
        if (block.length) runAjax(block, false);
    }
);


function runAjax(block, isPartyChange = false) {
    $.ajax({
        url: pouchRateAjaxUrl,
        type: "GET",
        data: {
            party_name: $("#party_name").val(),
            per_pouch_rate_basic: block.find(".per_pouch_rate_basic").val(),
            purchase_rate_per_kg: block.find(".purchase_rate_per_kg").val(),
            no_of_pouch_kg: block.find(".no_of_pouch_kg").val(),
            purchase_rate_unit: block.find(".purchase_rate_unit").val(),
            pouch_charge: block.find(".pouch_charge").val(),
            zipper_cost: block.find(".zipper_cost").val(),
        },

        success: function (response) {

            /* ---------- RATE FIELDS ---------- */
            block.find(".per_pouch_rate_basic").val(response.per_pouch_rate_basic || 0);
            block.find(".final_rate").val(response.final_rate || 0);
            block.find(".minimum_quantity").val(response.minimum_quantity || 0);

            /* ---------- PARTY EMAIL (ONLY ON PARTY CHANGE) ---------- */
            if (isPartyChange) {
                const $partyEmail = $("#party_email");
                const prevEmailValue = $partyEmail.val();

                $partyEmail.empty().append('<option value="">Select Party Email</option>');

                if (response.party_emails?.length) {
                    response.party_emails.forEach(email => {
                        $partyEmail.append(
                            $('<option></option>').val(email.email).text(email.email)
                        );
                    });
                }

                $partyEmail.append('<option value="others">Others</option>');

                if (
                    prevEmailValue &&
                    $partyEmail.find(`option[value="${prevEmailValue}"]`).length
                ) {
                    $partyEmail.val(prevEmailValue);
                }
            }


            const $partyContact = $("#party_contact");
            const prevContactValue = $partyContact.val();

            $partyContact.empty().append('<option value="">Select Party Contact</option>');

            if (response.party_contacts?.length) {
                response.party_contacts.forEach(contact => {
                    $partyContact.append(
                        $('<option></option>').val(contact.party_number).text(contact.party_number)
                    );
                });
            }

            $partyContact.append('<option value="others">Others</option>');

            if (prevContactValue && $partyContact.find(`option[value="${prevContactValue}"]`).length) {
                $partyContact.val(prevContactValue);
            }

            /* ---------- JOB NAME ---------- */
            let jobSelect = block.find(".job_name");

            if (jobSelect.length && jobSelect.is("select")) {
                let prev = jobSelect.val();

                jobSelect.empty().append('<option value="">Select Job Name</option>');

                (response.jobs || []).forEach(job => {
                    jobSelect.append(`<option value="${job}">${job}</option>`);
                });

                jobSelect.append('<option value="others">Others</option>');

                if (jobSelect.find(`option[value="${prev}"]`).length) {
                    jobSelect.val(prev);
                }
            }
        },

        error: function (xhr) {
            console.log("AJAX ERROR:", xhr.responseText);
        },
    });
}
