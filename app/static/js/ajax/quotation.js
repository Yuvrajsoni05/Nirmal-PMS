$(document).on(
    "input change",
    "#party_name, .party_email, .purchase_rate_per_kg, .no_of_pouch_kg, .purchase_rate_unit, .pouch_charge, .zipper_cost",
    function () {
        const party = $("#party_name").val();

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
                    block.find(".final_rare").val(response.final_rare || 0);
                    block.find(".minimum_quantity").val(response.minimum_quantity || 0);

                    // Preserve party_email selection
                    const $partyEmail = $("#party_email");
                    const prevEmailValue = $partyEmail.val();

                    $partyEmail.empty().append('<option value="">Select Party Email</option>');

                    if (response.party_emails && response.party_emails.length) {
                        $.each(response.party_emails, function (i, email) {
                            $partyEmail.append(
                                $('<option></option>').val(email.email).text(email.email)
                            );
                        });
                    }

                    $partyEmail.append('<option value="others">Others</option>');

                    // Restore previous selection if it still exists
                    if (prevEmailValue && $partyEmail.find("option[value='" + prevEmailValue + "']").length) {
                        $partyEmail.val(prevEmailValue);
                    }

                    // --- JOB SELECT UPDATE ---
                    if (response.jobs && response.jobs.length) {
                        let jobSelect = block.find(".job_name");
                        let prevJobValue = jobSelect.val();

                        jobSelect.empty().append('<option value="">Select Job Name</option>');

                        $.each(response.jobs, function (i, job) {
                            jobSelect.append(
                                $('<option></option>').val(job.job_name).text(job.job_name)
                            );
                        });

                        jobSelect.append('<option value="others">Others</option>');

                        if (prevJobValue && jobSelect.find("option[value='" + prevJobValue + "']").length) {
                            jobSelect.val(prevJobValue);
                        }
                    }
                },
            });
        });
    }
);
