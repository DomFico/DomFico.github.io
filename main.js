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
    const fileDivs = document.querySelectorAll('.files');
    fileDivs.forEach(fileDiv => {
        fileDiv.style.display = 'none';
    });
});