//index.js
/* --------------------- Déclaration des imports et paramétrage général --------------------- */

const express = require('express'),
  http = require('http'),
  app = express(),
  server = http.createServer(app),
  expressSession = require('express-session'),
  bodyParser = require("body-parser"),
  _ = require('lodash'),
  mongoose = require('mongoose'),
  passport = require('passport'),
  assert = require('assert');

//Define the resources repository. Call "next()" instead of 404 error when file is not found.
app.use(express.static(__dirname + "/static"));
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.use(bodyParser.json());
//The "extended" syntax allows for rich objects and arrays to be encoded into the URL-encoded format, allowing for a JSON-like experience with URL-encoded.
app.use(bodyParser.urlencoded({ extended: true })); //Use qs library (true)
app.use(expressSession({secret: 'mySecretKey'})); //TODO : voir pour le paramétrage de ce truc
app.use(passport.initialize());
app.use(passport.session());

/* --------------------- Gestion de la BDD --------------------- */

var AccountModel = require('bdd_modeles');
passport.use(new LocalStrategy(AccountModel.authenticate()));
passport.serializeUser(AccountModel.serializeUser());
passport.deserializeUser(AccountModel.deserializeUser());

mongoose.connect('mongodb://localhost/jdrthequeDB', function(err) {
  if (err) { throw err; }
});

//mongoose.connection.close(); //TODO : voir où placer les connexions et déconnexions


/* --------------------- Gestion des pages --------------------- */

//page d'accueil
app.get('/', function(req, res) {
    res.render('pages/index', {user : req.user}); //check si connecté
}); // use res.render to load up an ejs view file + parameters

//page d'enregistrement
app.get('/register', function(req, res) {
    res.render('pages/register', {user : req.user});
});

app.post('register', function(req, res) {
    AccountModel.register(new Account({ username : req.body.username }), req.body.password, function(err, account) {
       if (err) { return res.render('register', { account : account }); }
       passport.authenticate('local')(req, res, function () {
           res.redirect('/');
       });
   });
});

//page de login
app.get('/login', function(req, res) {
    res.render('pages/login', {user : req.user});
});

app.post('/login', passport.authenticate('local'), function(req, res) {
    res.redirect('/');
});

//logout
app.get('/logout', function(req, res) {
    req.logout();
    res.redirect('/');
})


/* --------------------- Lance le serveur --------------------- */

let serverPort = process.env.PORT || 5000; //Récupère la variable d'env. PORT ou 5000
app.set("port", serverPort); //Mise en place du port d'écoute
app.listen(serverPort, function() { //Lancement du serveur
  console.log(`Votre appli' est opérationnelle au port ${serverPort} \n`);
});


/* --------------------- Sources et tuto utilisés --------------------- */
//Gestion utilisateur via Passport et lien avec MongoDB
//http://mherman.org/blog/2015/01/31/local-authentication-with-passport-and-express-4/#.VbkHSfYvBhE
//https://code.tutsplus.com/tutorials/authenticating-nodejs-applications-with-passport--cms-21619

//MongoDB démarrage sur Windows
//https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
//Mongoose
//http://atinux.developpez.com/tutoriels/javascript/mongodb-nodejs-mongoose/
