 // Add interactivity
document.querySelectorAll('.stat-box').forEach(box => {
            box.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.03)';
            });
            box.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
});

       

       
const CSRF_TOKEN = document.querySelector('[name=csrfmiddlewaretoken]').value;
let deleteAction = null;





function confirmDeleteCR(slug, name) {
    deleteAction = { type: 'cr', slug: slug };
    document.getElementById('deleteMessage').textContent = `Are you sure you want to delete "${name}"? This action cannot be undone.`;
    openModal('deleteConfirmModal');
}



function confirmDelete() {
    if (!deleteAction) return;
    
    const url = deleteAction.type === 'cr' 
        ? `/cr/${deleteAction.slug}/delete/` 
        : `/review/${deleteAction.slug}/delete/`;
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': CSRF_TOKEN,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showNotification('Error deleting item', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error deleting item', 'error');
    });
    
    closeModal('deleteConfirmModal');
}












