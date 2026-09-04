document.addEventListener('DOMContentLoaded', () => {
    const scanForm = document.getElementById('scan-form');
    const customFilenameInput = document.getElementById('custom-filename');
    const dropzoneArea = document.getElementById('dropzone-area');
    const cameraInput = document.getElementById('camera-input');
    const galleryInput = document.getElementById('gallery-input');
    const cameraBtn = document.getElementById('camera-btn');
    const galleryBtn = document.getElementById('gallery-btn');
    const previewContainer = document.getElementById('image-preview-container');
    const previewImg = document.getElementById('image-preview');
    const imageName = document.getElementById('image-name');
    const submitScanBtn = document.getElementById('submit-scan-btn');
    const scanLoader = document.getElementById('scan-loader');
    const loaderStatus = document.getElementById('loader-status');
    const loaderBar = document.getElementById('loader-bar');

    const initialPlaceholder = document.getElementById('initial-placeholder');
    const resultsPanel = document.getElementById('results-panel');
    const verdictBanner = document.getElementById('verdict-banner');
    const verdictStatus = document.getElementById('verdict-status');
    const verdictIcon = document.getElementById('verdict-icon');
    const inspectionIdBadge = document.getElementById('inspection-id-badge');
    const evidenceImage = document.getElementById('evidence-image');
    const rulesMatrixTbody = document.getElementById('rules-matrix-tbody');
    const fontAnalysisList = document.getElementById('font-analysis-list');
    const downloadPdfBtn = document.getElementById('download-pdf-btn');

    let selectedFile = null;

    // Toast Notification System with Clean SVG Icons
    function showToast(message, type = 'error') {
        const container = document.getElementById('toast-container');
        if (!container) return;
        const toast = document.createElement('div');
        toast.className = `p-3 rounded shadow-md text-xs font-bold text-white flex items-center gap-2 ${type === 'error' ? 'bg-red-700' : 'bg-green-700'}`;
        const iconSvg = type === 'error'
            ? `<svg class="w-4 h-4 text-red-200 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`
            : `<svg class="w-4 h-4 text-green-200 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>`;
        toast.innerHTML = `${iconSvg}<span>${message}</span>`;
        container.appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
    }

    // Trigger File Inputs
    cameraBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        cameraInput.click();
    });

    galleryBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        galleryInput.click();
    });

    // Drag and Drop Handling
    dropzoneArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzoneArea.classList.add('dragover');
    });

    dropzoneArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropzoneArea.classList.remove('dragover');
    });

    dropzoneArea.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzoneArea.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    cameraInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) handleFile(e.target.files[0]);
    });

    galleryInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) handleFile(e.target.files[0]);
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            showToast('Invalid file format. Upload JPG, PNG or WebP package images.');
            return;
        }
        if (file.size > 10 * 1024 * 1024) {
            showToast('File size exceeds 10MB limit.');
            return;
        }

        selectedFile = file;
        imageName.textContent = file.name;

        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            previewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }

    // Form Submission
    scanForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!selectedFile) {
            showToast('Please upload or take a photograph of the package label.');
            return;
        }

        const customName = customFilenameInput.value.trim() || selectedFile.name;

        // UI Loading States
        submitScanBtn.disabled = true;
        submitScanBtn.classList.add('opacity-50', 'cursor-not-allowed');
        scanLoader.classList.remove('hidden');
        initialPlaceholder.classList.add('hidden');
        resultsPanel.classList.add('hidden');

        // Progress Animation Steps
        let progress = 25;
        loaderBar.style.width = '25%';
        loaderStatus.textContent = 'Applying OpenCV Bilateral Filtering & Adaptive Thresholding...';

        const timer1 = setTimeout(() => {
            progress = 60;
            loaderBar.style.width = '60%';
            loaderStatus.textContent = 'Executing EasyOCR Text Detection & Tokenization...';
        }, 800);

        const timer2 = setTimeout(() => {
            progress = 85;
            loaderBar.style.width = '85%';
            loaderStatus.textContent = 'Analyzing Physical Letter Heights (DPI → mm) & Statutory Rules...';
        }, 1800);

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('custom_name', customName);

        try {
            const response = await fetch('/api/scan', {
                method: 'POST',
                body: formData
            });

            clearTimeout(timer1);
            clearTimeout(timer2);

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Scan processing failed');
            }

            loaderBar.style.width = '100%';
            const data = await response.json();

            setTimeout(() => {
                scanLoader.classList.add('hidden');
                submitScanBtn.disabled = false;
                submitScanBtn.classList.remove('opacity-50', 'cursor-not-allowed');
                renderAuditResults(data);
            }, 400);

        } catch (err) {
            clearTimeout(timer1);
            clearTimeout(timer2);
            scanLoader.classList.add('hidden');
            initialPlaceholder.classList.remove('hidden');
            submitScanBtn.disabled = false;
            submitScanBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            showToast(err.message || 'Scan error occurred');
        }
    });

    function renderAuditResults(data) {
        const report = data.compliance_report;
        const isCompliant = report.overall_status === 'COMPLIANT';

        // Verdict Banner Setup
        verdictStatus.textContent = isCompliant ? 'COMPLIANT (100%)' : `STATUTORY INFRACTION DETECTED`;
        inspectionIdBadge.textContent = `#${data.scan_id}`;

        if (isCompliant) {
            verdictBanner.className = 'rounded-lg p-4 text-white shadow-md flex items-center justify-between bg-[#1E7E34] border-l-8 border-green-300';
            verdictIcon.innerHTML = `<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>`;
        } else {
            verdictBanner.className = 'rounded-lg p-4 text-white shadow-md flex items-center justify-between bg-[#C53030] border-l-8 border-red-300';
            verdictIcon.innerHTML = `<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 18L18 6M6 6l12 12"/></svg>`;
        }

        // Set Evidence Image
        evidenceImage.src = data.evidence_image || data.pdf_report;

        // Render Key Extracted Declarations Summary Grid
        const grid = document.getElementById('structured-declarations-grid');
        if (grid && report.structured_declarations) {
            const sd = report.structured_declarations;
            const items = [
                { label: 'Maximum Retail Price (MRP)', val: sd.mrp, icon: '🏷️' },
                { label: 'Net Quantity', val: sd.net_quantity, icon: '⚖️' },
                { label: 'Mfg / Expiry Date', val: sd.mfg_date, icon: '📅' },
                { label: 'Manufacturer / Packer', val: sd.manufacturer, icon: '🏭' },
                { label: 'Country of Origin', val: sd.country_of_origin, icon: '🇮🇳' },
                { label: 'Consumer Care Contact', val: sd.consumer_care, icon: '📞' }
            ];
            grid.innerHTML = items.map(i => {
                const detected = i.val && i.val !== 'NOT DETECTED';
                return `
                    <div class="p-2.5 rounded border ${detected ? 'bg-blue-50/50 border-blue-200' : 'bg-gray-50 border-gray-200'}">
                        <div class="font-bold text-gray-700 text-[11px] flex items-center gap-1">
                            <span>${i.icon}</span>
                            <span>${i.label}</span>
                        </div>
                        <div class="font-mono text-xs mt-1 ${detected ? 'text-[#1A365D] font-bold' : 'text-gray-400 italic'}">
                            ${detected ? i.val : 'Not Detected'}
                        </div>
                    </div>
                `;
            }).join('');
        }

        // Render Statutory Audit Matrix (6 Mandatory Clauses)
        rulesMatrixTbody.innerHTML = '';
        if (report.rule_results && report.rule_results.length > 0) {
            report.rule_results.forEach(r => {
                const tr = document.createElement('tr');
                const isPass = r.status === 'PASS';
                const snippets = r.matched_snippets && r.matched_snippets.length > 0
                    ? r.matched_snippets.join(', ')
                    : '<span class="text-gray-400 italic">No declaration detected</span>';

                tr.innerHTML = `
                    <td class="font-mono font-bold text-[#1A365D]">${r.rule_id}</td>
                    <td>
                        <div class="font-bold text-gray-800 text-xs">${r.rule_name}</div>
                        <div class="text-[11px] text-gray-500 font-mono">${r.section}</div>
                    </td>
                    <td class="text-xs font-mono">${snippets}</td>
                    <td>
                        <span class="px-2 py-0.5 rounded text-xs font-extrabold ${isPass ? 'badge-compliant' : 'badge-infraction'}">
                            ${r.status}
                        </span>
                    </td>
                `;
                rulesMatrixTbody.appendChild(tr);
            });
        }

        // Render Font Size & Readability Column
        fontAnalysisList.innerHTML = '';
        const fontViolations = report.font_violations || [];
        const fontSummary = report.font_analysis_summary || {};

        if (fontViolations.length === 0) {
            fontAnalysisList.innerHTML = `
                <div class="p-2 bg-green-50 text-green-800 rounded font-semibold flex items-center gap-2">
                    <svg class="w-4 h-4 text-green-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                    <span>All extracted Principal Display Panel text declarations meet statutory font height requirements (≥1.0mm - 2.0mm). Analyzed: ${fontSummary.total_analyzed || 0} text blocks.</span>
                </div>
            `;
        } else {
            fontViolations.forEach(fv => {
                const item = document.createElement('div');
                item.className = 'p-2 bg-amber-50 border border-amber-200 text-amber-900 rounded font-mono text-xs flex justify-between items-center';
                item.innerHTML = `
                    <div>
                        <span class="font-bold">Text:</span> "${fv.text}"
                    </div>
                    <div>
                        Measured: <span class="font-bold text-red-700">${fv.font_size_mm}mm</span> (Min Req: ${fv.min_required_mm}mm) — <span class="badge-warning px-1.5 py-0.5 rounded">ILLEGIBLE / SUB-STANDARD</span>
                    </div>
                `;
                fontAnalysisList.appendChild(item);
            });
        }

        // PDF Download Link Button
        downloadPdfBtn.href = `/api/download-pdf/${data.scan_id}`;

        // Show Results Panel
        resultsPanel.classList.remove('hidden');
        resultsPanel.scrollIntoView({ behavior: 'smooth' });
    }
});
