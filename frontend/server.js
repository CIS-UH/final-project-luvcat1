 var express = require('express');
 var path = require('path');
 var routes = require('./routes/index');

 // Create a new Express application.
 var app = express();
 
 // Configure view engine to render EJS templates.
 app.set('views', path.join(__dirname, '/views'));
 app.set('view engine', 'ejs');
 
 // Use application-level middleware for common functionality, including logging, parsing, and session handling.
 app.use(express.urlencoded({ extended: true}));
 app.use(express.json());
 
 app.use('/', routes);

 app.listen(3000, () => {
    console.log("Running on port 3000");
 });