const express = require('express');
const path = require('path');
var cors = require('cors');
const { stdout, stderr } = require('process');
const { threadId } = require('worker_threads');
//const port = process.env.PORT || 3000;

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.raw());
app.use(express.static('jsme'));
app.use('/pred_out', express.static('pred_out'));


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

    const { execFile, spawn } = require('child_process');
    var molecule = req.body.molecule.toString();
    const script  = execFile('/home/gambacorta/anaconda3/envs/ML/bin/python3', ['/home/gambacorta/Scrivania/Nico/website/molecule-form-server/run.py',molecule ],(error,stdout,stderr)=> {
    if (error) {
      console.error(`error: ${error}`);
      //res.set(500, {'Content-type': 'text/html'});
      //res.end(`execFile error : ${error}`);
    }
    const html =`<pre>${stdout}</pre>`
    res.setHeader('Content-type', 'text/html');
    res.send(html);
  //res.sendFile(path.join(__dirname + '/basic-template.html'));
  })
});

app.get('/go-to-result',(req,res) => {
  const { execFile, spawn } = require('child_process');
  var molecule = req.query.molecule;
  const script  = execFile('/home/gambacorta/anaconda3/envs/ML/bin/python3', ['/home/gambacorta/Scrivania/Nico/website/molecule-form-server/run.py',molecule ],(error,stdout,stderr)=> {
    if (error) {
      console.error(`error: ${error}`);
      //res.set(500, {'Content-type': 'text/html'});
      //res.end(`execFile error : ${error}`);
    }
    const html =`${stdout}`;
    res.setHeader('Content-type', 'text/html');
    res.send(html);
    // res.setHeader('Content-type', 'text/html');
    // res.send(html);
  //res.sendFile(path.join(__dirname + '/basic-template.html'));
  })
});




const port = 3000;
app.listen(port, () => console.log(`Nico app listening on port ${port}!`));
