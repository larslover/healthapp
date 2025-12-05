// school_student_filter.js

document.addEventListener('DOMContentLoaded', function() {
  const schoolSelect = document.getElementById('schoolSelect');
  const studentSelect = document.getElementById('studentSelect');
  const remarksContainer = document.getElementById('remarksContainer');
  const remarksText = document.getElementById('remarksText');

  function filterStudentsBySchool() {
      const selectedSchool = schoolSelect?.value;

      Array.from(studentSelect.options).forEach(opt => {
          if (opt.value === "") { opt.style.display = ''; return; }

          const studentSchool = opt.dataset.school;
          opt.style.display = (!selectedSchool || studentSchool === selectedSchool) ? '' : 'none';
      });

      // Reset if hidden
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

  async function fetchPreviousScreenings(studentId) {
      const card = document.getElementById('screeningsSummaryCard');
      const content = document.getElementById('screeningsSummaryContent');

      if (!card || !content) return;
      if (!studentId) {
          card.classList.add('d-none');
          content.innerHTML = "";
          return;
      }

      try {
          const res = await fetch(`/get_previous_screenings/?student_id=${studentId}`);
          const data = await res.json();

          content.innerHTML = data.html?.trim() || '<p class="text-muted">No previous screenings found.</p>';
          card.classList.remove('d-none');
      } catch {
          content.innerHTML = '<p class="text-danger">Failed to load previous screenings.</p>';
          card.classList.remove('d-none');
      }
  }

  // EVENT LISTENERS
  schoolSelect?.addEventListener('change', filterStudentsBySchool);

  studentSelect?.addEventListener('change', function () {
      const studentId = this.value;
      fetchLastRemarks(studentId);
      fetchPreviousScreenings(studentId);
  });

  // INITIAL FILTER
  filterStudentsBySchool();
});
