function formatNumberWithCommas(input) {
    let value = input.value;
    value = value.replace(/,/g, "");
    let formattedValue = Number(value).toLocaleString("EN-IN");
    input.value = formattedValue;
}

function formatNumberWithCommas(input) {
    let value = input.value;

    // Remove all commas first
    value = value.replace(/,/g, "");

    // Allow only numbers and decimal point
    // Remove any character that is not a digit or decimal point
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
    const folder_url = btn.dataset.folder_url || "N/A";

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
    <title>Job Details - Bill Format</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            padding: 20px;
            margin: 0;
            color: #333;
        }
        @page {
            margin: 20px;
        }
        h2, h4 {
            color: #0d6efd;
            margin-bottom: 10px;
        }
        .table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }
        .table td, .table th {
            padding: 10px 12px;
            text-align: left;
            border: 1px solid #dee2e6;
        }
        .table th {
            background-color: #f8f9fa;
            color: #495057;
            font-size: 1rem;
        }
        .table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .table .section-header {
            background-color: #e9ecef;
            font-weight: bold;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #6c757d;
            font-size: 0.875rem;
        }
    </style>
</head>
<body>
    <div class="text-center mb-4">
        <h2>Nirmal Group</h2>
        <h4>Job Details Bill</h4>
        <hr>
    </div>

    <!-- Table for job details -->
    <table class="table">
        <!-- Job Information Section -->
        <tr class="section-header">
            <th colspan="2">Job Information</th>
        </tr>
        <tr>
            <td><strong>Job ID</strong></td>
            <td>${jobId}</td>
        </tr>
        <tr>
            <td><strong>Job Name</strong></td>
            <td>${job_name}</td>
        </tr>
        <tr>
            <td><strong>Job Bill No</strong></td>
            <td>${job_bill_no}</td>
        </tr>
        <tr>
            <td><strong>Company Name</strong></td>
            <td>${company_name}</td>
        </tr>

        <!-- Pricing Information Section -->
        <tr class="section-header">
            <th colspan="2">Pricing Information</th>
        </tr>
        <tr>
            <td><strong>PRPC Purchase</strong></td>
            <td>${prpc_purchase}</td>
        </tr>
        <tr>
            <td><strong>PRPC Sell</strong></td>
            <td>${prpc_sell}</td>
        </tr>

        <!-- Cylinder Details Section -->
        <tr class="section-header">
            <th colspan="2">Cylinder Details</th>
        </tr>
        <tr>
            <td><strong>Cylinder Size</strong></td>
            <td>${cylinder_size}</td>
        </tr>
        <tr>
            <td><strong>Cylinder Bill No</strong></td>
            <td>${cylinder_bill_no}</td>
        </tr>

        <!-- Pouch Details Section -->
        <tr class="section-header">
            <th colspan="2">Pouch Details</th>
        </tr>
        <tr>
            <td><strong>Pouch Size</strong></td>
            <td>${pouch_size}</td>
        </tr>
        <tr>
            <td><strong>Pouch Open Size</strong></td>
            <td>${pouch_open_size}</td>
        </tr>
        <tr>
            <td><strong>Pouch Combination</strong></td>
            <td>${pouch_combination}</td>
        </tr>

        <!-- Additional Information Section -->
        <tr class="section-header">
            <th colspan="2">Additional Information</th>
        </tr>
        <tr>
            <td><strong>Correction</strong></td>
            <td>${correction}</td>
        </tr>
        <tr>
            <td><strong>Job Status</strong></td>
            <td>${job_status}</td>
        </tr>
        <tr>
            <td><strong>Folder URL</strong></td>
            <td style="word-wrap: break-word; max-width: 300px;">${folder_url}</td>
        </tr>
    </table>

    <!-- Footer -->

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
