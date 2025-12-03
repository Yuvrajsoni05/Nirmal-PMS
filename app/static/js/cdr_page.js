document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("cdr_form");

    const companyNameSelect = document.getElementById("company_name");
    const newCompanyInput = document.getElementById("new_company_name");
    const companyNameError = document.getElementById("company_name_error");

    const companyEmailSelect = document.getElementById("company_email");
    const newCompanyEmailInput = document.getElementById("new_company_email");
    const companyEmailError = document.getElementById("company_email_error");

    const job_nameSelect = document.getElementById("job_name");
    const new_job_nameInput = document.getElementById("new_job_name");
    const job_name_Error = document.getElementById("job_name_error");

    const partyContactSelect = document.getElementById("party_contact_used");
    const newPartyContactInput = document.getElementById("new_party_contact");
    const partyContactError = document.getElementById("party_contact_error");

    const cdrDateInput = document.getElementById("cdr_upload_date");
    const cdrDateError = document.getElementById("cdr_upload_date_error");

    const cdrFilesInput = document.getElementById("cdr_files");
    const cdrFilesError = document.getElementById("cdr_files_error");

    job_nameSelect.addEventListener("change", function () {
        if (this.value === "others") {
            new_job_nameInput.style.display = "block";
            new_job_nameInput.focus();
        } else {
            new_job_nameInput.style.display = "none";
            new_job_nameInput.value = "";
            job_name_Error.style.display = "none";
        }
    });

    new_job_nameInput.addEventListener("input", function () {
        if (this.value.trim() !== "") {
            job_name_Error.style.display = "none";
        }
    });

    companyNameSelect.addEventListener("change", function () {
        if (this.value === "others") {
            newCompanyInput.style.display = "block";
            newCompanyInput.focus();
        } else {
            newCompanyInput.style.display = "none";
            newCompanyInput.value = "";
            companyNameError.style.display = "none";
        }
    });

    newCompanyInput.addEventListener("input", function () {
        if (this.value.trim() !== "") {
            companyNameError.style.display = "none";
        }
    });

    partyContactSelect.addEventListener("change", function () {
        if (this.value === "others") {
            newPartyContactInput.style.display = "block";
            newPartyContactInput.focus();
        } else {
            newPartyContactInput.style.display = "none";
            newPartyContactInput.value = "";
            partyContactError.style.display = "none";
        }
    });

    newPartyContactInput.addEventListener("input", function () {
        if (this.value.trim() !== "") {
            partyContactError.style.display = "none";
        }
    });

    companyEmailSelect.addEventListener("change", function () {
        if (this.value === "other") {
            newCompanyEmailInput.style.display = "block";
            newCompanyEmailInput.focus();
        } else {
            newCompanyEmailInput.style.display = "none";
            newCompanyEmailInput.value = "";
            companyEmailError.style.display = "none";
        }
    });

    newCompanyEmailInput.addEventListener("input", function () {
        if (this.value.trim() !== "") {
            companyEmailError.style.display = "none";
        }
    });

    function validateEmail(email) {
        const pattern =
            /(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return pattern.test(email);
    }

    function validateContact(contact) {
        const contactPattern =
            /^((091|\+91)?|(\(091\)|\(+91\))|(91)?|\(91\)|0)?[ ]?[6-9]\d{9}$/;
        return contactPattern.test(contact);
    }

    function validateForm() {
        let isValid = true;

        if (companyNameSelect.value === "others") {
            if (newCompanyInput.value.trim() === "") {
                companyNameError.style.display = "block";
                isValid = false;
            }
        } else if (companyNameSelect.value === "") {
            companyNameError.style.display = "block";
            isValid = false;
        }

        if (job_nameSelect.value === "others") {
            if (new_job_nameInput.value.trim() === "") {
                job_name_Error.style.display = "block";
                isValid = false;
            }
        } else if (job_nameSelect.value === "") {
            job_name_Error.style.display = "block";
            isValid = false;
        }

        if (companyEmailSelect.value === "other") {
            if (
                newCompanyEmailInput.value.trim() === "" ||
                !validateEmail(newCompanyEmailInput.value)
            ) {
                companyEmailError.style.display = "block";
                isValid = false;
            }
        } else if (companyEmailSelect.value === "") {
            companyEmailError.style.display = "block";
            isValid = false;
        }

        if (partyContactSelect.value === "others") {
            if (
                newPartyContactInput.value.trim() === "" ||
                !validateContact(newPartyContactInput.value)
            ) {
                partyContactError.style.display = "block";
                isValid = false;
            }
        } else if (partyContactSelect.value === "") {
            partyContactError.style.display = "block";
            isValid = false;
        }

        if (cdrDateInput.value.trim() === "") {
            cdrDateError.style.display = "block";
            isValid = false;
        }

        if (cdrFilesInput.value.trim() === "") {
            cdrFilesError.style.display = "block";
            isValid = false;
        }

        return isValid;
    }

    form.addEventListener("submit", function (e) {
        const loaderOverlay = document.getElementById("loader-overlay");

        if (!validateForm()) {
            e.preventDefault();

            // Scroll to first visible error
            const firstError = document.querySelector(
                '[style*="display: block"]'
            );
            if (firstError) {
                firstError.scrollIntoView({ behavior: "smooth" });
            }
        } else {
            loaderOverlay.style.display = "flex";
        }
    });
});

function printJobDetails(btn) {
    const jobId = btn.dataset.id || "N/A";
    const job_name = btn.dataset.job_name || "N/A";
    const company_name = btn.dataset.company_name || "N/A";
    const company_email = btn.dataset.company_email || "N/A";
    const date = btn.dataset.date || "N/A";
    const correction = btn.dataset.correction || "N/A";
    const folder_url = btn.dataset.folder_url || "#";

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
<html>
<head>
    <title></title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            padding: 40px; 
            margin: 0;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .header {
            text-align: right;
            margin-bottom: 30px;
            border-bottom: 3px solid #007bff;
            padding-bottom: 20px;
        }
        
        .logo {
            text-align: left;
            margin-bottom: 15px;
        }
        
        .logo-text {
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }
        
        .logo-text span {
            color: #ff6600;
        }
        
        .company-name {
            font-size: 16px;
            font-weight: bold;
            color: #007bff;
            margin: 5px 0;
        }
        
        .company-address {
            font-size: 11px;
            color: #666;
            line-height: 1.4;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .info-label {
            font-weight: bold;
            color: #007bff;
            width: 150px;
        }
        
        .info-value {
            flex: 1;
            color: #333;
        }
        
        .section-header {
            background-color: #007bff;
            color: white;
            padding: 10px 15px;
            font-weight: bold;
            margin: 25px 0 0 0;
        }
        
        .section-content {
            border: 1px solid #007bff;
            border-top: none;
            padding: 0;
        }
        
        .detail-row {
            display: flex;
            padding: 10px 15px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .detail-row:last-child {
            border-bottom: none;
        }
        
        .detail-label {
            font-weight: bold;
            width: 200px;
            color: #333;
        }
        
        .detail-value {
            flex: 1;
            color: #333;
        }
        
        .correction-box {
            border: 2px dashed #007bff;
            padding: 15px;
            margin: 25px 0;
        }
        
        .correction-title {
            color: #007bff;
            font-weight: bold;
            margin-bottom: 8px;
        }
        
        .correction-text {
            color: #333;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #007bff;
            font-size: 11px;
            color: #666;
        }
        
        @media print {
            body {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    
    
    <div class="header">
    <div class="col-auto">
        <img  src="https://nirmalgroup.com/wp-content/uploads/2024/11/Mask-group-2.png" 
                alt="Logo" class="company-logo" style="height: 30px;">
    </div>
        <div class="company-name">Shrri nirmal ventures private limited. Ltd.</div>
        <div class="company-address">
            1601, 16th Floor, B Block, Navratna Corporate Park<br>
            Ambli Bopal Road, Ambli, Ahmedabad - 380058
        </div>
    </div>
    
    <div class="info-row">
        <span class="info-label">CDR ID:</span>
        <span class="info-value">${jobId}</span>
    </div>
    
    <div class="info-row">
        <span class="info-label">Job Date:</span>
        <span class="info-value">${date}</span>
    </div>
    
    <div class="info-row">
        <span class="info-label">Party Name:</span>
        <span class="info-value">${company_name}</span>
    </div>

    <div class="info-row">
        <span class="info-label">Party Email:</span>
        <span class="info-value">${company_email}</span>
    </div>
    
    <div class="info-row">
        <span class="info-label">Job Name:</span>
        <span class="info-value">${job_name}</span>
    </div>
    
    
    
    <div class="correction-box">
        <div class="correction-title">Correction:</div>
        <div class="correction-text">${correction}</div>
    </div>
    
    
    
    <div class="footer">
        © shrri nirmal ventures private limited.
    </div>
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
    const forms = document.querySelectorAll(".cdr-form");
    const loaderOverlay = document.getElementById("loader-overlay");

    forms.forEach((form) => {
        form.addEventListener("submit", function () {
            loaderOverlay.style.display = "flex";
        });
    });
});
