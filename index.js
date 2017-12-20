//index.js
/* --------------------- Déclaration des imports et paramétrage général --------------------- */

const express = require('express'),
  app = express(),
  http = require('http'),
  bodyParser = require("body-parser"),
  server = http.createServer(app),
  _ = require('lodash'),
  MongoClient = require('mongodb').MongoClient,
  assert = require('assert');

//Define the resources repository. Call "next()" instead of 404 error when file is not found.
app.use(express.static(__dirname + "/static"));
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.use(bodyParser.json());
//The "extended" syntax allows for rich objects and arrays to be encoded into the URL-encoded format, allowing for a JSON-like experience with URL-encoded.
app.use(bodyParser.urlencoded({ extended: true })); //Use qs library (true)

/* --------------------- Gestion de la BDD --------------------- */

/*var url = 'mongodb://localhost:27017/myproject';
// Use connect method to connect to the Server
MongoClient.connect(url, function(err, db) {
  assert.equal(null, err);
  console.log("Connexion à la BDD opérationnelle.");
  db.close();
});*/

/* --------------------- Gestion des pages --------------------- */

// index page
app.get('/', function(req, res) {
    res.render('pages/index'); // use res.render to load up an ejs view file
});

/* --------------------- Lance le serveur --------------------- */

let serverPort = process.env.PORT || 5000; //Récupère la variable d'env. PORT ou 5000
app.set("port", serverPort); //Mise en place du port d'écoute
app.listen(serverPort, function() { //Lancement du serveur
  console.log(`Votre appli' est opérationnelle au port ${serverPort} \n`);
});
