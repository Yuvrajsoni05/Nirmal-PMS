$(document).ready(function () {
    $(document).on(
        "input change",
         '#billing_address_select, #billing_state_name, #party_name, input[name="gst[]"], .item_check, input[name="quantity[]"], input[name="prpc_price[]"], .pouch-diameter, .pouch-height, .cylinder-diameter, .cylinder-height, .new-job, .job-name',
        function () {
            var changedField = $(this).attr("id") || $(this).attr("name");
            var billing_state_name = $("#billing_state_name").val();
            var party_name = $("#party_name").val();

            var igst = $("#igst").is(":checked") ? 18 : 0;
            var cgst = $("#cgst").is(":checked") ? 9 : 0;
            var sgst = $("#sgst").is(":checked") ? 9 : 0;

            var quantities = $('input[name="quantity[]"]')
                .map(function () {
                    return $(this).val() || 0;
                })
                .get();
            var prpc_prices = $('input[name="prpc_price[]"]')
                .map(function () {
                    return $(this).val() || 0;
                })
                .get();

            if (party_name === "others") {
                $("#new_party_name").show();
            } else {
                $("#new_party_name").hide();
            }

            if (changedField === "party_name") {
                $("#party_email").val("");
                $("#party_contact").val("");
                $("#billing_address").val("");
            }

            // Set GST options visibility
            if (billing_state_name === "Gujarat") {
                $("#igst_div").hide();
                $("#sgst_div").show();
                $("#cgst_div").show();
                igst = 0;
            } else if (billing_state_name) {
                $("#igst_div").show();
                $("#sgst_div").hide();
                $("#cgst_div").hide();
                sgst = 0;
                cgst = 0;
            }

            $.ajax({
                url: proformaAjaxUrl,
                type: "GET",
                data: {
                    billing_state_name: billing_state_name,
                    party_name: party_name,
                    igsts: igst,
                    cgsts: cgst,
                    sgsts: sgst,
                    quantities: quantities,
                    prpc_prices: prpc_prices,
                },
                success: function (response) {
                    if (changedField === "party_name") {
                        $("#billing_address").val(
                            response.billing_address || ""
                        );
                    }
                    if (
                        (response.contacts && response.contacts.length) ||
                        changedField === "party_name"
                    ) {
                        var $select = $("#party_contact");
                        var previous = $select.val();
                        $select
                            .empty()
                            .append(
                                '<option value="" selected disabled>Select Party Contact</option>'
                            );
                        if (response.contacts && response.contacts.length) {
                            $.each(
                                response.contacts,
                                function (index, contact) {
                                    $select.append(
                                        '<option value="' +
                                            contact.party_contacts__party_number +
                                            '">' +
                                            contact.party_contacts__party_number +
                                            "</option>"
                                    );
                                }
                            );
                        }
                        $select.append('<option value="others">Other</option>');

                        if (previous) {
                            if (
                                $select.find('option[value="' + previous + '"]')
                                    .length
                            ) {
                                $select.val(previous);
                            } else {
                                if (previous !== "others" && previous !== "") {
                                    $select.append(
                                        '<option class="custom-contact" value="' +
                                            previous +
                                            '" selected>' +
                                            previous +
                                            "</option>"
                                    );
                                } else {
                                    $select.prop("selectedIndex", 0);
                                }
                            }
                        }
                    }
                    if (
                        (response.emails && response.emails.length) ||
                        changedField === "party_name"
                    ) {
                        var $select = $("#party_email");
                        var previous = $select.val();
                        $select
                            .empty()
                            .append(
                                '<option value="" selected disabled>Select Party Email</option>'
                            );
                        if (response.emails && response.emails.length) {
                            $.each(response.emails, function (index, email) {
                                $select.append(
                                    '<option value="' +
                                        email.party_emails__email +
                                        '">' +
                                        email.party_emails__email +
                                        "</option>"
                                );
                            });
                        }
                        $select.append('<option value="others">Other</option>');

                        if (previous) {
                            if (
                                $select.find('option[value="' + previous + '"]')
                                    .length
                            ) {
                                $select.val(previous);
                            } else {
                                if (previous !== "others" && previous !== "") {
                                    $select.append(
                                        '<option class="custom-email" value="' +
                                            previous +
                                            '" selected>' +
                                            previous +
                                            "</option>"
                                    );
                                } else {
                                    $select.prop("selectedIndex", 0);
                                }
                            }
                        }
                    }

                
                      
                    if (
                        response.billing_addresses &&
                        response.billing_addresses.length &&
                        changedField !== "billing_address_select"
                    ) {
                        var $select = $("#billing_address_select");
                        var previous = $select.val();

                        $select
                            .empty()
                            .append('<option value="" disabled>Select Billing Address</option>');

                        let found = false;

                        $.each(response.billing_addresses, function (index, billing) {
                            const value = billing.party_billing_addresses__billing_address;

                            if (value === previous) {
                                found = true;
                            }

                            $select.append(
                                `<option value="${value}">${value}</option>`
                            );
                        });

                        $select.append('<option value="others">Other</option>');

                        // ✅ restore previous value safely
                        if (previous) {
                            if (found || previous === "others") {
                                $select.val(previous);
                            } else {
                                // custom typed address
                                $select.append(
                                    `<option class="custom-billing" value="${previous}" selected>${previous}</option>`
                                );
                            }
                        }
                    }

                    if (
                        response.billing_gstins &&
                        response.billing_gstins.length &&
                        changedField !== "billing_gstin_select"
                    ) {
                        var $select = $("#billing_gstin_select");
                        var previous = $select.val();

                        $select
                            .empty()
                            .append('<option value="" disabled selected>Select GSTIN</option>');

                        $.each(response.billing_gstins, function (index, gstin) {
                            $select.append(
                                `<option value="${gstin}">${gstin}</option>`
                            );
                        });

                        $select.append('<option value="others">Other</option>');

                        if (previous) {
                            $select.val(previous);
                        }
                    }



                    if (
                        (response.job && response.job.length) ||
                        changedField === "party_name"
                    ) {
                        $(".job-name").each(function () {
                            var $select = $(this);
                            var previous = $select.val();
                            $select
                                .empty()
                                .append(
                                    '<option value="" selected disabled>Select Job Name</option>'
                                );
                            if (response.job && response.job.length) {
                                $.each(response.job, function (index, job) {
                                    $select.append(
                                        '<option value="' +
                                            job.job_name +
                                            '">' +
                                            job.job_name +
                                            "</option>"
                                    );
                                });
                            }
                            $select.append(
                                '<option value="others">Other</option>'
                            );
                            


                            if (previous) {
                                if (
                                    $select.find(
                                        'option[value="' + previous + '"]'
                                    ).length
                                ) {
                                    $select.val(previous);
                                } else {
                                    if (
                                        previous !== "others" &&
                                        previous !== ""
                                    ) {
                                        $select.append(
                                            '<option class="custom-job" value="' +
                                                previous +
                                                '" selected>' +
                                                previous +
                                                "</option>"
                                        );
                                    } else {
                                        $select.prop("selectedIndex", 0);
                                    }
                                }
                            }
                        });
                    }

                    if (response.total_amount !== undefined) {
                        $("#total_amount").val(
                            Number(response.total_amount).toFixed(2)
                        );
                    }
                    if (response.taxable_value !== undefined) {
                        $("#taxable_value").val(
                            Number(response.taxable_value).toFixed(2)
                        );
                    }
                    if (response.gst_amount !== undefined) {
                        $("#gst_value").val(
                            Number(response.gst_amount).toFixed(2)
                        );
                    }
                },
                error: function (xhr, status, error) {
                    console.log("Error:", error);
                },
            });
        }
    );

    $(document).on("change", ".job-name", function () {
        const section = $(this).closest(".job-section");
        const newJobInput = section.find(".new-job");

        if ($(this).val() === "others") {
            newJobInput.show().focus();
        } else {
            newJobInput.hide().val("");
            section.find(".job-name option.custom-job").remove();
        }
    });

    $(document).on("input", ".new-job", function () {
        const section = $(this).closest(".job-section");
        const dropdown = section.find(".job-name");
        const newJobName = $(this).val().trim();

        dropdown.find("option.custom-job").remove();

        if (newJobName !== "") {
            dropdown.append(
                `<option class="custom-job" value="${newJobName}" selected>${newJobName}</option>`
            );
        } else {
            dropdown.val("others");
        }
    });

    $(document).on("change", "#party_email", function () {
        const val = $(this).val();
        if (val === "others") {
            $("#new_party_email").show().focus();
        } else {
            $("#new_party_email").hide().val("");
            $("#party_email option.custom-email").remove();
        }
    });



    $(document).on("change", "#billing_address_select", function () {
        const val = $(this).val();
        console.log(val);
        if (val === "others") {
            $("#new_billing_address").show().focus();
        } else {
            $("#new_billing_address").hide().val("");
    }
    });


    $(document).on("input", "#new_party_email", function () {
        const email = $(this).val().trim();
        const $dropdown = $("#party_email");
        $dropdown.find("option.custom-email").remove();

        if (email !== "") {
            $dropdown.append(
                `<option class="custom-email" value="${email}" selected>${email}</option>`
            );
        } else {
            $dropdown.val("others");
        }
    });

    $(document).on("change", "#party_contact", function () {
        const val = $(this).val();
        if (val === "others") {
            $("#new_party_contact").show().focus();
        } else {
            $("#new_party_contact").hide().val("");
            $("#party_contact option.custom-contact").remove();
        }
    });

    $(document).on("input", "#new_party_contact", function () {
        const contact = $(this).val().trim();
        const $dropdown = $("#party_contact");
        $dropdown.find("option.custom-contact").remove();

        if (contact !== "") {
            $dropdown.append(
                `<option class="custom-contact" value="${contact}" selected>${contact}</option>`
            );
        } else {
            $dropdown.val("others");
        }
    });

    $(document).on("input", ".pouch-diameter, .pouch-height", function () {
        const section = $(this).closest(".job-section");
        const diameter = section.find(".pouch-diameter").val();
        const height = section.find(".pouch-height").val();
        if (diameter && height) {
            section.find(".pouch-open-size").val(`${height}x${diameter}`);
        }
    });

    $(document).on(
        "input",
        ".cylinder-diameter, .cylinder-height",
        function () {
            const section = $(this).closest(".job-section");
            const diameter = section.find(".cylinder-diameter").val();
            const height = section.find(".cylinder-height").val();
            if (diameter && height) {
                section.find(".cylinder-size").val(`${height}x${diameter}`);
            }
        }
    );

    $("#add-job").on("click", function (e) {
        e.preventDefault();
        let newSection = $(".job-section:first").clone();
        newSection.find("input").val("");
        newSection.find("select").prop("selectedIndex", 0);
        newSection.find(".new-job").hide();
        newSection.find("option.custom-job").remove();
        newSection.find("h5").after(`
                <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                    <button class="btn btn-danger me-md-2 SN" id="close_job" type="button">X</button>
                </div>
                `);

        $("#job-container").append(newSection);
        jobIndex++;
    });
    $(document).on("click", "#close_job", function (e) {
        e.preventDefault();
        $(this).closest(".job-section").remove();
    });
});
