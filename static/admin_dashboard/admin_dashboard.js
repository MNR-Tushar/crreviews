// Admin Dashboard JavaScript with Dynamic Pagination

// DOM Elements
const sidebar = document.getElementById('sidebar1');
const mainContent = document.getElementById('mainContent1');
const toggleBtn = document.getElementById('toggleBtn1');
const navLinks = document.querySelectorAll('.nav-link1');
const pageContents = document.querySelectorAll('.page-content1');
const pageTitle = document.getElementById('pageTitle1');
const topActionBtn = document.getElementById('topActionBtn1');
const logoutBtn = document.getElementById('logoutBtn1');

// Current active page tracking
let currentActivePage = 'dashboard1';

// Page Configuration
const pageConfigs = {
    'dashboard1': {
        title: '📊 Admin Dashboard',
        button: '<span>➕</span><span>Add New CR</span>',
        action: '/admin/cr/add/'
    },
    'all-crs1': {
        title: '👥 All CRs Management',
        button: '<span>➕</span><span>Add New CR</span>',
        action: '/admin/cr/add/'
    },
    'reviews1': {
        title: '📝 Reviews Management',
        button: '<span>📊</span><span>Export Reviews</span>',
        action: 'export_reviews'
    },
    'users1': {
        title: '👤 Users Management',
        button: '<span>➕</span><span>Add User</span>',
        action: '/admin/user/add/'
    },
    'universities1': {
        title: '🏛️ Universities Management',
        button: '<span>➕</span><span>Add University</span>',
        action: '/admin_dashboard/university/add/'
    },
    'departments1': {
        title: '📚 Departments Management',
        button: '<span>➕</span><span>Add Department</span>',
        action: '/admin_dashboard/department/add/'
    },
    'settings1': {
        title: '⚙️ Settings',
        button: ''
    }
};

// Toggle Sidebar
if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
        if (sidebar) sidebar.classList.toggle('collapsed');
        if (mainContent) mainContent.classList.toggle('expanded');
    });
}

// Navigation Links
navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const pageName = this.getAttribute('data-page');
        
        if (!pageName) return;
        
        // Update current active page
        currentActivePage = pageName;
        
        // Remove active class from all links
        navLinks.forEach(l => l.classList.remove('active'));
        
        // Add active class to clicked link
        this.classList.add('active');
        
        // Hide all pages
        pageContents.forEach(page => page.classList.remove('active'));
        
        // Show target page
        const targetPage = document.getElementById(pageName + '-page');
        if (targetPage) {
            targetPage.classList.add('active');
            
            // Update page title and action button
            const config = pageConfigs[pageName];
            if (config) {
                if (pageTitle) pageTitle.textContent = config.title;
                if (topActionBtn) {
                    topActionBtn.innerHTML = config.button;
                    topActionBtn.style.display = config.button ? 'inline-flex' : 'none';
                    topActionBtn.setAttribute('data-action', config.action || '');
                }
            }
            
            // Initialize pagination for this page
            initializePaginationForPage(pageName);
        }
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});

// Dynamic Pagination Handler
function initializePaginationForPage(pageName) {
    const pageElement = document.getElementById(pageName + '-page');
    if (!pageElement) return;
    
    // Find all pagination links in this page
    const paginationLinks = pageElement.querySelectorAll('.pagination-btn:not(.pagination-active):not(.pagination-disabled)');
    
    paginationLinks.forEach(link => {
        // Remove any existing click handlers
        link.replaceWith(link.cloneNode(true));
    });
    
    // Re-query after replacing
    const freshPaginationLinks = pageElement.querySelectorAll('.pagination-btn:not(.pagination-active):not(.pagination-disabled)');
    
    freshPaginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const href = this.getAttribute('href');
            if (!href) return;
            
            // Parse the URL to get page parameter
            const url = new URL(href, window.location.origin);
            const params = new URLSearchParams(url.search);
            
            // Get the page parameter name (e.g., 'page', 'users_page', etc.)
            let pageParam = null;
            let pageNumber = null;
            
            for (const [key, value] of params.entries()) {
                if (key.includes('page')) {
                    pageParam = key;
                    pageNumber = value;
                    break;
                }
            }
            
            if (!pageParam || !pageNumber) return;
            
            // Show loading state
            showLoadingState(pageElement);
            
            // Fetch new data
            fetchPageData(pageParam, pageNumber, pageElement);
        });
    });
}

// Show loading state
function showLoadingState(pageElement) {
    const tables = pageElement.querySelectorAll('.data-table1 tbody');
    const grids = pageElement.querySelectorAll('.university-grid1, .review-card1');
    
    tables.forEach(table => {
        table.style.opacity = '0.5';
        table.style.pointerEvents = 'none';
    });
    
    grids.forEach(grid => {
        grid.style.opacity = '0.5';
        grid.style.pointerEvents = 'none';
    });
    
    // Add loading spinner
    const loadingSpinner = document.createElement('div');
    loadingSpinner.className = 'loading-spinner-overlay';
    loadingSpinner.innerHTML = `
        <div class="spinner">
            <div class="spinner-circle"></div>
            <p>Loading...</p>
        </div>
    `;
    pageElement.appendChild(loadingSpinner);
}

// Remove loading state
function removeLoadingState(pageElement) {
    const tables = pageElement.querySelectorAll('.data-table1 tbody');
    const grids = pageElement.querySelectorAll('.university-grid1, .review-card1');
    
    tables.forEach(table => {
        table.style.opacity = '1';
        table.style.pointerEvents = 'auto';
    });
    
    grids.forEach(grid => {
        grid.style.opacity = '1';
        grid.style.pointerEvents = 'auto';
    });
    
    // Remove loading spinner
    const spinner = pageElement.querySelector('.loading-spinner-overlay');
    if (spinner) spinner.remove();
}

// Fetch page data via AJAX
function fetchPageData(pageParam, pageNumber, pageElement) {
    // Build URL with page parameter
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set(pageParam, pageNumber);
    
    // Fetch data
    fetch(currentUrl.toString(), {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        // Parse the HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        // Find the corresponding page content in the fetched HTML
        const pageId = pageElement.getAttribute('id');
        const newPageContent = doc.getElementById(pageId);
        
        if (newPageContent) {
            // Replace only the inner content, keep the page wrapper
            pageElement.innerHTML = newPageContent.innerHTML;
            
            // Re-initialize pagination for the updated content
            initializePaginationForPage(currentActivePage);
            
            // Re-attach action button handlers
            attachActionButtonHandlers();
            
            // Update URL without reloading
            window.history.pushState({}, '', currentUrl.toString());
            
            // Scroll to top of content
            pageElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        
        removeLoadingState(pageElement);
        
    })
    .catch(error => {
        console.error('Error fetching page data:', error);
        removeLoadingState(pageElement);
        showNotification('Failed to load page. Please try again.', 'error');
    });
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-icon">${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</span>
        <span class="notification-message">${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Logout Functionality
if (logoutBtn) {
    logoutBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (confirm('Are you sure you want to logout?')) {
            window.location.href = '/logout/';
        }
    });
}

// === SCROLL POSITION SAVE/RESTORE SYSTEM ===

// Save scroll position before navigation
function saveScrollPosition() {
    localStorage.setItem('scrollPos', window.scrollY);
}

// Restore scroll position after reload
function restoreScrollPosition() {
    const scrollPos = localStorage.getItem('scrollPos');
    if (scrollPos) {
        window.scrollTo(0, parseInt(scrollPos));
        localStorage.removeItem('scrollPos'); // clear after restore
    }
}

// Call restore on load
document.addEventListener('DOMContentLoaded', restoreScrollPosition);


// === EXISTING FUNCTION MODIFIED BELOW ===

// Attach action button handlers
function attachActionButtonHandlers() {
    // View buttons
    document.querySelectorAll('.action-btn1.view').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            showNotification('View action clicked!', 'info');
        });
    });

    // Edit buttons
    document.querySelectorAll('.action-btn1.edit').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();

            const container = this.closest('[data-slug]');
            const slug = container ? container.getAttribute('data-slug') : null;

            if (!slug) {
                showNotification('Slug not found for this item!', 'error');
                return;
            }

            // ✅ Save scroll before redirect
            saveScrollPosition();

            if (currentActivePage === 'universities1') {
                window.location.href = `/admin_dashboard/university/edit/${slug}`;
            } else if (currentActivePage === 'departments1') {
                window.location.href = `/admin_dashboard/department/edit/${slug}`;
            }
        });
    });

    // Delete buttons
    document.querySelectorAll('.action-btn1.delete').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Are you sure you want to delete this item?')) {
                const container = this.closest('[data-slug]');
                const slug = container ? container.getAttribute('data-slug') : null;

                if (!slug) {
                    showNotification('Slug not found for this item!', 'error');
                    return;
                }

                // ✅ Save scroll before redirect
                saveScrollPosition();

                if (currentActivePage === 'universities1') {
                    window.location.href = `/admin_dashboard/university/delete/${slug}`;
                } else if (currentActivePage === 'departments1') {
                    window.location.href = `/admin_dashboard/department/delete/${slug}`;
                }
            }
        });
    });
}


// Top Action Button
if (topActionBtn) {
    topActionBtn.addEventListener('click', function() {
        const action = this.getAttribute('data-action');
        
        if (action && action.startsWith('/')) {
            // Navigate to the URL
            window.location.href = action;
        } else if (action === 'export_reviews') {
            showNotification('Export feature coming soon!', 'info');
        } else {
            const buttonText = this.textContent.trim();
            showNotification(buttonText + ' feature coming soon!', 'info');
        }
    });
}

// Add CSS for notifications and loading spinner
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
    
    .notification {
        position: fixed;
        top: 20px;
        right: -300px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 1rem;
        z-index: 10000;
        transition: right 0.3s ease;
        min-width: 250px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    .notification.show {
        right: 20px;
    }
    
    .notification-success {
        border-left: 4px solid #4caf50;
    }
    
    .notification-error {
        border-left: 4px solid #f44336;
    }
    
    .notification-info {
        border-left: 4px solid #2196f3;
    }
    
    .notification-icon {
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .notification-success .notification-icon {
        color: #4caf50;
    }
    
    .notification-error .notification-icon {
        color: #f44336;
    }
    
    .notification-info .notification-icon {
        color: #2196f3;
    }
    
    .notification-message {
        color: white;
        font-weight: 500;
    }
    
    .loading-spinner-overlay {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1000;
    }
    
    .spinner {
        text-align: center;
    }
    
    .spinner-circle {
        width: 50px;
        height: 50px;
        border: 4px solid rgba(255, 255, 255, 0.1);
        border-top: 4px solid #4facfe;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
    
    .spinner p {
        color: white;
        font-weight: 600;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

// Animate Statistics
function animateCounters() {
    const statValues = document.querySelectorAll('.stat-value1');
    statValues.forEach(stat => {
        const finalValue = stat.textContent.replace(/,/g, '');
        const numericValue = parseInt(finalValue);
        
        if (isNaN(numericValue)) return;
        
        let currentValue = 0;
        const increment = Math.ceil(numericValue / 100);
        const duration = 2000;
        const stepTime = duration / (numericValue / increment);
        
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= numericValue) {
                stat.textContent = numericValue.toLocaleString();
                clearInterval(timer);
            } else {
                stat.textContent = currentValue.toLocaleString();
            }
        }, stepTime);
    });
}

// Initialize animations on page load
window.addEventListener('load', () => {
    setTimeout(() => {
        animateCounters();
        // Initialize pagination for the default active page
        initializePaginationForPage('dashboard1');
        // Attach action button handlers
        attachActionButtonHandlers();
    }, 500);
});

// Mobile Menu Toggle
if (window.innerWidth <= 1024) {
    const mobileToggle = document.createElement('button');
    mobileToggle.innerHTML = '☰';
    mobileToggle.style.cssText = `
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1001;
        background: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
        width: 45px;
        height: 45px;
        border-radius: 10px;
        font-size: 1.5rem;
        cursor: pointer;
        backdrop-filter: blur(10px);
    `;
    
    document.body.appendChild(mobileToggle);
    
    mobileToggle.addEventListener('click', () => {
        if (sidebar) {
            sidebar.classList.toggle('active');
        }
    });
    
    // Close sidebar when clicking outside
    document.addEventListener('click', (e) => {
        if (sidebar && sidebar.classList.contains('active')) {
            if (!sidebar.contains(e.target) && e.target !== mobileToggle) {
                sidebar.classList.remove('active');
            }
        }
    });
}

// Search Functionality
const searchInputs = document.querySelectorAll('.form-input1[type="text"]');
searchInputs.forEach(input => {
    input.addEventListener('input', function() {
        this.style.borderColor = 'rgba(79, 172, 254, 0.5)';
        this.style.boxShadow = '0 0 20px rgba(79, 172, 254, 0.3)';
        
        setTimeout(() => {
            this.style.borderColor = '';
            this.style.boxShadow = '';
        }, 1000);
    });
});

// Chart Bar Animation
const chartBars = document.querySelectorAll('.chart-bar1');
chartBars.forEach((bar, index) => {
    setTimeout(() => {
        bar.style.animation = 'growBar 1s ease-out forwards';
    }, index * 200);
});

// Add chart animation CSS
const chartStyle = document.createElement('style');
chartStyle.textContent = `
    @keyframes growBar {
        from {
            height: 0;
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
`;
document.head.appendChild(chartStyle);

// Table Row Hover Effect
document.querySelectorAll('.data-table1 tr').forEach(row => {
    row.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.01)';
    });
    
    row.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
});