document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('upload-area');
    const cameraInput = document.getElementById('camera-input');
    const galleryInput = document.getElementById('gallery-input');
    const cameraBtn = document.getElementById('camera-btn');
    const galleryBtn = document.getElementById('gallery-btn');
    const previewSection = document.getElementById('preview-section');
    const previewImg = document.getElementById('preview-img');
    const scanBtn = document.getElementById('scan-btn');
    const loaderSection = document.getElementById('loader-section');
    const resultsSection = document.getElementById('results-section');
    const toastContainer = document.getElementById('toast-container');
    
    let selectedFile = null;
    const MAX_FILE_SIZE_MB = 10;

    // --- Toast Notification System ---
    function showToast(message, type = 'error') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toastContainer.appendChild(toast);
        
        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 10);
        
        // Remove after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // --- Event Listeners for Mobile Actions ---
    cameraBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        cameraInput.click();
    });

    galleryBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        galleryInput.click();
    });

    // Handle drag and drop for desktop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    // Handle File Selection
    cameraInput.addEventListener('change', (e) => processInputEvent(e));
    galleryInput.addEventListener('change', (e) => processInputEvent(e));

    function processInputEvent(e) {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    }

    function handleFile(file) {
        // Validation: Ensure it's an image
        if (!file.type.startsWith('image/')) {
            showToast('Invalid file format. Please select an image.');
            return;
        }

        // Validation: Prevent huge files from crashing mobile browsers/server
        const fileSizeMB = file.size / (1024 * 1024);
        if (fileSizeMB > MAX_FILE_SIZE_MB) {
            showToast(`File is too large (${fileSizeMB.toFixed(1)}MB). Limit is ${MAX_FILE_SIZE_MB}MB.`);
            return;
        }

        selectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            previewSection.style.display = 'block';
            resultsSection.style.display = 'none';
            // Smooth scroll to preview
            previewSection.scrollIntoView({ behavior: 'smooth' });
        };
        reader.readAsDataURL(file);
    }

    scanBtn.addEventListener('click', async () => {
        if (!selectedFile) {
            showToast('Please capture or select an image first.');
            return;
        }

        const customNameInput = document.getElementById('custom-filename');
        const formData = new FormData();
        formData.append('file', selectedFile);
        if (customNameInput && customNameInput.value.trim() !== '') {
            formData.append('custom_name', customNameInput.value.trim());
        }

        previewSection.style.display = 'none';
        loaderSection.style.display = 'block';
        resultsSection.style.display = 'none';
        loaderSection.scrollIntoView({ behavior: 'smooth' });

        try {
            const response = await fetch('/api/scan', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Scan failed');
            }

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error during scan:', error);
            alert('An error occurred during scanning. Please try again.');
        } finally {
            loaderSection.style.display = 'none';
        }
    });

    function displayResults(data) {
        const report = data.compliance_report;
        
        // Status Badge
        const statusBadge = document.getElementById('status-badge');
        statusBadge.textContent = report.overall_status;
        statusBadge.className = 'badge ' + (report.overall_status === 'COMPLIANT' ? 'compliant' : 'non-compliant');

        // Stats
        document.getElementById('rules-checked').textContent = report.total_rules_checked || 0;
        document.getElementById('rules-passed').textContent = report.rules_passed || 0;
        document.getElementById('rules-failed').textContent = report.rules_failed || 0;

        // Rules Table
        const rulesTbody = document.getElementById('rules-tbody');
        rulesTbody.innerHTML = '';
        if (report.rule_results) {
            report.rule_results.forEach(rule => {
                const tr = document.createElement('tr');
                const statusClass = rule.status === 'PASS' ? 'compliant' : 'non-compliant';
                tr.innerHTML = `
                    <td>${rule.rule_id}</td>
                    <td>${rule.rule_name}</td>
                    <td class="status-text ${statusClass}">${rule.status}</td>
                `;
                rulesTbody.appendChild(tr);
            });
        }

        // Violations List
        const violationsList = document.getElementById('violations-list');
        violationsList.innerHTML = '';
        const allViolations = [...(report.violations || []), ...(report.font_violations || [])];
        if (allViolations.length > 0) {
            allViolations.forEach(v => {
                const div = document.createElement('div');
                div.className = 'violation-item';
                if (v.rule_id) {
                    div.innerHTML = `<strong>${v.rule_id}: ${v.rule_name}</strong><br>${v.description || ''}`;
                } else {
                    div.innerHTML = `<strong>Font Violation:</strong> "${v.text}" — Found: ${v.font_size_mm}mm, Required: ${v.min_required_mm}mm`;
                }
                violationsList.appendChild(div);
            });
        } else {
            violationsList.innerHTML = '<p style="color: #00e676;">✅ No violations found!</p>';
        }

        // Report Links
        document.getElementById('pdf-link').href = data.pdf_report || '#';
        document.getElementById('evidence-link').href = data.evidence_image || '#';

        resultsSection.style.display = 'block';
    }
});
