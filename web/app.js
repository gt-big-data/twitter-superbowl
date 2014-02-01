var redis = require("redis"),
    client = redis.createClient();
client.select(1, function() {
    client.get("track:peyton&manning:period", function(err, reply) {
        console.log(reply); 
    });
});


var express = require("express");
var app = express();

app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(app.router);

app.get("/", function(req, res) {
  client.multi()
    .get("track:peyton&manning:period")
    .get("track:peyton&manning:start")
    .lrange("track:peyton&manning:end", 0, -1)
    .exec(function(err, replies) {
        if(err) throw err;
        res.send({
          period: replies[0],
          start: replies[1],
          frequencies: replies[2]
        });
    });
});

app.listen(3000);
console.log("Listening on 3000");
