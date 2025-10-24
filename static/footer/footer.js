document.getElementById('footerContactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const form = this;
    const submitBtn = form.querySelector('.footer-submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');
    const messageDiv = document.getElementById('footerMessage');
    const formData = new FormData(form);
    
    // Disable submit button
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline';
    messageDiv.style.display = 'none';
    
    fetch('{% url "contact_message" %}', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Show message
        messageDiv.style.display = 'block';
        messageDiv.textContent = data.message || data.error;
        
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
    })
    .catch(error => {
        messageDiv.style.display = 'block';
        messageDiv.className = 'footer-message error';
        messageDiv.textContent = 'An error occurred. Please try again.';
        console.error('Error:', error);
    })
    .finally(() => {
        // Re-enable submit button
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    });
});