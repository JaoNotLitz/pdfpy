const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const { exec } = require('child_process');

const app = express();
const PORT = 3000;

app.use(bodyParser.json());
app.use(express.static('public')); // Serve static files from the 'public' directory

app.post('/save', (req, res) => {
    const inputData = req.body;

    fs.writeFile('data.json', JSON.stringify(inputData, null, 4), (err) => {
        if (err) {
            res.status(500).send('Error writing to file');
        } else {
            // Execute the Python script
            exec('python3 pdf.py', (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error executing script: ${error}`);
                    res.status(500).send('Error executing script');
                    return;
                }
                if (stderr) {
                    console.error(`Script error output: ${stderr}`);
                    res.status(500).send('Script error');
                    return;
                }
                console.log(`Script output: ${stdout}`);
                res.send('File saved and script executed successfully');
            });
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
