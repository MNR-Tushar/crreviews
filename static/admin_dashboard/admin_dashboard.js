// DOM Elements - Declare first
const sidebar = document.getElementById('sidebar1');
const mainContent = document.getElementById('mainContent1');
const toggleBtn = document.getElementById('toggleBtn1');
const navLinks = document.querySelectorAll('.nav-link1');
const pageContents = document.querySelectorAll('.page-content1');
const pageTitle = document.getElementById('pageTitle1');
const topActionBtn = document.getElementById('topActionBtn1');
const logoutBtn = document.getElementById('logoutBtn1');
const adminProfileInfo = document.getElementById('adminProfileInfo');
const visitorAnalyticsPage = document.getElementById('visitor-analytics');
// Current active page tracking
let currentActivePage = 'dashboard1';

// Page Configuration
const pageConfigs = {
    'dashboard1': {
        title: '📊 Admin Dashboard',
        button: '',
        action: '',
        showAdminInfo: true
    },
    'all-crs1': {
        title: '👥 All CRs Management',
        button: '<span>➕</span><span>Add New CR</span>',
        action: '/admin_dashboard/cr/add/',
        showAdminInfo: false
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
    'visitors1': {
        title: '👤 Visitor Analytics',
        button: '',
        action: 'admin_dashboard/',
    },
    'settings1': {
        title: '⚙️ Settings',
        button: ''
    }
};

// Save active page to localStorage
function saveActivePage(pageName) {
    localStorage.setItem('activeAdminPage', pageName);
}

// Get active page from localStorage
function getActivePage() {
    return localStorage.getItem('activeAdminPage') || 'dashboard1';
}

// Detect current page from URL path
function detectCurrentPageFromPath() {
    const path = window.location.pathname;
    
    // Check for specific patterns and return the correct page
    if (path.includes('/admin_dashboard/university/') || path.includes('/admin/university/')) {
        return 'universities1';
    } else if (path.includes('/admin_dashboard/department/') || path.includes('/admin/department/')) {
        return 'departments1';
    } else if (path.includes('/admin_dashboard/cr/') || path.includes('/admin/cr/')) {
        return 'all-crs1';
    } else if (path.includes('/admin_dashboard/review/') || path.includes('/admin/review/')) {
        return 'reviews1';
    } else if (path.includes('/admin_dashboard/user/') || path.includes('/admin/user/')) {
        return 'users1';
    } else if (path.includes('/admin_dashboard/notice/')) {
        return 'dashboard1';
    } else if (path.includes('/admin_dashboard/message/')) {
        return 'dashboard1';
    } else if (path.includes('/admin_dashboard/developer/')) {
        return 'dashboard1';
    } else if (path.includes('/admin_dashboard/tech-stack/')) {
        return 'dashboard1';
    } else if (path.includes('/admin_dashboard/')) {
        return 'visitors1';
    } 
    else if (path === '/admin_dashboard/' || path === '/admin_dashboard') {
        return getActivePage(); // Get from localStorage when on main dashboard
    }
    
    return null;
}

// Set active nav based on current page
function setActiveNavigation(pageName, showPageContent = true) {
    if (!pageName) return;
    
    // Save to localStorage
    saveActivePage(pageName);
    
    // Remove all active classes
    navLinks.forEach(l => l.classList.remove('active'));
    
    // Set the correct nav link as active
    const targetNavLink = document.querySelector(`[data-page="${pageName}"]`);
    if (targetNavLink) {
        targetNavLink.classList.add('active');
    }
    
    // Update current active page tracker
    currentActivePage = pageName;
    
    // Show/hide admin profile based on page
    const adminProfileInfo = document.getElementById('adminProfileInfo');
    if (adminProfileInfo) {
        adminProfileInfo.style.display = (pageName === 'dashboard1' && showPageContent) ? 'flex' : 'none';
    }
    
    // Only show page content if on main dashboard page
    if (showPageContent) {
        pageContents.forEach(page => page.classList.remove('active'));
        
        const targetPage = document.getElementById(pageName + '-page');
        if (targetPage) {
            targetPage.classList.add('active');
            
            // Update page title and button
            const config = pageConfigs[pageName];
            if (config) {
                if (pageTitle) pageTitle.textContent = config.title;
                if (topActionBtn) {
                    topActionBtn.innerHTML = config.button;
                    topActionBtn.style.display = config.button ? 'inline-flex' : 'none';
                    topActionBtn.setAttribute('data-action', config.action || '');
                }
            }
        }
    }
}

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
        
        // Save active page
        saveActivePage(pageName);
        
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
            
            // Show/hide admin profile
            const adminProfileInfo = document.getElementById('adminProfileInfo');
            if (adminProfileInfo) {
                adminProfileInfo.style.display = (pageName === 'dashboard1') ? 'flex' : 'none';
            }
            
            // Initialize pagination for this page
            initializePaginationForPage(pageName);
        }
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});

function handleUrlFragment() {
    const hash = window.location.hash.substring(1);
    
    if (hash) {
        const fragmentToPage = {
            'departments': 'departments1',
            'universities': 'universities1',
            'users': 'users1',
            'reviews': 'reviews1',
            'crs': 'all-crs1',
            'dashboard': 'dashboard1',
            'visitors': 'visitors1'
        };
        
        const pageName = fragmentToPage[hash];
        
        if (pageName) {
            // Save to localStorage
            saveActivePage(pageName);
            
            const targetNavLink = document.querySelector(`[data-page="${pageName}"]`);
            
            if (targetNavLink) {
                navLinks.forEach(l => l.classList.remove('active'));
                targetNavLink.classList.add('active');
                
                pageContents.forEach(page => page.classList.remove('active'));
                
                const targetPage = document.getElementById(pageName + '-page');
                if (targetPage) {
                    targetPage.classList.add('active');
                    currentActivePage = pageName;
                    
                    const config = pageConfigs[pageName];
                    if (config) {
                        if (pageTitle) pageTitle.textContent = config.title;
                        if (topActionBtn) {
                            topActionBtn.innerHTML = config.button;
                            topActionBtn.style.display = config.button ? 'inline-flex' : 'none';
                            topActionBtn.setAttribute('data-action', config.action || '');
                        }
                    }
                    
                    initializePaginationForPage(pageName);
                }
                
                restoreScrollPosition();
            }
        }
        
        history.replaceState(null, null, window.location.pathname);
    }
}

// Page Load Handler
window.addEventListener('load', () => {
    // First check if we're on a specific page (edit/view/add)
    const detectedPage = detectCurrentPageFromPath();
    
    if (detectedPage) {
        // We're on an edit/view/add page or returning to dashboard
        setActiveNavigation(detectedPage, detectedPage === 'dashboard1' || window.location.pathname === '/admin_dashboard/' || window.location.pathname === '/admin_dashboard');
    } else if (window.location.hash) {
        // If there's a hash, handle it
        handleUrlFragment();
    } else {
        // Default to dashboard or last active page
        const lastActivePage = getActivePage();
        setActiveNavigation(lastActivePage, true);
    }
    
    setTimeout(() => {
        animateCounters();
        initializePaginationForPage(currentActivePage);
        attachActionButtonHandlers();
    }, 500);
});

window.addEventListener('hashchange', handleUrlFragment);

// Dynamic Pagination Handler
function initializePaginationForPage(pageName) {
    const pageElement = document.getElementById(pageName + '-page');
    if (!pageElement) return;
    
    const paginationLinks = pageElement.querySelectorAll('.pagination-btn:not(.pagination-active):not(.pagination-disabled)');
    
    paginationLinks.forEach(link => {
        link.replaceWith(link.cloneNode(true));
    });
    
    const freshPaginationLinks = pageElement.querySelectorAll('.pagination-btn:not(.pagination-active):not(.pagination-disabled)');
    
    freshPaginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const href = this.getAttribute('href');
            if (!href) return;
            
            const url = new URL(href, window.location.origin);
            const params = new URLSearchParams(url.search);
            
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
            
            showLoadingState(pageElement);
            fetchPageData(pageParam, pageNumber, pageElement);
        });
    });
}

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
    
    const spinner = pageElement.querySelector('.loading-spinner-overlay');
    if (spinner) spinner.remove();
}

function fetchPageData(pageParam, pageNumber, pageElement) {
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set(pageParam, pageNumber);
    
    fetch(currentUrl.toString(), {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        const pageId = pageElement.getAttribute('id');
        const newPageContent = doc.getElementById(pageId);
        
        if (newPageContent) {
            pageElement.innerHTML = newPageContent.innerHTML;
            initializePaginationForPage(currentActivePage);
            attachActionButtonHandlers();
            window.history.pushState({}, '', currentUrl.toString());
            pageElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        
        removeLoadingState(pageElement);
    })
    .catch(error => {
        console.error('Error fetching page data:', error);
        removeLoadingState(pageElement);
    });
}

// Logout Functionality
if (logoutBtn) {
    logoutBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (confirm('Are you sure you want to logout?')) {
            localStorage.removeItem('activeAdminPage'); // Clear saved page on logout
            window.location.href = '/logout/';
        }
    });
}

// Scroll Position Management
function saveScrollPosition() {
    localStorage.setItem('scrollPos', window.scrollY);
}

function restoreScrollPosition() {
    const scrollPos = localStorage.getItem('scrollPos');
    if (scrollPos) {
        window.scrollTo(0, parseInt(scrollPos));
        localStorage.removeItem('scrollPos');
    }
}

document.addEventListener('DOMContentLoaded', restoreScrollPosition);

// Action Button Handlers
function attachActionButtonHandlers() {
    // Save current active page before navigation
    document.querySelectorAll('.action-btn1.view, .action-btn1.edit, .action-btn1.delete').forEach(btn => {
        btn.addEventListener('click', function(e) {
            saveActivePage(currentActivePage);
        });
    });

    document.querySelectorAll('.action-btn1.view').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const container = this.closest('[data-slug]');
            const slug = container ? container.getAttribute('data-slug') : null;
            
            if (!slug) return;
            
            saveScrollPosition();
            
            if (currentActivePage === 'universities1') {
                window.location.href = `/admin_dashboard/university/view/${slug}`;
            } else if (currentActivePage === 'departments1') {
                window.location.href = `/admin_dashboard/department/view/${slug}`;
            } else if (currentActivePage === 'all-crs1') {
                window.location.href = `/admin_dashboard/cr/view/${slug}`;
            } else if(currentActivePage === 'reviews1') {
                window.location.href = `/admin_dashboard/review/view/${slug}`;
            } else if(currentActivePage === 'users1') {
                window.location.href = `/admin_dashboard/user/view/${slug}`;
            }
        });
    });

    document.querySelectorAll('.action-btn1.edit').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const container = this.closest('[data-slug]');
            const slug = container ? container.getAttribute('data-slug') : null;
            
            if (!slug) return;
            
            saveScrollPosition();
            
            if (currentActivePage === 'universities1') {
                window.location.href = `/admin_dashboard/university/edit/${slug}`;
            } else if (currentActivePage === 'departments1') {
                window.location.href = `/admin_dashboard/department/edit/${slug}`;
            } else if (currentActivePage === 'all-crs1') {
                window.location.href = `/admin_dashboard/cr/edit/${slug}`;
            } else if(currentActivePage === 'reviews1') {
                window.location.href = `/admin_dashboard/review/edit/${slug}`;
            } else if(currentActivePage === 'users1') {
                window.location.href = `/admin_dashboard/user/edit/${slug}`;
            }
        });
    });

    document.querySelectorAll('.action-btn1.delete').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Are you sure you want to delete this item?')) {
                const container = this.closest('[data-slug]');
                const slug = container ? container.getAttribute('data-slug') : null;
                
                if (!slug) return;
                
                saveScrollPosition();
                
                if (currentActivePage === 'universities1') {
                    window.location.href = `/admin_dashboard/university/delete/${slug}`;
                } else if (currentActivePage === 'departments1') {
                    window.location.href = `/admin_dashboard/department/delete/${slug}`;
                } else if (currentActivePage === 'all-crs1') {
                    window.location.href = `/admin_dashboard/cr/delete/${slug}`;
                } else if(currentActivePage === 'reviews1') {
                    window.location.href = `/admin_dashboard/review/delete/${slug}`;
                } else if(currentActivePage === 'users1') {
                    window.location.href = `/admin_dashboard/user/delete/${slug}`;
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
            saveScrollPosition();
            saveActivePage(currentActivePage);
            window.location.href = action;
        }
    });
}

// Styles
const style = document.createElement('style');
style.textContent = `
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

// Mobile Menu
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
        if (sidebar) sidebar.classList.toggle('active');
    });
    
    document.addEventListener('click', (e) => {
        if (sidebar && sidebar.classList.contains('active')) {
            if (!sidebar.contains(e.target) && e.target !== mobileToggle) {
                sidebar.classList.remove('active');
            }
        }
    });
}

// Chart Animation
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

function showNotification(message, type) {
  const colors = {
    success: "#4CAF50",
    error: "#F44336",
    warning: "#FF9800",
    info: "#2196F3"
  };
  
  const toast = document.createElement("div");
  toast.textContent = message;
  toast.style.position = "fixed";
  toast.style.bottom = "30px";
  toast.style.right = "30px";
  toast.style.background = colors[type] || "#333";
  toast.style.color = "white";
  toast.style.padding = "12px 18px";
  toast.style.borderRadius = "8px";
  toast.style.boxShadow = "0 3px 6px rgba(0,0,0,0.3)";
  toast.style.zIndex = "9999";
  toast.style.opacity = "0";
  toast.style.transition = "opacity 0.3s ease-in-out";
  
  document.body.appendChild(toast);
  
  // fade in
  setTimeout(() => toast.style.opacity = "1", 100);
  // fade out after 3s
  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 500);
  }, 3000);
}
