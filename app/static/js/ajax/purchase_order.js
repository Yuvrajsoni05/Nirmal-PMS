$(document).on(
    "input change",
    "#party_name, .purchase_rate_per_kg, .no_of_pouch_kg, .purchase_rate_unit, .pouch_charge, .zipper_cost",
    function () {

        const party = $("#party_name").val();

      
        const block = $(this).closest(".job-block");

      
        if (!block.length) return;

        $.ajax({
            url: pouchRateAjaxUrl,
            type: "GET",
            data: {
                party_name: party,
                purchase_rate_per_kg: block.find(".purchase_rate_per_kg").val(),
                no_of_pouch_kg: block.find(".no_of_pouch_kg").val(),
                purchase_rate_unit: block.find(".purchase_rate_unit").val(),
                pouch_charge: block.find(".pouch_charge").val(),
                zipper_cost: block.find(".zipper_cost").val(),
            },

            success: function (response) {

                block.find(".per_pouch_rate_basic")
                    .val(response.per_pouch_rate_basic || 0);

                block.find(".final_rare, .final_rate")   // (works even if class name differs)
                    .val(response.final_rare || 0);

                block.find(".minimum_quantity")
                    .val(response.minimum_quantity || 0);

                // --- JOB SELECT UPDATE ---
                if (response.jobs && response.jobs.length) {

                    let jobSelect = block.find(".job_name");
                    let prevValue = jobSelect.val();

                    jobSelect.empty()
                        .append('<option value="">Select Job Name</option>');

                    $.each(response.jobs, function (i, job) {
                        jobSelect.append(
                            '<option value="' + job.job_name + '">' +
                            job.job_name +
                            '</option>'
                        );
                    });

                    jobSelect.append('<option value="others">Others</option>');

                    // Restore selected value (if still exists)
                    if (jobSelect.find("option[value='" + prevValue + "']").length) {
                        jobSelect.val(prevValue);
                    }
                }
            },

            error: function (xhr) {
                console.log(xhr.responseText);
            }
        });
    }
);
