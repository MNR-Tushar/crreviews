// Global variables
let selectedRating = 0;
let currentCRName = '';

const ratingTexts = {
    0: 'Select a rating',
    1: '😞 Very Bad',
    2: '😐 Bad', 
    3: '😊 Average',
    4: '😄 Good',
    5: '🌟 Excellent!'
};

// Create floating particles
function createParticles() {
    for (let i = 0; i < 15; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 6 + 's';
        particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
        document.body.appendChild(particle);
    }
}
createParticles();

// Show loading screen initially
window.addEventListener('load', () => {
    setTimeout(() => {
        const loading = document.getElementById('loading');
        if (loading) {
            loading.classList.remove('active');
        }
    }, 1000);
});

// Navigation functionality with enhanced transitions
const navLinks = document.querySelectorAll('.nav-link');
const pages = document.querySelectorAll('.page');

function showPage(pageId) {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.classList.add('active');
    }
    
    setTimeout(() => {
        pages.forEach(page => {
            page.classList.remove('active');
        });
        
        const selectedPage = document.getElementById(pageId);
        if (selectedPage) {
            selectedPage.classList.add('active');
        }
        
        navLinks.forEach(link => {
            link.classList.remove('active');
        });
        
        const activeLink = document.querySelector(`[data-page="${pageId}"]`);
        if (activeLink && activeLink.classList.contains('nav-link')) {
            activeLink.classList.add('active');
        }
        
        if (loading) {
            loading.classList.remove('active');
        }
    }, 300);
}

// Rating Modal Functions
function openRatingModal(crName) {
    currentCRName = crName;
    const modal = document.getElementById('rating-modal');
    
    if (!modal) {
        console.warn('Rating modal not found');
        return;
    }
    
    const modalTitle = document.getElementById('rating-cr-name');
    if (modalTitle) {
        modalTitle.textContent = `Rating for ${crName}`;
    }
    
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    selectedRating = 0;
    updateRatingDisplay();
    
    const commentField = document.getElementById('review-comment');
    if (commentField) {
        commentField.value = '';
    }
}

function closeRatingModal() {
    const modal = document.getElementById('rating-modal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    const modal = document.getElementById('rating-modal');
    if (modal && e.target === modal) {
        closeRatingModal();
    }
});

// Add event listeners for modal buttons
document.addEventListener('DOMContentLoaded', () => {
    const cancelBtn = document.getElementById('cancel-rating');
    const submitBtn = document.getElementById('submit-rating');
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', closeRatingModal);
    }
    
    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            if (selectedRating > 0) {
                const comment = document.getElementById('review-comment')?.value || '';
                addNewReview(selectedRating, comment);
                showNotification(`⭐ ${selectedRating} star rating submitted!`, 'success');
                closeRatingModal();
            }
        });
    }
});

// Enhanced search functionality
document.querySelectorAll('.search-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255,255,255,0.6);
            width: 20px;
            height: 20px;
            animation: ripple 0.6s ease-out;
            pointer-events: none;
        `;
        btn.style.position = 'relative';
        btn.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
            showNotification('🔍 Search feature coming soon!', 'info');
        }, 100);
    });
});

// Rating star click handlers
document.querySelectorAll('.rating-star').forEach(star => {
    star.addEventListener('click', () => {
        selectedRating = parseInt(star.getAttribute('data-value'));
        updateRatingDisplay();
    });
    
    star.addEventListener('mouseenter', () => {
        const hoverRating = parseInt(star.getAttribute('data-value'));
        const stars = document.querySelectorAll('.rating-star');
        
        stars.forEach((s, index) => {
            if (index < hoverRating) {
                s.style.color = '#ffeb3b';
                s.style.transform = 'scale(1.1)';
            } else {
                s.style.color = 'rgba(255,255,255,0.3)';
                s.style.transform = 'scale(1)';
            }
        });
    });
    
    star.addEventListener('mouseleave', () => {
        updateRatingDisplay();
    });
});

// Function to add new review to profile page
function addNewReview(rating, comment) {
    const reviewsContainer = document.getElementById('reviews-container');
    if (!reviewsContainer) return;
    
    const starHtml = '★'.repeat(rating) + '☆'.repeat(5 - rating);
    const defaultComment = comment || 'No comment provided.';
    
    const newReview = document.createElement('div');
    newReview.className = 'review-card';
    newReview.style.animation = 'fadeInUp 0.8s ease';
    newReview.innerHTML = `
        <div class="review-header">
            <div>
                <strong>You</strong> - Current Student
                <div class="rating">
                    ${starHtml.split('').map(star => `<span class="star">${star}</span>`).join('')}
                </div>
            </div>
            <div style="color: rgba(255,255,255,0.7);">🕒 Just now</div>
        </div>
        <div class="review-text">
            "${defaultComment} 😊"
        </div>
    `;
    
    reviewsContainer.insertBefore(newReview, reviewsContainer.firstChild);
    
    const reviewCount = document.getElementById('review-count');
    if (reviewCount) {
        const currentCount = parseInt(reviewCount.textContent.match(/\d+/)[0]);
        reviewCount.textContent = `(Based on ${currentCount + 1} reviews)`;
    }
}

// Enhanced button interactions - DO NOT prevent form submissions
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        // Allow form submit buttons to work normally
        if (btn.type === 'submit' || btn.closest('form')) {
            return;
        }
        
        if (btn.textContent.includes('Rate') || btn.textContent.includes('রেটিং')) {
            e.preventDefault();
            showNotification('⭐ Rating feature coming soon!', 'success');
        } else if (btn.textContent.includes('Profile') || btn.textContent.includes('প্রোফাইল')) {
            e.preventDefault();
            showNotification('👤 Profile view coming soon!', 'info');
        } else if (btn.textContent.includes('Add CR') || btn.textContent.includes('সিআর যোগ')) {
            e.preventDefault();
            showNotification('➕ Add CR form coming soon!', 'warning');
        }
    });
});

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    const colors = {
        info: 'linear-gradient(135deg, #4facfe, #00f2fe)',
        success: 'linear-gradient(135deg, #11998e, #38ef7d)',
        warning: 'linear-gradient(135deg, #f093fb, #f5576c)',
        error: 'linear-gradient(135deg, #ff6b6b, #ee5a24)'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type]};
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 10000;
        font-weight: 600;
        backdrop-filter: blur(10px);
        animation: slideIn 0.5s ease;
        max-width: 350px;
        word-wrap: break-word;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.5s ease forwards';
        setTimeout(() => {
            notification.remove();
        }, 500);
    }, 3000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    @keyframes ripple {
        from { width: 20px; height: 20px; opacity: 0.8; }
        to { width: 200px; height: 200px; opacity: 0; }
    }
`;
document.head.appendChild(style);

// Enhanced mobile menu
const mobileMenu = document.querySelector('.mobile-menu');
const navLinksContainer = document.querySelector('.nav-links');

if (mobileMenu && navLinksContainer) {
    mobileMenu.addEventListener('click', () => {
        const isVisible = navLinksContainer.style.display === 'flex';
        
        if (isVisible) {
            navLinksContainer.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => {
                navLinksContainer.style.display = 'none';
            }, 300);
        } else {
            navLinksContainer.style.display = 'flex';
            navLinksContainer.style.flexDirection = 'column';
            navLinksContainer.style.position = 'absolute';
            navLinksContainer.style.top = '100%';
            navLinksContainer.style.left = '0';
            navLinksContainer.style.right = '0';
            navLinksContainer.style.background = 'rgba(255, 255, 255, 0.1)';
            navLinksContainer.style.backdropFilter = 'blur(30px)';
            navLinksContainer.style.padding = '2rem';
            navLinksContainer.style.borderRadius = '0 0 25px 25px';
            navLinksContainer.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)';
            navLinksContainer.style.animation = 'slideIn 0.3s ease forwards';
        }
    });
}

// Animated statistics counter
function animateCounters() {
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => {
        const finalValue = stat.textContent;
        const numericValue = parseInt(finalValue.replace(/[^\d]/g, ''));
        if (isNaN(numericValue)) return;
        
        let currentValue = 0;
        const increment = Math.ceil(numericValue / 100);
        const duration = 2000;
        const stepTime = duration / (numericValue / increment);
        
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= numericValue) {
                stat.textContent = finalValue;
                clearInterval(timer);
            } else {
                stat.textContent = currentValue.toLocaleString();
            }
        }, stepTime);
    });
}

// Animate chart bars
function animateCharts() {
    const chartFills = document.querySelectorAll('.chart-fill');
    chartFills.forEach((fill, index) => {
        const width = fill.style.width;
        fill.style.width = '0%';
        setTimeout(() => {
            fill.style.width = width;
        }, 200 * (index + 1));
    });
}

// Initialize animations when home page loads
setTimeout(() => {
    if (document.querySelectorAll('.stat-number').length > 0) {
        animateCounters();
    }
    if (document.querySelectorAll('.chart-fill').length > 0) {
        animateCharts();
    }
}, 1500);

// Enhanced card hover effects
document.querySelectorAll('.card, .stat-card, .review-card').forEach(card => {
    card.addEventListener('mouseenter', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px) scale(1.02)`;
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0) scale(1)';
    });
});

// Enhanced star rating interactions
document.querySelectorAll('.star').forEach(star => {
    star.addEventListener('click', () => {
        const stars = star.parentElement.querySelectorAll('.star');
        const rating = Array.from(stars).indexOf(star) + 1;
        
        stars.forEach((s, index) => {
            if (index < rating) {
                s.textContent = '★';
                s.style.color = '#ffeb3b';
            } else {
                s.textContent = '☆';
                s.style.color = 'rgba(255,255,255,0.3)';
            }
        });
        
        showNotification(`⭐ ${rating} star rating given!`, 'success');
    });
});

// Scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.8s ease forwards';
        }
    });
}, observerOptions);

// Observe all cards and sections
document.querySelectorAll('.card, .section, .stat-card').forEach(el => {
    observer.observe(el);
});

// Welcome message - only show on home page
// setTimeout(() => {
//     if (window.location.pathname === '/' || document.getElementById('home')) {
//         showNotification('🎉 Welcome to BD University CR Review!', 'success');
//     }
// }, 2000);
setTimeout(() => {
    if ((window.location.pathname === '/' || document.getElementById('home')) 
        && !localStorage.getItem('welcomeShown')) {
        
        showNotification('🎉 Welcome to BD University CR Review!', 'success');
        sessionStorage.setItem('welcomeShown', 'true');
    }
}, 2000);
