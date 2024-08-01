const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(__dirname));

// Endpoint to get files from a directory
app.get('/:folder', (req, res) => {
    const folderPath = path.join(__dirname, req.params.folder);
    fs.readdir(folderPath, (err, files) => {
        if (err) {
            return res.status(500).send('Error reading files');
        }
        res.json(files);
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});