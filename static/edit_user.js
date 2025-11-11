 function switchTab(index, btn) {
            const tabs = document.querySelectorAll('.tab-content');
            const btns = document.querySelectorAll('.tab-btn');
            const titles = ['✏️ Edit Profile', '⚙️ Settings'];

            tabs.forEach(tab => tab.classList.remove('active'));
            btns.forEach(b => b.classList.remove('active'));

            tabs[index].classList.add('active');
            btn.classList.add('active');
            document.getElementById('pageTitle').textContent = titles[index];
        }

        // function toggleSwitch(btn) {
        //     btn.classList.toggle('deactive');
        // }

        // Photo upload preview
        // document.getElementById('photoInput').addEventListener('change', function(e) {
        //     const file = e.target.files[0];
        //     if (file) {
        //         const reader = new FileReader();
        //         reader.onload = function(event) {
        //             const photoDiv = document.querySelector('.profile-photo_edit');
        //             photoDiv.innerHTML = `<img src="${event.target.result}" style="width:100%; height:100%; object-fit:cover; border-radius:50%;">`;
        //         };
        //         reader.readAsDataURL(file);
        //     }
        // });