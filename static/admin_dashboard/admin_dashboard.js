// Admin Dashboard JavaScript

// DOM Elements
const sidebar = document.getElementById('sidebar1');
const mainContent = document.getElementById('mainContent1');
const toggleBtn = document.getElementById('toggleBtn1');
const navLinks = document.querySelectorAll('.nav-link1');
const pageContents = document.querySelectorAll('.page-content1');
const pageTitle = document.getElementById('pageTitle1');
const topActionBtn = document.getElementById('topActionBtn1');
const logoutBtn = document.getElementById('logoutBtn1');

// Page Configuration
const pageConfigs = {
    'dashboard1': {
        title: '📊 Admin Dashboard',
        button: '<span>➕</span><span>Add New CR</span>'
    },
    'all-crs1': {
        title: '👥 All CRs Management',
        button: '<span>➕</span><span>Add New CR</span>'
    },
    'reviews1': {
        title: '📝 Reviews Management',
        button: '<span>📊</span><span>Export Reviews</span>'
    },
    'users1': {
        title: '👤 Users Management',
        button: '<span>➕</span><span>Add User</span>'
    },
    'universities1': {
        title: '🏛️ Universities Management',
        button: '<span>➕</span><span>Add University</span>'
    },
    'departments1': {
        title: '📚 Departments Management',
        button: '<span>➕</span><span>Add Department</span>'
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
                }
            }
        }
    });
});

// Logout Functionality
if (logoutBtn) {
    logoutBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (confirm('Are you sure you want to logout?')) {
            // In production, redirect to logout URL
            alert('Logging out... Redirecting to login page.');
            // window.location.href = '/logout/';
        }
    });
}

// Action Buttons
document.querySelectorAll('.action-btn1').forEach(btn => {
    btn.addEventListener('click', function() {
        const action = this.textContent.trim();
        
        if (action === 'Delete') {
            if (confirm('Are you sure you want to delete this item?')) {
                showNotification(action + ' action confirmed!', 'success');
            }
        } else {
            showNotification(action + ' action clicked!', 'info');
        }
    });
});

// Top Action Button
if (topActionBtn) {
    topActionBtn.addEventListener('click', function() {
        const buttonText = this.textContent.trim();
        showNotification(buttonText + ' feature coming soon!', 'info');
    });
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
        // Add visual feedback
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

// Form Validation Helper
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('.form-input1[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = 'rgba(244, 67, 54, 0.5)';
            isValid = false;
            
            setTimeout(() => {
                input.style.borderColor = '';
            }, 2000);
        }
    });
    
    return isValid;
}

// Print Current Page Statistics
function printStatistics() {
    window.print();
}

// Export Data (Placeholder)
function exportData(format = 'csv') {
    showNotification(`Exporting data as ${format.toUpperCase()}...`, 'info');
    // In production, implement actual export functionality
}