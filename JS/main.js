// Versión Rapida
window.onerror = function(msg) {
  // $('#attackdiv').html('<h1 style="color:red;font-size:1em">' + msg + '</h1>')
  console.log(msg);
  setTimeout(function() {
    location.reload();
  }, 3000);
}



function checkTime(i) {
  if (i < 10) {
    i = "0" + i;
  }
  return i;
}

function startTime() {
  var event = new Date();
  var options = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  };
  var horaMexico = event.toLocaleDateString('es-MX', options);
  document.getElementById('container2').innerHTML = horaMexico;
  t = setTimeout(function() {
    startTime()
  }, 500);
}
startTime();


var log = [];
var count = 0;
var time = 500;
var len = 0;
var debug = false;
var queue = 50;
var show_time = true;
var show_console = true;
var estatico = false;

if (!show_console) {
  var tmp = document.getElementById('attackdiv')
  tmp.style.visibility = 'hidden';
}

//~ Timer
var timer = function(name) {
  var start = new Date();
  return {
    stop: function() {
      var end = new Date();
      var time = end.getTime() - start.getTime();
      //~ console.log('Timer:', name, 'finished in', time, 'ms');
      $('#attackdiv').append('Timer:' + name + ' finished in ' + time + 'ms<br/>');
    }
  }
};


$.extend({
  getUrlVars: function() {
    var vars = [],
      hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = hash[1];
    }
    return vars;
  },
  getUrlVar: function(name) {
    return $.getUrlVars()[name];
  }
});

function FixedQueue(size, initialValues) {
  initialValues = (initialValues || []);
  var queue = Array.apply(null, initialValues);
  queue.fixedSize = size;
  queue.push = FixedQueue.push;
  queue.splice = FixedQueue.splice;
  queue.unshift = FixedQueue.unshift;
  FixedQueue.trimTail.call(queue);
  return (queue);
}

FixedQueue.trimHead = function() {
  if (this.length <= this.fixedSize) {
    return;
  }
  Array.prototype.splice.call(this, 0, (this.length - this.fixedSize));
};

FixedQueue.trimTail = function() {
  if (this.length <= this.fixedSize) {
    return;
  }
  Array.prototype.splice.call(this, this.fixedSize, (this.length - this.fixedSize));
};

FixedQueue.wrapMethod = function(methodName, trimMethod) {
  var wrapper = function() {
    var method = Array.prototype[methodName];
    var result = method.apply(this, arguments);
    trimMethod.call(this);
    return (result);
  };
  return (wrapper);
};

FixedQueue.push = FixedQueue.wrapMethod("push", FixedQueue.trimHead);
FixedQueue.splice = FixedQueue.wrapMethod("splice", FixedQueue.trimTail);
FixedQueue.unshift = FixedQueue.wrapMethod("unshift", FixedQueue.trimTail);


// we read in a modified file of all country centers
var centers = [];
d3.tsv("CSV/country_centroids_primary.csv", function(data) {
  centers = data;
});
d3.csv("CSV/samplatlong.csv", function(data) {
  slatlong = data;
});
d3.csv("CSV/cnlatlong.csv", function(data) {
  cnlatlong = data;
});
d3.tsv("CSV/all_countries.csv", function(data) {
  countries = data;
});


// setup structures for the "hits" (arcs)
// and circle booms

var hits = FixedQueue(queue, []);
var boom = FixedQueue(queue, []);

// we need random numbers and also a way to build random ip addresses
function readTextFile(file, callback) {
  var rawFile = new XMLHttpRequest();
  rawFile.overrideMimeType("application/json");
  rawFile.open("GET", file, true);
  rawFile.onreadystatechange = function() {
    if (rawFile.readyState === 4 && rawFile.status == "200") {
      callback(rawFile.responseText);
    } else {
      $('#attackdiv').html('<h1 style="color:red;font-size:1em">No file found</h1>')
      setTimeout(function() {
        location.reload();
      }, 1500000);
    }
  }
  rawFile.onerror = function(msg) {
    $('#attackdiv').html('<h1 style="color:red;font-size:1em">' + msg + '</h1>')
    setTimeout(function() {
      location.reload();
    }, 1500000);
  }
  rawFile.upload.onerror = function(msg) {
    $('#attackdiv').html('<h1 style="color:red;font-size:1em">' + msg + '</h1>')
    setTimeout(function() {
      location.reload();
    }, 1500000);
  }

  rawFile.send(null);
}

// doing this a bit fancy for a hack, but it makes it
// easier to group code functions together and have variables
// out of global scope
var attacks = {
  interval: time,

  init: function() {
    setTimeout(
      jQuery.proxy(this.getData, this),
      this.interval
    );
  },


  //usage:


  test: function() {
    $('#attackdiv').html('')
    $('#attackdiv').append("<h1>Loading...</h1><br/>");

    readTextFile("XML/LastHour.json", function(text) {
      var data = JSON.parse(text);

      log = data
      //console.log(log);
      len = Object.keys(log).length;
      $('#attackdiv').html('');
      attacks.getData();
    });

  },

  getData: function() {
    var self = this;
    if (debug)
      var t = timer("Loop " + count);
    //<Parte Gabo>
    var a = log[count];
    // $('#container2').html('<h1>' + a['time_generated'] + '</h1>');

    var IP1 = "";
    var IP2 = "";

    var srccountry = a["srcname"];
    var attackdiv_slatlong = a["dstname"];
    /*
    		if (typeof b === 'undefined' || b === null)
    		{
    			b = {}
    			for (var i=0; i<countries.length; i++){
    				b[countries[i].name] = countries[i];
    			}
    			countries = b;
    		}
    */
    var srclat = a["srclat"];
    var srclong = a["srclong"];
    var dstlat = a["dstlat"];
    var dstlong = a["dstlong"];

    which_attack = a["subtype"];
    var atkname = a["threatid"];
    strokeColor = a["severity"];

    hits.push({
      origin: {
        latitude: +srclat,
        longitude: +srclong
      },
      destination: {
        latitude: +dstlat,
        longitude: +dstlong
      }
    });
    map.arc(hits, {
      strokeWidth: 3,
      strokeColor: strokeColor
    });

    // add boom to the bubbles queue

    boom.push({
      radius: 7,
      latitude: +dstlat,
      longitude: +dstlong,
      fillOpacity: 0.5,
      attk: which_attack
    });
    map.bubbles(boom, {
      popupTemplate: function(geo, data) {
        return '<div class="hoverinfo">' + data.attk + '</div>';
      }
    });
    if (show_time) {
      tiempo = "@" + a['time_generated'] + '<br>';
    } else {
      tiempo = '';
    }

    $('#attackdiv').append(tiempo + "<b>" + srccountry + "</b> " + IP1 +
      " <span style='color:#FF7474'>attacks</span><br/> <b>" +
      attackdiv_slatlong + "</b> " + IP2 + " <br>" +
      " <span style='color:" + strokeColor + "'> " + atkname +
      "(" + which_attack + ")</span> " + "<br/>" + "<br/>");

    $('#attackdiv').animate({
      scrollTop: $('#attackdiv').prop("scrollHeight")
    }, time);

    // pick a new random time and start the timer again!
    count++;

    if (count < len) {
      if (debug) {
        t.stop();
      }
      if (!estatico) {
        attacks.init();
      }
    } else {
      setTimeout(function() {
        //~ $('#attackdiv').html('Loading')
        count = 0;
        log = [];
        location.reload();
        attacks.test();
      }, time);
      //location.reload();

    }

  },

};

attacks.test();
d3.select(window).on('resize', function() {
  location.reload();
});
