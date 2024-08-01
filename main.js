function toggleFiles(fileId) {
    const filesDiv = document.getElementById(fileId);
    if (filesDiv.style.display === 'none' || filesDiv.style.display === '') {
        filesDiv.style.display = 'block';
    } else {
        filesDiv.style.display = 'none';
    }
}

// Initial setup to hide the files
document.addEventListener('DOMContentLoaded', (event) => {
    const filesDiv = document.getElementById('root-files');
    filesDiv.style.display = 'none';
});