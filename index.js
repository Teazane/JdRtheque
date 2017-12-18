const express = require('express'),
  app = express(),
  http = require('http'),
  bodyParser = require("body-parser"),
  server = http.createServer(app),
  _ = require('lodash');

//Define the resources repository. Call "next()" instead of 404 error when file is not found.
app.use(express.static(__dirname + "/static"));
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.use(bodyParser.json());
//The "extended" syntax allows for rich objects and arrays to be encoded into the URL-encoded format, allowing for a JSON-like experience with URL-encoded.
app.use(bodyParser.urlencoded({ extended: true })); //Use qs library (true)

// use res.render to load up an ejs view file

// index page
app.get('/', function(req, res) {
    res.render('pages/index');
});

/* --------------------- Lance le serveur --------------------- */

let serverPort = process.env.PORT || 5000; //Récupère la variable d'env. PORT ou 5000
app.set("port", serverPort); //Mise en place du port d'écoute
app.listen(serverPort, function() { //Lancement du serveur
  console.log(`Votre appli' est opérationnelle au port ${serverPort} \n`);
});
