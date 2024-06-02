// index.js

function previewImage(event) {
    const file = event.target.files[0];
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('preview');

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewContainer.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}