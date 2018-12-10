const express = require('express');
var app = express();
var upload = require('express-fileupload');
const http = require('http');
http.Server(app).listen(80); // make server listen on port 80

app.use(express.static('public'));
app.use(upload()); // configure middleware

console.log("Server Started at port 80");

app.get('/',function(req,res){
  res.sendFile(__dirname+'/index.html');
})


app.post('/upload',function(req,res){
  console.log(req.files);
  console.log(req.files.file);
  if(req.files.file){
    var file = req.files.file,
      name = file.name,
      type = file.mimetype;
    var uploadpath = __dirname + '/uploads/' + name;


    file.mv(uploadpath,function(err){
      if(err){
        console.log("File Upload Failed",name,err);
        res.send("Error Occured!")
      }
      else {
        console.log("File Uploaded",name);
        res.send('Done! Uploading files')

      }

  });

	} else {
    res.send("No File selected !");
    res.end();
}});


app.get('/status', function(req,res){
		const spawn = require("child_process").spawn;
		const pythonProcess = spawn('python',[__dirname+"1.py"]);
    ret = pythonProcess.stdout.on('data', (data) =>{})
		if(ret){
			res.send("Lie to me said you're a liar!")
	} else {
			res.send("All good, Lie to me said you speak the truth")
	}
});
