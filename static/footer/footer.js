// ✅ FIX: Footer contact form submission
document.getElementById('footerContactForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const form = this;
    const submitBtn = form.querySelector('.footer-submit-btn');
    const btnText = submitBtn?.querySelector('.btn-text');
    const btnLoading = submitBtn?.querySelector('.btn-loading');
    const messageDiv = document.getElementById('footerMessage');
    const formData = new FormData(form);
    
    // Disable submit button
    if (submitBtn) {
        submitBtn.disabled = true;
    }
    if (btnText) btnText.style.display = 'none';
    if (btnLoading) btnLoading.style.display = 'inline';
    if (messageDiv) messageDiv.style.display = 'none';
    
    // ✅ FIX: Get URL from form action instead of Django template tag
    const actionUrl = form.action || '/contact-message/'; // Fallback URL
    
    fetch(actionUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Show message
        if (messageDiv) {
            messageDiv.style.display = 'block';
            messageDiv.textContent = data.message || data.error || 'Message sent successfully!';
            
            if (data.success) {
                messageDiv.className = 'footer-message success';
                form.reset(); // Clear form on success
                
                // Hide success message after 5 seconds
                setTimeout(() => {
                    messageDiv.style.display = 'none';
                }, 5000);
            } else {
                messageDiv.className = 'footer-message error';
            }
        }
    })
    .catch(error => {
        if (messageDiv) {
            messageDiv.style.display = 'block';
            messageDiv.className = 'footer-message error';
            messageDiv.textContent = 'An error occurred. Please try again.';
        }
        console.error('Error:', error);
    })
    .finally(() => {
        // Re-enable submit button
        if (submitBtn) submitBtn.disabled = false;
        if (btnText) btnText.style.display = 'inline';
        if (btnLoading) btnLoading.style.display = 'none';
    });
});

// Helper function to get CSRF token
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