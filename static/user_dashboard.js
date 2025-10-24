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



document.addEventListener("DOMContentLoaded", function() {

    // Fixed Review Modal Functions
    let currentReviewSlug = '';

    window.openEditReviewModal = function(slug, rating, description) {
        currentReviewSlug = slug;
        
        const form = document.getElementById('editReviewForm');
        if (form) form.action = `/edit_review/${slug}/`;

        const ratingInput = document.getElementById('editRatingValue');
        if (ratingInput) ratingInput.value = rating;

        const descriptionInput = document.getElementById('editReviewComment');
        if (descriptionInput) descriptionInput.value = description;

        updateEditStarDisplay(rating);

        const modal = document.getElementById('editReviewModal');
        if (modal) {
            modal.classList.add('show');
            modal.style.display = 'flex';
        }

        console.log('✅ Edit modal opened for slug:', slug);
    }

    window.setEditRating = function(value) {
        const ratingInput = document.getElementById('editRatingValue');
        if (ratingInput) ratingInput.value = value;
        updateEditStarDisplay(value);
    }

   function updateEditStarDisplay(rating) {
    rating = parseInt(rating) || 0;  // Convert string to number, default 0

    const stars = document.querySelectorAll('.rating-star-edit');

    stars.forEach((star, index) => {
        if (index < rating) {
            star.style.opacity = '1';
            star.style.transform = 'scale(1.2)';
        } else {
            star.style.opacity = '0.3';
            star.style.transform = 'scale(1)';
        }
    });

    const ratingTexts = [
        'Select a rating',
        '⭐ Poor',
        '⭐⭐ Fair',
        '⭐⭐⭐ Good',
        '⭐⭐⭐⭐ Very Good',
        '⭐⭐⭐⭐⭐ Excellent'
    ];
    const ratingTextElement = document.getElementById('editRatingText');
    if (ratingTextElement) ratingTextElement.textContent = ratingTexts[rating];
}


    window.closeReviewModal = function() {
        const modal = document.getElementById('editReviewModal');

        if (modal) {
            modal.classList.remove('show');
            modal.style.display = 'none';
        }
    }

    window.openDeleteReviewModal = function(slug) {
        currentReviewSlug = slug;
        const modal = document.getElementById('deleteReviewModal');
        if (modal) {
            modal.classList.add('show');
            modal.style.display = 'flex';
        }
        console.log('✅ Delete modal opened for slug:', slug);
    }

    window.closeDeleteReviewModal = function() {
        const modal = document.getElementById('deleteReviewModal');
        if (modal) {
            modal.classList.remove('show');
            modal.style.display = 'none';
        }
    }

    window.confirmDeleteReview = function() {
        if (currentReviewSlug) {
            window.location.href = `/delete_review/${currentReviewSlug}/`;
        }
    }

    // Close modals when clicking outside
    document.addEventListener('click', function(event) {
        const editModal = document.getElementById('editReviewModal');
        const deleteModal = document.getElementById('deleteReviewModal');
        
        if (editModal && event.target === editModal) closeReviewModal();
        if (deleteModal && event.target === deleteModal) closeDeleteReviewModal();
    });

    // Close modals when pressing Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeReviewModal();
            closeDeleteReviewModal();
        }
    });
});
