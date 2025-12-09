
function formatNumberWithCommas(input) {
    let value = input.value;

    // Remove all commas first
    value = value.replace(/,/g, "");

    
    value = value.replace(/[^0-9.]/g, "");

    // Ensure only one decimal point
    const parts = value.split(".");
    if (parts.length > 2) {
        value = parts[0] + "." + parts.slice(1).join("");
    }

    // If the value is empty, clear the input
    if (value === "") {
        input.value = "";
        return;
    }

    // If it's just a decimal point, allow it
    if (value === ".") {
        input.value = ".";
        return;
    }

    // Split into integer and decimal parts
    const [integerPart, decimalPart] = value.split(".");

    // If there's no integer part, just show the decimal point
    if (!integerPart) {
        input.value = decimalPart !== undefined ? "." + decimalPart : "";
        return;
    }

    // Format the integer part with commas (Indian numbering system)
    const formattedInteger = parseInt(integerPart).toLocaleString("en-IN");

    // Combine integer and decimal parts
    if (decimalPart !== undefined) {
        input.value = formattedInteger + "." + decimalPart;
    } else {
        input.value = formattedInteger;
    }
}

// Simple number validation function
function validateNumber(input) {
    input.addEventListener("input", function () {
        this.value = this.value.replace(/[^0-9.-]/g, "");
    });
}

function initPouchValidation() {
    const inputs = [
        "pouch_combination1",
        "pouch_combination2",
        "pouch_combination3",
        "pouch_combination4",
    ];

    inputs.forEach((name) => {
        const input = document.querySelector(`input[name="${name}"]`);
        if (input) {
            validateNumber(input);
        }
    });
}

function getPouchValues() {
    const values = {};
    const inputs = [
        "pouch_combination1",
        "pouch_combination2",
        "pouch_combination3",
        "pouch_combination4",
    ];

    inputs.forEach((name) => {
        const input = document.querySelector(`input[name="${name}"]`);
        if (input) {
            values[name] = input.value ? parseFloat(input.value) : null;
        }
    });

    return values;
}

// Initialize when page loads
document.addEventListener("DOMContentLoaded", initPouchValidation);

function printJobDetails(btn) {
    const jobId = btn.dataset.id || "N/A";
    const job_name = btn.dataset.job_name || "N/A";
    const job_bill_no = btn.dataset.job_bill_no || "N/A";
    const company_name = btn.dataset.company_name || "N/A";
    const prpc_purchase = btn.dataset.prpc_purchase || "N/A";
    const prpc_sell = btn.dataset.prpc_sell || "N/A";
    const cylinder_size = btn.dataset.cylinder_size || "N/A";
    const cylinder_made_in = btn.dataset.cylinder_made_in || "N/A";
    const cylinder_bill_no = btn.dataset.cylinder_bill_no || "N/A";
    const cylinder_date = btn.dataset.cylinder_date || "N/A";
    const pouch_size = btn.dataset.pouch_size || "N/A";
    const pouch_open_size = btn.dataset.pouch_open_size || "N/A";
    const pouch_combination = btn.dataset.pouch_combination || "N/A";
    const correction = btn.dataset.correction || "N/A";
    const job_status = btn.dataset.job_status || "N/A";
    
    const noc = btn.dataset.noc || "N/A";

    // Create iframe for silent printing
    const iframe = document.createElement("iframe");
    iframe.style.position = "absolute";
    iframe.style.top = "-1000px";
    iframe.style.left = "-1000px";
    document.body.appendChild(iframe);

    const doc = iframe.contentWindow.document;
    doc.open();
    doc.write(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Order Completed</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.2/css/bootstrap.min.css" rel="stylesheet">
    
    <style>
        @page {
            size: A4;
            margin: 0;
        }

        body {
            background-color: #f5f5f5;
            font-family: Arial, sans-serif;
        }

        .a4-container {
            width: 210mm;
            min-height: 297mm;
            margin: 20px auto;
            background: white;
            padding: 20mm;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }

        .header-line {
            border-bottom: 2px solid #0d6efd;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .company-logo {
            max-width: 70px;
        }

        .company-name {
            color: #0d6efd;
            font-weight: bold;
            font-size: 1.1rem;
        }

        .section-title {
            background-color: #0d6efd;
            color: white;
            padding: 8px 12px;
            font-weight: bold;
            margin: 20px 0 10px 0;
            font-size: 0.9rem;
        }

        .info-row {
            padding: 8px;
            border-bottom: 1px solid #e0e0e0;
            font-size: 0.9rem;
        }

        .label {
            font-weight: bold;
            color: #0d6efd;
        }

        table {
            font-size: 0.85rem;
        }

        table th {
            background-color: #e7f1ff;
            color: #000;
            font-weight: bold;
        }

        .correction-box {
            border: 2px dashed #0d6efd;
            padding: 15px;
            margin: 20px 0;
            min-height: 60px;
        }

        .correction-title {
            font-weight: bold;
            color: #0d6efd;
            margin-bottom: 8px;
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 15px;
            border-top: 2px solid #0d6efd;
            font-size: 0.85rem;
            color: #666;
        }

        @media print {
            body {
                background: white;
            }

            .a4-container {
                width: 100%;
                margin: 0;
                padding: 15mm;
                box-shadow: none;
            }

            * {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
        }

        @media screen and (max-width: 768px) {
            .a4-container {
                width: 100%;
                margin: 0;
                padding: 15px;
                box-shadow: none;
            }
        }
    </style>
</head>
<body>

    <div class="a4-container">
        
        <!-- HEADER -->
        <div class="header-line">
            <div class="row align-items-center">
                <div class="col-auto">
                    <img src="https://nirmalgroup.com/wp-content/uploads/2024/11/Mask-group-2.png" 
                         alt="Logo" class="company-logo">
                </div>
                <div class="col text-end">
                    <div class="company-name">Shrri Nirmal Ventures Private Limited.</div>
                    <div style="font-size: 0.8rem; color: #666;">
                        Unit. 1601, 16th Floor, B Block, Navratna Corporate Park<br>
                        Ambli Bopal Road, Ambli, Ahmedabad - 380058
                    </div>
                </div>
            </div>
        </div>

        <!-- BASIC INFO -->
        <div class="info-row">
            <div class="row">
                <div class="col-6">
                    <span class="label">Bill No:</span> ${job_bill_no}
                </div>
                <div class="col-6 text-end">
                    <span class="label">Job Date:</span> ${cylinder_date}
                </div>
            </div>
        </div>

        <div class="info-row">
            <span class="label">Party Name:</span> ${company_name}
        </div>

        <div class="info-row">
            <span class="label">Job Name:</span> ${job_name}
        </div>

        <!-- CYLINDER DETAILS -->
        <div class="section-title">Cylinder Details</div>
        
        <table class="table table-bordered">
            <tbody>
                <tr>
                    <td class="label" style="width: 30%;">Cylinder Size</td>
                    <td>${cylinder_size}</td>
                </tr>
                <tr>
                    <td class="label">Cylinder Made In</td>
                    <td>${cylinder_made_in}</td>
                </tr>
                <tr>
                    <td class="label">Cylinder Bill No</td>
                    <td>${cylinder_bill_no}</td>
                </tr>
                <tr>
                    <td class="label">No. of Colors</td>
                    <td>${noc}</td>
                </tr>
            </tbody>
        </table>

        <!-- POUCH DETAILS -->
        <div class="section-title">Pouch Details</div>
        
        <table class="table table-bordered">
            <tbody>
                <tr>
                    <td class="label" style="width: 30%;">Pouch Size</td>
                    <td>${pouch_size}</td>
                </tr>
                <tr>
                    <td class="label">Pouch Open Size</td>
                    <td>${pouch_open_size}</td>
                </tr>
            </tbody>
        </table>

        <!-- PRPC DETAILS -->
        <div class="section-title">PRPC Details</div>
        
        <table class="table table-bordered">
            <tbody>
                <tr>
                    <td class="label" style="width: 30%;">PRPC Purchase</td>
                    <td>${prpc_purchase}</td>
                </tr>
                <tr>
                    <td class="label">PRPC Sell</td>
                    <td>${prpc_sell}</td>
                </tr>
            </tbody>
        </table>

        <!-- CORRECTION -->
        <div class="correction-box">
            <div class="correction-title">Correction:</div>
            <div>${correction}</div>
        </div>

        <!-- FOOTER -->
        <div class="footer">
            © shrri nirmal ventures private limited.
        </div>

    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.2/js/bootstrap.bundle.min.js"></script>

</body>
</html>
    `);
    doc.close();

    // Wait for content to load then print silently
    iframe.onload = function () {
        try {
            // Try to print without dialog
            iframe.contentWindow.focus();
            iframe.contentWindow.print();
        } catch (e) {
            // Fallback: create blob and download as PDF
            const printContent = doc.documentElement.outerHTML;
            const blob = new Blob([printContent], { type: "text/html" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `Job_Details_${jobId}_${new Date().getTime()}.html`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }

        // Clean up iframe
        setTimeout(() => {
            document.body.removeChild(iframe);
        }, 1000);
    };
}

document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");
    const loaderOverlay = document.getElementById("loader-overlay");

    forms.forEach((form) => {
        form.addEventListener("submit", function () {
            loaderOverlay.style.display = "flex";
        });
    });
});
