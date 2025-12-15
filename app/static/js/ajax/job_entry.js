$("#party_name").change(function () {
    let PartyName = $(this).val();
    if (PartyName === "other") {
        $("#new_party_name").show();
    } else {
        $("#new_party_name").hide();
    }

    if (PartyName) {
        $.ajax({
            url: job_entryAjaxUrl,
            data: { party_name: PartyName },
            success: function (data) {
                $("#job_name")
                    .empty()
                    .append('<option value="">Select Job</option>');

                $.each(data.jobs, function (index, job) {
                    $("#job_name").append(
                        '<option value="' +
                            job.job_name +
                            '">' +
                            job.job_name +
                            "</option>"
                    );
                });
                $("#job_name").append('<option value="others">Other</option>');
            },
        });
    } else {
        $("#job_name")
            .empty()
            .append('<option value="">Select Job</option>')
            .append('<option value="others">Other</option>');
    }
});
