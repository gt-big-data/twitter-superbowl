var redis = require("redis"),
    client = redis.createClient();
client.select(1);


var express = require("express");
var app = express();

app.use(express.bodyParser());
app.use(express.methodOverride());
app.use("/", express.static(__dirname + "/public"));
app.use(app.router);

app.get("/data", function(req, res) {
  var phrase = req.query.phrase;
  var from = req.query.from || 0;


  client.multi()
    .get("track:" + phrase + ":period")
    .get("track:" + phrase + ":start")
    .lrange("track:"+ phrase + ":end", from, -1)
    .exec(function(err, replies) {
        if(err) throw err;
        console.log(replies[2].length);
        res.send({
          phrase: phrase,
          period: replies[0],
          start: replies[1],
          freqStart: from,
          frequencies: replies[2]
        });
    });
});

app.listen(3000);
console.log("Listening on 3000");
