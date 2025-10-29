     const sidebar = document.getElementById('sidebar1');
        const mainContent = document.getElementById('mainContent1');
        const toggleBtn = document.getElementById('toggleBtn1');
        const navLinks = document.querySelectorAll('.nav-link1');
        const pageContents = document.querySelectorAll('.page-content1');
        const pageTitle = document.getElementById('pageTitle1');
        const topActionBtn = document.getElementById('topActionBtn1');
        const logoutBtn = document.getElementById('logoutBtn1');

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

        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('expanded');
        });

        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const pageName = this.getAttribute('data-page');
                
                if (!pageName) return;
                
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
                
                pageContents.forEach(page => page.classList.remove('active'));
                
                const targetPage = document.getElementById(pageName + '-page');
                if (targetPage) {
                    targetPage.classList.add('active');
                    const config = pageConfigs[pageName];
                    if (config) {
                        pageTitle.textContent = config.title;
                        topActionBtn.innerHTML = config.button;
                        topActionBtn.style.display = config.button ? 'inline-flex' : 'none';
                    }
                }
            });
        });

        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Are you sure you want to logout?')) {
                alert('Logging out... Redirecting to login page.');
            }
        });

        document.querySelectorAll('.action-btn1').forEach(btn => {
            btn.addEventListener('click', function() {
                const action = this.textContent.trim();
                if (action === 'Delete') {
                    if (confirm('Are you sure you want to delete this item?')) {
                        alert(action + ' action confirmed!');
                    }
                } else {
                    alert(action + ' action clicked!');
                }
            });
        });