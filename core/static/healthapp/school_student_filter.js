document.addEventListener('DOMContentLoaded', function() {
    const schoolSelect = document.getElementById('schoolSelect');
    const studentSelect = document.getElementById('studentSelect');
    const remarksContainer = document.getElementById('remarksContainer');
    const remarksText = document.getElementById('remarksText');
  
    // Initialize SlimSelect for searchable dropdown
    if (studentSelect) {
      new SlimSelect({
        select: '#studentSelect',
        settings: {
          placeholderText: 'Search student...',
          searchPlaceholder: 'Type name to search...'
        }
      });
    }
  
    function filterStudentsBySchool() {
        const selectedSchool = String(schoolSelect?.value);
  
        Array.from(studentSelect.options).forEach(opt => {
            if (opt.value === "") { opt.style.display = ''; return; }
  
            const studentSchool = String(opt.dataset.school);
            opt.style.display = (!selectedSchool || studentSchool === selectedSchool) ? '' : 'none';
        });
  
        // Reset selected student if it’s hidden
        if (studentSelect.selectedOptions[0]?.style.display === 'none') {
            studentSelect.value = "";
            if (remarksContainer) remarksContainer.style.display = "none";
        }
    }
  
    async function fetchLastRemarks(studentId) {
        if (!remarksContainer || !remarksText) return;
  
        if (!studentId) {
            remarksContainer.style.display = "none";
            remarksText.textContent = "";
            return;
        }
  
        try {
            const res = await fetch(`/get_last_remarks/?student_id=${studentId}`);
            const data = await res.json();
  
            if (data.remarks) {
                remarksText.textContent = data.remarks;
                remarksContainer.style.display = 'block';
            } else {
                remarksContainer.style.display = 'none';
            }
        } catch {
            remarksContainer.style.display = 'none';
        }
    }
  
    // Event listeners
    schoolSelect?.addEventListener('change', filterStudentsBySchool);
  
    studentSelect?.addEventListener('change', function () {
        const studentId = this.value;
        fetchLastRemarks(studentId);
    });
  
    // Initial filter
    filterStudentsBySchool();
  });
  