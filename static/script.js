     

     // Global variables
        let selectedRating = 0;
        let currentCRName = '';
        
        const ratingTexts = {
            0: 'একটি রেটিং নির্বাচন করুন',
            1: '😞 খুবই খারাপ',
            2: '😐 খারাপ', 
            3: '😊 মোটামুটি',
            4: '😄 ভালো',
            5: '🌟 চমৎকার!'
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
                document.getElementById('loading').classList.remove('active');
            }, 1000);
        });

        // Navigation functionality with enhanced transitions
        const navLinks = document.querySelectorAll('.nav-link');
        const pages = document.querySelectorAll('.page');

        function showPage(pageId) {
            // Show loading
            const loading = document.getElementById('loading');
            loading.classList.add('active');
            
            setTimeout(() => {
                // Hide all pages
                pages.forEach(page => {
                    page.classList.remove('active');
                });
                
                // Show selected page
                const selectedPage = document.getElementById(pageId);
                if (selectedPage) {
                    selectedPage.classList.add('active');
                }
                
                // Update active nav link
                navLinks.forEach(link => {
                    link.classList.remove('active');
                });
                
                const activeLink = document.querySelector(`[data-page="${pageId}"]`);
                if (activeLink && activeLink.classList.contains('nav-link')) {
                    activeLink.classList.add('active');
                }
                
                // Hide loading
                loading.classList.remove('active');
            }, 300);
        }



        // Add click event listeners to navigation links
        // navLinks.forEach(link => {
        //     link.addEventListener('click', (e) => {
        //         e.preventDefault();
        //         const pageId = link.getAttribute('data-page');
        //         showPage(pageId);
        //     });
        // });

         // View Profile Function
        // function viewProfile(name, id, university, department, photo) {
        //     document.getElementById('profile-name').textContent = name;
        //     document.getElementById('profile-photo').textContent = photo;
        //     document.getElementById('profile-info').textContent = `🆔 আইডি: ${id} | 🏛️ ${university} | 📚 ${department}`;
            
        //     const profileDetails = document.getElementById('profile-details');
        //     profileDetails.innerHTML = `
        //         <div>
        //             <strong style="color: rgba(255,255,255,0.8);">🏛️ বিশ্ববিদ্যালয়:</strong>
        //             <p style="color: white; font-size: 1.1rem; margin-top: 0.5rem;">${university}</p>
        //         </div>
        //         <div>
        //             <strong style="color: rgba(255,255,255,0.8);">📚 বিভাগ:</strong>
        //             <p style="color: white; font-size: 1.1rem; margin-top: 0.5rem;">${department}</p>
        //         </div>
        //         <div>
        //             <strong style="color: rgba(255,255,255,0.8);">📑 সেকশন:</strong>
        //             <p style="color: white; font-size: 1.1rem; margin-top: 0.5rem;">এ (A)</p>
        //         </div>
        //         <div>
        //             <strong style="color: rgba(255,255,255,0.8);">📅 ব্যাচ:</strong>
        //             <p style="color: white; font-size: 1.1rem; margin-top: 0.5rem;">২০২১-২২</p>
        //         </div>
        //     `;
            
        //     showPage('cr-profile');
        // }

        // Rating Modal Functions
        function openRatingModal(crName) {
            currentCRName = crName;
            document.getElementById('rating-cr-name').textContent = `${crName} এর জন্য রেটিং`;
            document.getElementById('rating-modal').style.display = 'block';
            document.body.style.overflow = 'hidden';
            
            // Reset modal
            selectedRating = 0;
            updateRatingDisplay();
            document.getElementById('review-comment').value = '';
        }

        function closeRatingModal() {
            document.getElementById('rating-modal').style.display = 'none';
            document.body.style.overflow = 'auto';
        }

        function updateRatingDisplay() {
            const stars = document.querySelectorAll('.rating-star');
            const ratingText = document.getElementById('rating-text');
            const submitBtn = document.getElementById('submit-rating');
            
            stars.forEach((star, index) => {
                if (index < selectedRating) {
                    star.classList.add('active');
                } else {
                    star.classList.remove('active');
                }
            });
            
            ratingText.textContent = ratingTexts[selectedRating];
            
            if (selectedRating > 0) {
                submitBtn.disabled = false;
                submitBtn.style.opacity = '1';
            } else {
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.5';
            }
        }

        //Add click event listeners to footer links and other page links
        document.querySelectorAll('a[data-page]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const pageId = link.getAttribute('data-page');
                showPage(pageId);
            });
        });

        // Enhanced search functionality
        document.querySelectorAll('.search-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                // Add ripple effect
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
                    showNotification('🔍 খোঁজার ফিচার শীঘ্রই আসছে!', 'info');
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

        //Rating modal event listeners
        // document.getElementById('cancel-rating').addEventListener('click', closeRatingModal);
        
        // document.getElementById('submit-rating').addEventListener('click', () => {
        //     if (selectedRating === 0) return;
            
        //     const comment = document.getElementById('review-comment').value.trim();
        //     const submitBtn = document.getElementById('submit-rating');
            
        //     submitBtn.textContent = '⏳ জমা দেওয়া হচ্ছে...';
        //     submitBtn.disabled = true;
            
        //     setTimeout(() => {
        //         closeRatingModal();
        //         showNotification(`🌟 ${selectedRating} স্টার রেটিং সফলভাবে জমা দেওয়া হয়েছে!`, 'success');
                
        //         // Add the new review to the profile page if we're viewing one
        //         if (document.getElementById('cr-profile').classList.contains('active')) {
        //             addNewReview(selectedRating, comment);
        //         }
        //     }, 1500);
        // });

        // Close modal when clicking outside
        // document.getElementById('rating-modal').addEventListener('click', (e) => {
        //     if (e.target.id === 'rating-modal') {
        //         closeRatingModal();
        //     }
        // });

        // Function to add new review to profile page
        function addNewReview(rating, comment) {
            const reviewsContainer = document.getElementById('reviews-container');
            if (!reviewsContainer) return;
            
            const starHtml = '★'.repeat(rating) + '☆'.repeat(5 - rating);
            const defaultComment = comment || 'কোনো মন্তব্য দেওয়া হয়নি।';
            
            const newReview = document.createElement('div');
            newReview.className = 'review-card';
            newReview.style.animation = 'fadeInUp 0.8s ease';
            newReview.innerHTML = `
                <div class="review-header">
                    <div>
                        <strong>আপনি</strong> - বর্তমান ছাত্র
                        <div class="rating">
                            ${starHtml.split('').map(star => `<span class="star">${star}</span>`).join('')}
                        </div>
                    </div>
                    <div style="color: rgba(255,255,255,0.7);">🕒 এখনই</div>
                </div>
                <div class="review-text">
                    "${defaultComment} 😊"
                </div>
            `;
            
            // Insert at the beginning
            reviewsContainer.insertBefore(newReview, reviewsContainer.firstChild);
            
            // Update review count
            const reviewCount = document.getElementById('review-count');
            if (reviewCount) {
                const currentCount = parseInt(reviewCount.textContent.match(/\d+/)[0]);
                reviewCount.textContent = `(${currentCount + 1}টি রিভিউ এর উপর ভিত্তি করে)`;
            }
        }

         //Enhanced button interactions
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                if (btn.textContent.includes('রেটিং দিন')) {
                    e.preventDefault();
                    showNotification('⭐ রেটিং দেওয়ার ফিচার শীঘ্রই আসছে!', 'success');
                } else if (btn.textContent.includes('প্রোফাইল দেখুন')) {
                    e.preventDefault();
                    showNotification('👤 প্রোফাইল দেখার ফিচার শীঘ্রই আসছে!', 'info');
                } else if (btn.textContent.includes('নতুন সিআর যোগ করুন')) {
                    e.preventDefault();
                    showNotification('➕ নতুন সিআর যোগ করার ফর্ম শীঘ্রই আসছে!', 'warning');
                }
            });
        });

        // Enhanced form submission
        // document.querySelectorAll('form').forEach(form => {
        //     form.addEventListener('submit', (e) => {
        //         e.preventDefault();
        //         const submitBtn = form.querySelector('button[type="submit"]');
        //         const originalText = submitBtn.textContent;
                
        //         submitBtn.textContent = '⏳ প্রক্রিয়াকরণ...';
        //         submitBtn.disabled = true;
                
        //         setTimeout(() => {
        //             submitBtn.textContent = originalText;
        //             submitBtn.disabled = false;
        //             showNotification('🎉 ফর্ম সাবমিশন ফিচার শীঘ্রই আসছে!', 'success');
        //         }, 2000);
        //     });
        // });

       

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

        // Animated statistics counter
        function animateCounters() {
            const statNumbers = document.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {
                const finalValue = stat.textContent;
                const numericValue = parseInt(finalValue.replace(/[^\d]/g, ''));
                let currentValue = 0;
                const increment = Math.ceil(numericValue / 100);
                const duration = 2000; // 2 seconds
                const stepTime = duration / (numericValue / increment);
                
                const timer = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= numericValue) {
                        stat.textContent = finalValue;
                        clearInterval(timer);
                    } else {
                        stat.textContent = currentValue.toLocaleString('bn-BD');
                    }
                }, stepTime);
            });
        }

        // Animate chart bars with enhanced effects
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
            animateCounters();
            animateCharts();
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
                
                showNotification(`⭐ ${rating} স্টার রেটিং দেওয়া হয়েছে!`, 'success');
            });
        });

        //Scroll animations
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

        // Welcome message
        setTimeout(() => {
            showNotification('🎉 বিডি বিশ্ববিদ্যালয় সিআর রিভিউতে স্বাগতম!', 'success');
        }, 2000);
