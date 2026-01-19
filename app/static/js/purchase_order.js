
document.addEventListener("DOMContentLoaded", function () {

    /* ================= PARTY NAME & EMAIL ================= */
    const partyNameSelect = document.getElementById("party_name");
    const newPartyNameInput = document.getElementById("new_party_name");
    const partyEmailSelect = document.getElementById("party_email");
    const newPartyEmailInput = document.getElementById("new_party_email");

    partyNameSelect?.addEventListener("change", function () {
        newPartyNameInput.classList.toggle("d-none", this.value !== "others");
        newPartyNameInput.required = this.value === "others";
        if (this.value !== "others") newPartyNameInput.value = "";
    });

    partyEmailSelect?.addEventListener("change", function () {
        newPartyEmailInput.classList.toggle("d-none", this.value !== "others");
        newPartyEmailInput.required = this.value === "others";
        if (this.value !== "others") newPartyEmailInput.value = "";
    });

    // /* ================= JOB NAME ================= */
    // function setupJobNameHandlers() {
    //     document.querySelectorAll(".job_name").forEach(select => {
    //         select.onchange = function () {
    //             const block = this.closest(".job-block, .job-block_data");
    //             const input = block?.querySelector(".new_job_name");
    //             if (!input) return;

    //             input.classList.toggle("d-none", this.value !== "others");
    //             input.required = this.value === "others";
    //             if (this.value !== "others") input.value = "";
    //         };
    //     });
    // }

    /* ================= POUCH SIZE ================= */
    function setupPouchSizeCalculation() {
        document.querySelectorAll(".job-block").forEach(block => {
            const h = block.querySelector(".pouch_height");
            const d = block.querySelector(".pouch_diameter");
            const out = block.querySelector(".pouch_size");

            if (!h || !d || !out) return;

            const calc = () => {
                out.value = h.value && d.value ? `${h.value} × ${d.value}` : "";
            };

            h.oninput = calc;
            d.oninput = calc;
            calc();
        });
    }

    /* ================= POUCH COMBINATION ================= */
    function setupPouchCombinationCalculation() {
        document.querySelectorAll(".job-block, .job-block_data").forEach(block => {
            const pcs = block.querySelectorAll(".pc1, .pc2, .pc3, .pc4");
            const hidden = block.querySelector(".pouch_combination");

            if (pcs.length !== 4 || !hidden) return;

            const calc = () => {
                hidden.value = [...pcs]
                    .map(i => i.value.trim())
                    .filter(Boolean)
                    .join(" + ");
            };

            pcs.forEach(i => i.oninput = calc);
            calc(); // 🔥 important for existing data
        });
    }

    /* ================= PER POUCH RATE ================= */
    function setupPouchRateCalculation() {
        document.querySelectorAll(".job-block, .job-block_data").forEach(block => {
            const rate = block.querySelector(".purchase_rate_per_kg");
            const qty = block.querySelector(".no_of_pouch_kg");
            const out = block.querySelector(".per_pouch_rate_basic");

            if (!rate || !qty || !out) return;

            const calc = () => {
                const r = parseFloat(rate.value) || 0;
                const q = parseFloat(qty.value) || 0;
                out.value = r && q ? (r / q).toFixed(4) : "";
            };

            rate.oninput = calc;
            qty.oninput = calc;
        });
    }

    /* ================= READONLY FOR EXISTING ================= */
    function applyReadonlyIfValue() {
        document.querySelectorAll(".job-block_data input, .job-block_data textarea").forEach(el => {
            if (
                el.type === "hidden" ||
                ["quantity","purchase_rate_per_kg","no_of_pouch_kg","pouch_charge",
                 "zipper_cost","final_rare","minimum_quantity","delivery_address"]
                .includes(el.name)
            ) return;

            if (el.value?.trim()) el.readOnly = true;
        });
    }

    /* ================= ADD JOB (NEW) ================= */
    document.getElementById("add-job")?.addEventListener("click", () => {
        const container = document.getElementById("jobs-container");
        const template = container.querySelector(".job-block:last-of-type");
        const clone = template.cloneNode(true);

        clone.querySelectorAll("input, textarea").forEach(el => {
            el.value = "";
            el.readOnly = false;
        });
        clone.querySelectorAll("select").forEach(el => el.selectedIndex = 0);

        container.appendChild(clone);
        initAll();
    });

    /* ================= ADD JOB (FROM EXISTING DATA) ================= */
    document.getElementById("add-jobs")?.addEventListener("click", () => {
        const container = document.getElementById("job_data_container");
        const template = container.querySelector(".job-block_data:last-of-type");
        const clone = template.cloneNode(true);

        clone.querySelectorAll("input, textarea").forEach(el => {
            if (el.type !== "hidden") {
                el.value = "";
                el.readOnly = false;
            }
        });
        clone.querySelectorAll("select").forEach(el => el.selectedIndex = 0);

        container.appendChild(clone);
        initAll();
    });

    /* ================= REMOVE JOB ================= */
    document.addEventListener("click", e => {
        if (!e.target.classList.contains("remove-job")) return;
        const blocks = document.querySelectorAll(".job-block, .job-block_data");
        if (blocks.length === 1) return alert("At least one job is required");
        e.target.closest(".job-block, .job-block_data").remove();
    });

    /* ================= INIT ================= */
    function initAll() {
        // setupJobNameHandlers();
        setupPouchSizeCalculation();
        setupPouchCombinationCalculation();
        setupPouchRateCalculation();
        applyReadonlyIfValue();
    }

    initAll();
});


/* ---------- JOB NAME → OTHERS (PER JOB BLOCK) ---------- */
$(document).on(
    "change",
    ".job-block select.job_name, .job-block_data select.job_name",
    function () {
        const block = $(this).closest(".job-block, .job-block_data");
        const select = $(this);
        const newJob = block.find(".new_job_name");

        if (select.val() === "others") {
            newJob
                .removeClass("d-none")
                .prop("required", true)
                .focus();

            // store original name only once
            if (!select.data("orig-name")) {
                select.data("orig-name", select.attr("name"));
            }

            select.removeAttr("name");
            newJob.attr("name", "job_name[]");

        } else {
            newJob
                .addClass("d-none")
                .prop("required", false)
                .val("")
                .removeClass("is-invalid")
                .removeAttr("name");

            if (!select.attr("name")) {
                select.attr("name", select.data("orig-name"));
            }
        }
    }
);

/* ---------- JOB NAME LIVE VALIDATION ---------- */
$(document).on(
    "input",
    ".job-block .new_job_name, .job-block_data .new_job_name",
    function () {
        const block = $(this).closest(".job-block, .job-block_data");
        const select = block.find(".job_name");

        if (select.val() === "others" && $(this).val().trim() === "") {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    }
);
