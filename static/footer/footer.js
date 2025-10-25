// Footer.js - Simple form validation (optional)
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('footerContactForm');
    
    if (!form) return;
    
    // Optional: Add loading state to button
    form.addEventListener('submit', function(e) {
        const submitBtn = form.querySelector('.footer-submit-btn');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sending...';
        }
    });
});