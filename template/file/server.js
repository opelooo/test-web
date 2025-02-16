const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// Serve static files (e.g., index.html) from the "public" directory
app.use(express.static('public'));

// Endpoint to list folder contents
app.get('/list', (req, res) => {
  const folder = req.query.folder;

  // Security precaution: validate and sanitize "folder" as needed!
  if (!folder) {
    return res.status(400).json({ error: 'Missing folder parameter' });
  }

  // Resolve absolute path and restrict access if needed
  const absPath = path.resolve(folder);

  fs.readdir(absPath, (err, files) => {
    if (err) {
      return res.status(500).json({ error: err.toString() });
    }
    res.json({ files });
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
