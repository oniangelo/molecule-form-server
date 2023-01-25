const express = require('express');
const path = require('path');
var cors = require('cors');
const { stdout, stderr } = require('process');
const { threadId } = require('worker_threads');
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

    const { execFile } = require('child_process');
    var molecule = req.body;
    const script  = execFile('python3', ['-u','/home/gambacorta/Scrivania/Nico/progetto/Novembre_2022/predizione.py',
  'models_sequence',molecule.molecule.toString(),'arg2'],(error,stdout,stderr)=> {
    if (error) {
      console.error(`error: ${error}`);
    }
      //put your outuput logic here
    });
  });


  app.listen(port, () => console.log(`Nico app listening on port ${port}!`))});
