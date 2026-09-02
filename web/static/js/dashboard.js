document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const exportBtn = document.getElementById('export-btn');
    const recordsTbody = document.getElementById('records-tbody');
    
    let allRecords = [];

    // Fetch records on load
    fetchRecords();

    async function fetchRecords() {
        try {
            const response = await fetch('/api/repository');
            if (response.ok) {
                const data = await response.json();
                allRecords = data.records || [];
                updateStats(allRecords);
                displayRecords(allRecords);
            }
        } catch (error) {
            console.error('Error fetching records:', error);
        }
    }

    function updateStats(records) {
        const total = records.length;
        const compliant = records.filter(r => r.overall_status === 'COMPLIANT').length;
        const nonCompliant = total - compliant;

        document.getElementById('total-scans').textContent = total;
        document.getElementById('compliant-count').textContent = compliant;
        document.getElementById('non-compliant-count').textContent = nonCompliant;
    }

    function displayRecords(records) {
        recordsTbody.innerHTML = '';
        records.forEach(r => {
            const tr = document.createElement('tr');
            const statusClass = r.overall_status === 'COMPLIANT' ? 'compliant' : 'non-compliant';
            tr.innerHTML = `
                <td>${r.scan_id}</td>
                <td>${new Date(r.timestamp).toLocaleString()}</td>
                <td>${r.filename}</td>
                <td class="status-text ${statusClass}">${r.overall_status}</td>
                <td>${r.rules_passed}</td>
                <td>${r.rules_failed}</td>
            `;
            recordsTbody.appendChild(tr);
        });
    }

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const filtered = allRecords.filter(r => 
            r.scan_id.toLowerCase().includes(query) ||
            r.filename.toLowerCase().includes(query) ||
            r.overall_status.toLowerCase().includes(query)
        );
        displayRecords(filtered);
    });

    exportBtn.addEventListener('click', () => {
        window.location.href = '/api/export-csv';
    });
});
