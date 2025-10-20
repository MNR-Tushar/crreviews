// Fixed Review Modal Functions
let currentReviewSlug = '';

function openEditReviewModal(slug, rating, description) {
    currentReviewSlug = slug;
    
    // Set form action
    const form = document.getElementById('editReviewForm');
    if (form) {
        form.action = `/edit_review/${slug}/`;
    }
    
    // Set rating value
    const ratingInput = document.getElementById('editRatingValue');
    if (ratingInput) {
        ratingInput.value = rating;
    }
    
    // Set description
    const descriptionInput = document.getElementById('editReviewComment');
    if (descriptionInput) {
        descriptionInput.value = description;
    }
    
    // Update star display
    updateEditStarDisplay(rating);
    
    // Show modal
    const modal = document.getElementById('editReviewModal');
    if (modal) {
        modal.classList.add('show');
        modal.style.display = 'flex';
    }
    
    console.log('Edit modal opened for slug:', slug);
}

function setEditRating(value) {
    const ratingInput = document.getElementById('editRatingValue');
    if (ratingInput) {
        ratingInput.value = value;
    }
    updateEditStarDisplay(value);
}

function updateEditStarDisplay(rating) {
    const stars = document.querySelectorAll('.rating-star-edit');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('active');
            star.style.color = '#ffeb3b';
            star.style.textShadow = '0 0 20px rgba(255, 235, 59, 0.8)';
        } else {
            star.classList.remove('active');
            star.style.color = 'rgba(255, 255, 255, 0.3)';
            star.style.textShadow = 'none';
        }
    });
}

function closeReviewModal() {
    const modal = document.getElementById('editReviewModal');
    if (modal) {
        modal.classList.remove('show');
        modal.style.display = 'none';
    }
}

function openDeleteReviewModal(slug) {
    currentReviewSlug = slug;
    const modal = document.getElementById('deleteReviewModal');
    if (modal) {
        modal.classList.add('show');
        modal.style.display = 'flex';
    }
    
    console.log('Delete modal opened for slug:', slug);
}

function closeDeleteReviewModal() {
    const modal = document.getElementById('deleteReviewModal');
    if (modal) {
        modal.classList.remove('show');
        modal.style.display = 'none';
    }
}

function confirmDeleteReview() {
    if (currentReviewSlug) {
        window.location.href = `/delete_review/${currentReviewSlug}/`;
    }
}

// Close modals when clicking outside
document.addEventListener('click', function(event) {
    const editModal = document.getElementById('editReviewModal');
    const deleteModal = document.getElementById('deleteReviewModal');
    
    if (editModal && event.target === editModal) {
        closeReviewModal();
    }
    if (deleteModal && event.target === deleteModal) {
        closeDeleteReviewModal();
    }
});

// Close modals when pressing Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeReviewModal();
        closeDeleteReviewModal();
    }
});