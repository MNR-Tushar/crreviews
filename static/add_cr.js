// File upload functionality
        const fileInput = document.getElementById('profilePicture');
        const uploadZone = document.getElementById('uploadZone');
        const previewSection = document.getElementById('previewSection');
        const previewImage = document.getElementById('previewImage');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const removeBtn = document.getElementById('removeBtn');
        const form = document.getElementById('addCrForm');
        const progressIndicator = document.getElementById('progressIndicator');

        // File input change event
        fileInput.addEventListener('change', handleFileSelect);

        // Drag and drop events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => {
                uploadZone.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => {
                uploadZone.classList.remove('dragover');
            });
        });

        uploadZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                handleFileSelect();
            }
        });

        // Handle file selection
        function handleFileSelect() {
            const file = fileInput.files[0];
            if (!file) return;

            // Validate file size (5MB)
            if (file.size > 5 * 1024 * 1024) {
                showNotification('File size must be less than 5MB', 'error');
                fileInput.value = '';
                return;
            }

            // Validate file type
            if (!file.type.startsWith('image/')) {
                showNotification('Please select an image file', 'error');
                fileInput.value = '';
                return;
            }

            // Show preview
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                fileName.textContent = file.name;
                fileSize.textContent = formatFileSize(file.size);
                previewSection.style.display = 'block';
                uploadZone.style.display = 'none';
            };
            reader.readAsDataURL(file);
        }

        // Remove file
        removeBtn.addEventListener('click', () => {
            fileInput.value = '';
            previewSection.style.display = 'none';
            uploadZone.style.display = 'block';
        });

        // Format file size
        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
        }

        // Form submission
        form.addEventListener('submit', function(e) {
            // Show progress indicator
            progressIndicator.style.display = 'block';
            
            // Disable submit button
            const submitBtn = form.querySelector('.submit-button');
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.6';
            
            // For Django, form will submit normally
            // If you want to use AJAX, prevent default here
        });

        // Input validation styling
        const requiredInputs = form.querySelectorAll('[required]');
        requiredInputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (!this.value) {
                    this.style.borderColor = '#ff6b6b';
                } else {
                    this.style.borderColor = 'rgba(255, 255, 255, 0.15)';
                }
            });

            input.addEventListener('input', function() {
                if (this.value) {
                    this.style.borderColor = '#4ade80';
                }
            });
        });

        // Show welcome notification
        setTimeout(() => {
            showNotification('✨ Fill in the details to add a new CR profile!', 'info');
        }, 500);