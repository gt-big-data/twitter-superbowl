
function render(tweets, sents, time) {
    $("#main").html('<div class="time">What people "said" <b>' + time + "</b> minutes from the start:</div>");
    for(var i = 0; i < tweets.length; i++) {
        var tweetsHTML = "";
        var words = tweets[i].split(" "); 
        for(var j = 0; j < words.length; j++) {
            var word = words[j];
            var sent = sents[word];
            if(!sent) {sent = 0;}
            var neg = sent < 0;
            sent = Math.min(Math.floor(Math.abs(sent)), 4);
            if(neg) {sent = -sent;}
            tweetsHTML += '<span class="sent-' + sent + '">' + word + '</span> ';
        }
        $("#main").append("<div>" + tweetsHTML + "</div><br>");
    }
}

function ready(periodsData, sentiments) {
    var val = 0;
    var old = null;
    var startDate = new Date("February 2, 2014 18:30:00");
    $("#periodSel").change(function() {
        val = $(this).val();
        clearTimeout(old);
        old = setTimeout(function() {
            console.log("render");
            render(periodsData[val], sentiments, val);
        }, 100);
    });
    render(periodsData[0], sentiments, val);
}

$.ajax("/ridiculous-sentences.json", {success: function(data){
    periodsData = {};
    max = (min = data[0].per);
    for(var i = 0; i < data.length; i++) {
        periodsData[data[i].per] = data[i].tweets;
        if(data[i].per > max) {max = data[i].per;}
        if(data[i].per < min) {min = data[i].per;}
    }
    $.ajax("/sentiments.json", {success: function(data) {ready(periodsData, data);}});
}});

