var mongoose = require('mongoose');
var Schema = mongoose.Schema;
var passportLocalMongoose = require('passport-local-mongoose');

var Account = new Schema({
    pseudo : String,
    email : String,
    mdp : String,
    playlists : String //TODO
});

Account.plugin(passportLocalMongoose);

module.exports = mongoose.model('Account', Account);
