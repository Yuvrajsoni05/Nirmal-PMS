$("#party_name").change(function () {
  
    let PartyName = $(this).val();
    if (PartyName) {
        $.ajax({
            url: master_dataAjaxUrl,
            data: { party_name: PartyName },
            success: function (data) {

                if(data.party_email){
                $("#party_email").empty()
                    .append('<option value="">Select Email</option>');

                $.each(data.party_email, function (index, email) {
                    $("#party_email").append(
                        '<option value="' +
                            email +
                            '">' +
                            email +
                            "</option>"
                    );
                });
                $("#party_email").append('<option value="other">Other</option>');
                }
                if(data.party_contact){
                    $("#party_contact").empty()
                    .append('<option value="">Select Contact</option>');

                $.each(data.party_contact, function (index, contact) {
                    $("#party_contact").append(
                        '<option value="' +
                            contact +
                            '">' +
                            contact +
                            "</option>"
                    );
                });
                $("#party_contact").append('<option value="other">Other</option>');
                }
            },
        });
    } else {
        $("#party_email")
            .empty()
            .append('<option value="">Select Email</option>')
            .append('<option value="other">Other</option>');

        $("#party_contact")
            .empty()
            .append('<option value="">Select Contact</option>')
            .append('<option value="other">Other</option>');
    }
});
