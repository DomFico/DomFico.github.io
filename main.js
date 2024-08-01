function toggleFiles(fileId) {
    const filesDiv = document.getElementById(fileId);
    if (filesDiv.style.display === 'none' || filesDiv.style.display === '') {
        filesDiv.style.display = 'block';
    } else {
        filesDiv.style.display = 'none';
    }
}

// Function to fetch and display files
function fetchAndDisplayFiles() {
    fetchFiles('Coding Projects', 'coding-projects-list');
    fetchFiles('Research', 'research-list');
}

// Function called by the refresh button
document.getElementById('refresh-button').addEventListener('click', fetchAndDisplayFiles);

// Initial setup to hide the files
document.addEventListener('DOMContentLoaded', (event) => {
    const fileDivs = document.querySelectorAll('.files');
    fileDivs.forEach(fileDiv => {
        fileDiv.style.display = 'none';
    });
});

// Fetch files from a specified directory
function fetchFiles(folder, outputElementId) {
    fetch(`/${folder}`)
        .then(response => response.json())
        .then(data => {
            console.log(`Fetched files from ${folder}:`, data); // Log the output
            const outputElement = document.getElementById(outputElementId);
            // Clear the current file list
            outputElement.innerHTML = '';
            // Populate with new file list
            data.forEach(file => {
                const fileLink = document.createElement('div');
                fileLink.innerHTML = `<a href="${folder}/${file}">${file}</a>`;
                outputElement.appendChild(fileLink);
            });
        })
        .catch(error => console.error('Error fetching files:', error));
}