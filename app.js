const express = require("express");
const bodyParser = require("body-parser");
const request = require("request");
const axios = require("axios");

const sqlite = require('sqlite3').verbose();
const db = new sqlite.Database("./TuttyFrutty.db", sqlite.OPEN_READWRITE, (err)=>{
    if(err) return console.error(err);
});

var number_order=1;
const sql = "INSERT INTO cart (number_order,id_product,count) VALUES(?,?,?)";

const app= express();

app.use(express.static("public"));
app.use(bodyParser.urlencoded({extended:true}));

app.get("/", function(req,res){
    res.sendFile(__dirname+"/index.html");
});
var number_order=1;
app.use(express.json());
app.post("/", (req, res) => {
    console.log(typeof(req.body[req.body.length-1]));// this would be the data sent with the request
    var add =req.body[req.body.length-1];
    db.run(sql,number_order++,add,1);
    res.send("game started");
});

app.listen(3000,function(){
console.log("server running");
});


