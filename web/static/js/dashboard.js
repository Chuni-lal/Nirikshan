document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const statusFilter = document.getElementById('status-filter');
    const exportBtn = document.getElementById('export-btn');
    const recordsTbody = document.getElementById('records-tbody');

    const totalScansEl = document.getElementById('total-scans');
    const compliantCountEl = document.getElementById('compliant-count');
    const nonCompliantCountEl = document.getElementById('non-compliant-count');
    const complianceRateEl = document.getElementById('compliance-rate');

    let allRecords = [];

    // Fetch repository records on page load
    fetchRecords();

    async function fetchRecords() {
        try {
            const response = await fetch('/api/repository');
            if (response.ok) {
                const data = await response.json();
                allRecords = data.records || [];
                updateMetrics(allRecords);
                renderTable(allRecords);
            } else {
                recordsTbody.innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center py-6 text-red-600 font-bold">
                            Failed to connect to Legal Metrology Repository. Please refresh or check server status.
                        </td>
                    </tr>
                `;
            }
        } catch (error) {
            console.error('Error loading repository:', error);
            recordsTbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center py-6 text-red-600 font-bold">
                        Error fetching records: ${error.message}
                    </td>
                </tr>
            `;
        }
    }

    function updateMetrics(records) {
        const total = records.length;
        const compliant = records.filter(r => r.overall_status === 'COMPLIANT').length;
        const nonCompliant = total - compliant;
        const rate = total > 0 ? ((compliant / total) * 100).toFixed(1) : '0.0';

        totalScansEl.textContent = total;
        compliantCountEl.textContent = compliant;
        nonCompliantCountEl.textContent = nonCompliant;
        complianceRateEl.textContent = `${rate}%`;
    }

    function renderTable(records) {
        recordsTbody.innerHTML = '';

        if (records.length === 0) {
            recordsTbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center py-8 text-gray-500 italic">
                        No inspection records found in repository matching search criteria.
                    </td>
                </tr>
            `;
            return;
        }

        records.forEach(r => {
            const tr = document.createElement('tr');
            const isCompliant = r.overall_status === 'COMPLIANT';
            const statusBadgeClass = isCompliant ? 'badge-compliant' : 'badge-infraction';
            
            const totalRules = (r.rules_passed || 0) + (r.rules_failed || 0);
            const scorePercent = totalRules > 0 ? Math.round((r.rules_passed / totalRules) * 100) : 0;

            const formattedDate = r.timestamp ? new Date(r.timestamp).toLocaleString('en-IN', {
                year: 'numeric', month: 'short', day: '2-digit', hour: '2-digit', minute: '2-digit'
            }) : 'N/A';

            tr.innerHTML = `
                <td class="font-mono font-bold text-[#1A365D]">#${r.scan_id}</td>
                <td class="text-xs font-mono text-gray-600">${formattedDate}</td>
                <td>
                    <div class="font-bold text-gray-800 text-xs">${r.filename}</div>
                    <div class="text-[11px] text-gray-500 font-mono">Inspector ID: INSP-DEL-2026-8841</div>
                </td>
                <td class="text-xs font-mono">
                    <span class="text-green-700 font-bold">${r.rules_passed || 0} Pass</span> / 
                    <span class="text-red-700 font-bold">${r.rules_failed || 0} Fail</span>
                    <div class="w-24 bg-gray-200 h-1.5 rounded-full overflow-hidden mt-1">
                        <div class="${isCompliant ? 'bg-green-600' : 'bg-red-600'} h-full" style="width: ${scorePercent}%"></div>
                    </div>
                </td>
                <td>
                    <span class="px-2.5 py-1 rounded text-xs font-extrabold ${statusBadgeClass}">
                        ${r.overall_status}
                    </span>
                </td>
                <td>
                    <a href="/api/download-pdf/${r.scan_id}" target="_blank"
                       class="inline-flex items-center gap-1 px-2.5 py-1 bg-[#1A365D] hover:bg-blue-900 text-white text-xs font-bold rounded shadow transition">
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                        <span>PDF Notice</span>
                    </a>
                </td>
            `;
            recordsTbody.appendChild(tr);
        });
    }

    // Search and Filter Handlers
    function applyFilters() {
        const query = searchInput.value.toLowerCase().trim();
        const selectedStatus = statusFilter.value;

        const filtered = allRecords.filter(r => {
            const matchesQuery = (
                r.scan_id.toLowerCase().includes(query) ||
                r.filename.toLowerCase().includes(query) ||
                r.overall_status.toLowerCase().includes(query)
            );
            const matchesStatus = (selectedStatus === 'ALL' || r.overall_status === selectedStatus);

            return matchesQuery && matchesStatus;
        });

        renderTable(filtered);
    }

    searchInput.addEventListener('input', applyFilters);
    statusFilter.addEventListener('change', applyFilters);

    exportBtn.addEventListener('click', () => {
        window.location.href = '/api/export-csv';
    });
});
