$(document).on(
    "input change",
    "#purchase_rate, #no_of_pouch_kg, #party_name, #purchase_rate_unit, #per_pouch_rate_basic, #pouch_charge, #zipper_cost",
    function () {
        $.ajax({
            url: pouchRateAjaxUrl,
            type: "GET",
            data: {
                party_name : $("#party_name").val(),
                purchase_rate: $("#purchase_rate").val(),
                no_of_pouch_kg: $("#no_of_pouch_kg").val(),
                purchase_rate_unit: $("#purchase_rate_unit").val(),
                per_pouch_rate_basic: $("#per_pouch_rate_basic").val(),
                pouch_charge: $("#pouch_charge").val(),
                zipper_cost: $("#zipper_cost").val(),
            },
            success: function (response) {

                $("#per_pouch_rate_basic").val(response.per_pouch_rate_basic || 0);
                $("#final_rare").val(response.final_rare || 0);
                $("#minium_quantity").val(response.minium_quantity || 0);


                if (response.jobs) {
                    let jobSelect = $("#job_name");

                    jobSelect.empty();
                    jobSelect.append('<option value="">Select Job Name</option>');

                    $.each(response.jobs, function (i, job) {
                        jobSelect.append(
                            '<option value="' + job.job_name + '">' + job.job_name + "</option>"
                        );
                    });

                    jobSelect.append('<option value="others">Others</option>');
                }
            }

        });
    }
);
