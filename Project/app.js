const express = require("express");
const Server = express();
// GET , POST , DELETE, PUT

Server.get("/", (req,res)=>{
    res.sendFile(__dirname + "/index.html");
});

Server.get("/about", (req,res)=>{
    res.sendFile(__dirname + "/about.html");
});

Server.listen(3300, (err) =>{
    if(err) return console.log(err);
    console.log("The Server is Listening on Port 3300");
})