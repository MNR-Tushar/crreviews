// Add interactivity
document.querySelectorAll('.stat-box').forEach(box => {
    box.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px) scale(1.03)';
    });
    box.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

let deleteSlug = null;

function openDeleteModal(slug, name) {
    deleteSlug = slug;
    document.getElementById('deleteMessage').innerText = `Are you sure you want to delete "${name}"?`;
    document.getElementById('deleteConfirmModal').style.display = 'block';
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

function confirmDelete() {
    if (!deleteSlug) return;

    fetch(`/delete_cr/${deleteSlug}/`, {  // ✅ underscore ব্যবহার করুন
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeModal('deleteConfirmModal');
            
            const crElement = document.querySelector(`#cr-${deleteSlug}`);
            if (crElement) {
                crElement.remove();
            }
          
            setTimeout(() => {
                location.reload();
            }, 500);
        } else {
            alert('Failed to delete profile!');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error deleting profile!');
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}