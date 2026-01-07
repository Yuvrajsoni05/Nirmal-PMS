$(document).on(
    "input change",
    "#party_name, .purchase_rate_per_kg, .no_of_pouch_kg, .purchase_rate_unit, .pouch_charge, .zipper_cost",
    function () {

        const isPartyChange = $(this).attr("id") === "party_name";

        // If PARTY changed → update ALL JOB TYPES
        if (isPartyChange) {

            $(".job-block, .job-block_data").each(function () {
                runAjax($(this));
            });

            return;
        }

        // Otherwise update ONLY current block
        const block = $(this).closest(".job-block, .job-block_data");

        if (block.length) runAjax(block);
    }
);


function runAjax(block) {

    $.ajax({
        url: pouchRateAjaxUrl,
        type: "GET",

        data: {
            party_name: $("#party_name").val(),

            purchase_rate_per_kg: block.find(".purchase_rate_per_kg").val(),
            no_of_pouch_kg: block.find(".no_of_pouch_kg").val(),
            purchase_rate_unit: block.find(".purchase_rate_unit").val(),

            pouch_charge: block.find(".pouch_charge").val(),
            zipper_cost: block.find(".zipper_cost").val(),
        },

        success: function (response) {

            block.find(".per_pouch_rate_basic")
                 .val(response.per_pouch_rate_basic || 0);

            block.find(".final_rare, .final_rate")
                 .val(response.final_rare || 0);

            block.find(".minimum_quantity")
                 .val(response.minimum_quantity || 0);


            // -------- JOB NAME DROPDOWN --------
            let jobSelect = block.find(".job_name");

            if (jobSelect.length && jobSelect.is("select")) {

                let prev = jobSelect.val();

                jobSelect.empty()
                    .append('<option value="">Select Job Name</option>');

                $.each(response.jobs || [], function (i, job) {
                    jobSelect.append(
                        '<option value="' + job.job_name + '">' +
                        job.job_name +
                        '</option>'
                    );
                });

                jobSelect.append('<option value="others">Others</option>');

                if (jobSelect.find("option[value='" + prev + "']").length)
                    jobSelect.val(prev);
            }
        },

        error: function (xhr) {
            console.log("AJAX ERROR:", xhr.responseText);
        }
    });
}
