// Client-side checks. Flask validates the same rules again server-side.
document.querySelectorAll('form[data-check]').forEach(form => {
  form.addEventListener('submit', event => {
    const errors = [];
    const kind = form.dataset.check;
    if (kind === 'register') {
      if (!form.elements.name.value.trim()) errors.push('Name is required');
      if (!form.elements.email.value.trim()) errors.push('Email is required');
      if (!form.elements.password.value) errors.push('Password is required');
      if (!form.elements.confirm_password.value) errors.push('Confirm password is required');
      if (form.elements.password.value && form.elements.confirm_password.value &&
          form.elements.password.value !== form.elements.confirm_password.value) errors.push('Passwords do not match');
    } else if (kind === 'login') {
      if (!form.elements.email.value.trim()) errors.push('Email is required');
      if (!form.elements.password.value) errors.push('Password is required');
    } else if (kind === 'title') {
      if (!form.elements.title.value.trim()) errors.push('Title is required');
      else if (form.elements.title.value.trim().length > 200) errors.push('Title is too long');
    }
    if (errors.length) {
      event.preventDefault();
      const alert = document.getElementById('client-errors') || form.closest('.task')?.querySelector('.edit-errors');
      if (alert) { alert.textContent = errors.join(' · '); alert.classList.remove('hidden'); }
      else window.alert(errors.join('\n'));
    }
  });
});
document.querySelectorAll('.delete-form').forEach(form => {
  form.addEventListener('submit', event => {
    if (!window.confirm('Are you sure you want to delete this task?')) event.preventDefault();
  });
});
document.querySelectorAll('.edit-toggle').forEach(button => {
  button.addEventListener('click', () => {
    const form = button.closest('.task').querySelector('.edit-form');
    const opening = form.classList.contains('hidden');
    form.classList.toggle('hidden');
    button.setAttribute('aria-expanded', opening ? 'true' : 'false');
    if (opening) form.elements.title.focus();
  });
});

// Library delete prompts (including ON DELETE CASCADE warning).
document.querySelectorAll('.confirm-delete').forEach(form => {
  form.addEventListener('submit', event => {
    if (!window.confirm(form.dataset.confirm || 'Are you sure?')) event.preventDefault();
  });
});
