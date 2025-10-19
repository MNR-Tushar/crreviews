 // Add interactivity
        document.querySelectorAll('.stat-box').forEach(box => {
            box.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.03)';
            });
            box.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });

        // Action button clicks
        // document.querySelectorAll('.action-btn').forEach(btn => {
        //     btn.addEventListener('click', function() {
        //         const action = this.textContent.trim();
        //         alert(`${action} clicked!`);
        //     });
        // });

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

    fetch(`/delete-cr/${deleteSlug}/`, {
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
            // Optionally: পেজ রিফ্রেশ করো বা নির্দিষ্ট এলিমেন্ট রিমুভ করো
            document.querySelector(`#cr-${deleteSlug}`).remove();
        } else {
            alert('Failed to delete profile!');
        }
    })
    .catch(error => console.error('Error:', error));
}

// CSRF token নেওয়ার helper function (Django এর জন্য দরকার)
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


       
    
    