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

       
    
    