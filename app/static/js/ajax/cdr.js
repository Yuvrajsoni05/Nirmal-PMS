$(document).ready(function () {
    // Listen to company selection change
    $("#party_name").change(function () {
        let partyName = $(this).val();

        // Reset dropdowns function
        function resetDropdowns() {
            $("#job_name")
                .empty()
                .append('<option value="">Select Job</option>')
                .append('<option value="others">Other</option>');

            $("#party_email")
                .empty()
                .append('<option value="">Select Company Email</option>')
                .append('<option value="other">Other</option>');

            $("#party_contact_used")
                .empty()
                .append('<option value="">Select Contact Number</option>')
                .append('<option value="others">Other</option>');
        }

        if (!partyName) {
            resetDropdowns();
            return;
        }

        // AJAX call
        $.ajax({
            url: cdrAjaxUrl,  // use URL passed from template
            data: { party_name: partyName },
            success: function (data) {
                resetDropdowns();  // reset before populating

                // Populate Party Contact
                if (data.contact && data.contact.length > 0) {
                    $.each(data.contact, function (index, contact) {
                        $("#party_contact_used").append(
                            '<option value="' +
                                contact.party_contacts__party_number +
                                '">' +
                                contact.party_contacts__party_number +
                                "</option>"
                        );
                    });
                }

                // Populate Company Email
                if (data.email && data.email.length > 0) {
                    $.each(data.email, function (index, email) {
                        $("#party_email").append(
                            '<option value="' +
                                email.party_emails__email +
                                '">' +
                                email.party_emails__email +
                                "</option>"
                        );
                    });
                }

                // Populate Job Names
                if (data.jobs && data.jobs.length > 0) {
                    $.each(data.jobs, function (index, job) {
                        $("#job_name").append(
                            '<option value="' +
                                job.job_name +
                                '">' +
                                job.job_name +
                                "</option>"
                        );
                    });
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX Error:", error);
                resetDropdowns();
            },
        });
    });
});