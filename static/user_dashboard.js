 // Add interactivity
        document.querySelectorAll('.stat-box').forEach(box => {
            box.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.03)';
            });
            box.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });

        // Action button clicks
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const action = this.textContent.trim();
                alert(`${action} clicked!`);
            });
        });

        // Edit profile button
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const text = this.textContent.trim();
                if (text.includes('Edit Profile')) {
                    alert('Edit Profile feature coming soon!');
                } else if (text.includes('Settings')) {
                    alert('Settings page coming soon!');
                }
            });
        });

        // Saved CR items click
        document.querySelectorAll('.saved-cr-item').forEach(item => {
            item.addEventListener('click', function() {
                const name = this.querySelector('h4').textContent;
                alert(`Viewing ${name}'s profile`);
            });
        });