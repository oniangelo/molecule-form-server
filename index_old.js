const express = require('express');
const path = require('path');
var cors = require('cors');
const port = process.env.PORT || 3000;

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.raw());
app.use(express.static('jsme'));



// app.get('/',(req, res) => {
  
//   res.sendFile(path.join(__dirname, '/node_modules/jsme-editor/jsme.nocache.js'));
//   //res.sendFile(path.join(__dirname, '/frontend.html'));
// });

app.get('/',(req, res) => {
    res.sendFile(path.join(__dirname, '/frontend.html'));
    //res.sendFile(path.join(__dirname, '/frontend.html'));
  });

  app.get('/test',(req, res) => {
    res.sendFile(path.join(__dirname, '/frontend_copy.html'));
    //res.sendFile(path.join(__dirname, '/frontend.html'));
  });
  app.post('/analize-data',(req, res) => {

    const { spawn } = require('child_process');
   
    const pyProg = spawn('python3', ['./predizione.py',3,6]);
    var result = 0;
    pyProg.stdout.on('data', (data) => {
        result = data;
        console.log(`stdout: ${data}`);
        var molecule = req.body;
        res.json({risultato :molecule.molecule.toString()});
      });
    
    //res.sendFile(path.join(__dirname, '/frontend.html'));
  });


  app.listen(port, () => console.log(`Nico app listening on port ${port}!`));