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

    function validateForm() {
        let isValid = true;

        if (companyNameSelect.value === "others") {
            if (newCompanyInput.value.trim() === "") {
                companyNameError.style.display = "block";
                isValid = false;
            } else {
                companyNameError.style.display = "none";
            }
        } else if (companyNameSelect.value === "") {
            companyNameError.style.display = "block";
            isValid = false;
        }

        if (job_nameSelect.value === "others") {
            if (new_job_nameInput.value.trim() === "") {
                job_name_Error.style.display = "block";
                isValid = false;
            } else {
                job_name_Error.style.display = "none";
            }
        } else if (job_nameSelect.value === "") {
            job_name_Error.style.display = "block";
            isValid = false;
        }

        // Company Email
        if (companyEmailSelect.value === "other") {
            if (
                newCompanyEmailInput.value.trim() === "" ||
                !validateEmail(newCompanyEmailInput.value)
            ) {
                companyEmailError.style.display = "block";
                isValid = false;
            } else {
                companyEmailError.style.display = "none";
            }
        } else if (companyEmailSelect.value === "") {
            companyEmailError.style.display = "block";
            isValid = false;
        }

        // CDR Date
        if (cdrDateInput.value.trim() === "") {
            cdrDateError.style.display = "block";
            isValid = false;
        } else {
            cdrDateError.style.display = "none";
        }

        // CDR Files
        if (cdrFilesInput.value.trim() === "") {
            cdrFilesError.style.display = "block";
            isValid = false;
        } else {
            cdrFilesError.style.display = "none";
        }

        return isValid;
    }

    form.addEventListener("submit", function (e) {
        const loaderOverlay = document.getElementById("loader-overlay");

        if (!validateForm()) {
            e.preventDefault();
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
                    <title>Job Details - Print</title>
                    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
                    <style>
                        body { font-family: Arial, sans-serif; padding: 20px; margin: 0; }
                        @page { margin: 20px; }
                    </style>
                </head>
                <body>
                    <div class="text-center mb-4">
                        <h2 style="color: #0d6efd; margin-bottom: 5px;">Nirmal Group</h2>
                        <h4 style="margin-bottom: 20px;">CDR Details    </h4>
                        <hr>
                    </div>
                    
                    <table class="table table-bordered" style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="background-color: #212529; color: white;">
                                <th style="width: 30%; padding: 12px; border: 1px solid #dee2e6;">Field</th>
                                <th style="padding: 12px; border: 1px solid #dee2e6;">Details</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Job ID</strong></td>
                                <td style="padding: 8px; border: 1px solid #dee2e6;">${jobId}</td>
                            </tr>
                            <tr style="background-color: #f8f9fa;">
                                <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Job Name</strong></td>
                                <td style="padding: 8px; border: 1px solid #dee2e6;">${job_name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Date</strong></td>
                                <td style="padding: 8px; border: 1px solid #dee2e6;">${date}</td>
                            </tr>
                            <tr style="background-color: #f8f9fa;">
                                <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Company Name</strong></td>
                                <td style="padding: 8px; border: 1px solid #dee2e6;">${company_name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Company Email</strong></td>
                                <td style="padding: 8px; border: 1px solid #dee2e6;">${company_email}</td>
                            </tr>
                            <tr style="background-color: #f8f9fa;">
                                <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Corrections</strong></td>
                                <td style="padding: 8px; border: 1px solid #dee2e6;">${correction}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Folder Link</strong></td>
                                <td style="padding: 8px; border: 1px solid #dee2e6;"><a href="${folder_url}" target="_blank">Open Folder</a></td> 
                            </tr>  
                        
                        </tbody>
                    </table>
                    
                    <div class="text-center mt-4">
                        <small style="color: #6c757d;">Generated on ${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()}</small>
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
