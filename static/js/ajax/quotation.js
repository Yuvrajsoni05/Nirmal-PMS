$(document).on("change", "#party_name", function () {

    const party = $(this).val();

    $(".job-block").each(function () {

        const block = $(this);

        $.ajax({
            url: pouchRateAjaxUrl,
            type: "GET",
            data: {   
                
                
                party_name: party,
                // JOB-WISE VALUES
                purchase_rate_per_kg: block.find(".purchase_rate_per_kg").val(),
                no_of_pouch_kg: block.find(".no_of_pouch_kg").val(),
                purchase_rate_unit: block.find(".purchase_rate_unit").val(),
                pouch_charge: block.find(".pouch_charge").val(),
                zipper_cost: block.find(".zipper_cost").val(), },

            success: function (response) {
                block
                    .find(".per_pouch_rate_basic")
                    .val(response.per_pouch_rate_basic || 0);
                block.find(".final_rare").val(response.final_rare || 0);
                block
                    .find(".minimum_quantity")
                    .val(response.minimum_quantity || 0);

                if (response.jobs && response.jobs.length) {
                    
                    let jobSelect = block.find(".job_name");
                    let prevValue = jobSelect.val();

                    jobSelect.empty();
                    jobSelect.append('<option value="">Select Job Name</option>');

                    $.each(response.jobs, function (i, job) {
                        jobSelect.append('<option value="'+ job.job_name +'">'+ job.job_name +'</option>');
                    });

                    jobSelect.append('<option value="others">Others</option>');

                    if (jobSelect.find("option[value='"+prevValue+"']").length) {
                        jobSelect.val(prevValue);
                    }
                }
            }
        });
    });
});


$(document).on(
    "input change",
    ".purchase_rate_per_kg, .no_of_pouch_kg, #party_name, .purchase_rate_unit, .pouch_charge, .zipper_cost, .job_name",
    function () {
        const block = $(this).closest(".job-block"); // <<=== KEY POINT

        $.ajax({
            url: pouchRateAjaxUrl,
            type: "GET",

            data: {
                // GLOBAL
                party_name: $("#party_name").val(),
                
                // JOB-WISE VALUES
                purchase_rate_per_kg: block.find(".purchase_rate_per_kg").val(),
                no_of_pouch_kg: block.find(".no_of_pouch_kg").val(),
                purchase_rate_unit: block.find(".purchase_rate_unit").val(),
                pouch_charge: block.find(".pouch_charge").val(),
                zipper_cost: block.find(".zipper_cost").val(),
            },

            success: function (response) {
                block
                    .find(".per_pouch_rate_basic")
                    .val(response.per_pouch_rate_basic || 0);
                block.find(".final_rare").val(response.final_rare || 0);
                block
                    .find(".minimum_quantity")
                    .val(response.minimum_quantity || 0);

                if (response.jobs && response.jobs.length) {
                    let jobSelect = block.find(".job_name");
                    let prevValue = jobSelect.val();

                    jobSelect.empty();
                    jobSelect.append(
                        '<option value="">Select Job Name</option>'
                    );

                    $.each(response.jobs, function (i, job) {
                        jobSelect.append(
                            '<option value="' + job.job_name + '">' + job.job_name  + "</option>"
                        );
                    });

                    jobSelect.append('<option value="others">Others</option>');

                    if (
                        jobSelect.find("option[value='" + prevValue + "']")
                            .length
                    ) {
                        jobSelect.val(prevValue);
                    }
                }
            },
        });
    }
);
