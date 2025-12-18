$(document).on(
    "input",
    "[name='pouch_height'], [name='pouch_diameter']",
    function () {
        const section = $(this).closest(".col-md-4");

        const pouch_open_height = section.find("[name='pouch_height']").val();

        const pouch_open_diameter = section
            .find("[name='pouch_diameter']")
            .val();

        let pouch_open_Size = "";

        if (pouch_open_height && pouch_open_diameter) {
            pouch_open_Size = `${pouch_open_height} x ${pouch_open_diameter}`;
            section.find("[name='pouch_size']").val(pouch_open_Size);
        }

        console.log(pouch_open_Size);
    }
);

$(document).on(
    "input",
    "[name='pouch_combination1'], [name='pouch_combination2'], [name='pouch_combination3'], [name='pouch_combination4']",
    function () {
        const section = $(this).closest(".col-md-8");

        const values = [
            section.find("[name='pouch_combination1']").val(),
            section.find("[name='pouch_combination2']").val(),
            section.find("[name='pouch_combination3']").val(),
            section.find("[name='pouch_combination4']").val(),
        ].filter((v) => v !== ""); // keep 0 but remove empty

        const combined = values.join("+");

        section.find("[name='pouch_combination']").val(combined);

        console.log(combined);
    }
);
