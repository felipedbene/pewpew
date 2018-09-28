window.onerror =  function(msg) {
$('#attackdiv').html('<h1 style="color:red;font-size:1em">'+msg+'</h1>')
setTimeout(function(){location.reload();} ,3000);
}
var log = [];
var time = 1;
var debug = true;
var queue = 50;
var count = 0;
var timer = function(name) {
    var start = new Date();
    return {
        stop: function() {
            var end  = new Date();
            var time = end.getTime() - start.getTime();
            //~ console.log('Timer:', name, 'finished in', time, 'ms');
            $('#attackdiv').append('Timer:'+ name+ ' finished in '+ time+ 'ms<br/>');
        }
    }
};
$.extend({
	getUrlVars: function(){
		var vars = [], hash;
		var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
		for(var i = 0; i < hashes.length; i++)
		{
			hash = hashes[i].split('=');
			vars.push(hash[0]);
			vars[hash[0]] = hash[1];
		}
		return vars;
	},
	getUrlVar: function(name){
		return $.getUrlVars()[name];
	}
});
function FixedQueue( size, initialValues ){
	initialValues = (initialValues || []);
	var queue = Array.apply( null, initialValues );
	queue.fixedSize = size;
	queue.push = FixedQueue.push;
	queue.splice = FixedQueue.splice;
	queue.unshift = FixedQueue.unshift;
	FixedQueue.trimTail.call( queue );
	return( queue );
}
FixedQueue.trimHead = function(){
	if (this.length <= this.fixedSize){ return; }
	Array.prototype.splice.call( this, 0, (this.length - this.fixedSize) );
};
FixedQueue.trimTail = function(){
	if (this.length <= this.fixedSize) { return; }
	Array.prototype.splice.call( this, this.fixedSize, (this.length - this.fixedSize)
	);
};
FixedQueue.wrapMethod = function( methodName, trimMethod ){
	var wrapper = function(){
		var method = Array.prototype[ methodName ];
		var result = method.apply( this, arguments );
		trimMethod.call( this );
		return( result );
	};
	return( wrapper );
};

FixedQueue.push = FixedQueue.wrapMethod( "push", FixedQueue.trimHead );
FixedQueue.splice = FixedQueue.wrapMethod( "splice", FixedQueue.trimTail );
FixedQueue.unshift = FixedQueue.wrapMethod( "unshift", FixedQueue.trimTail );

var map = new Datamap({

		scope: 'world',
		element: document.getElementById('container1'),
		projection: 'mercator',
		// change the projection to something else only if you have absolutely no cartographic sense

		fills: { defaultFill: 'black', },

		geographyConfig: {
			dataUrl: null,
			hideAntarctica: true,
			borderWidth: 0.75,
			borderColor: '#4393c3',
			popupTemplate: function(geography, data) {
				return '<div class="hoverinfo" style="color:white;background:black">' +
							 geography.properties.name + '</div>';
			},
			popupOnHover: true,
			highlightOnHover: false,
			highlightFillColor: 'black',
			highlightBorderColor: 'rgba(250, 15, 160, 0.2)',
			highlightBorderWidth: 2
		},
})
var hits = FixedQueue( queue, [  ] );
var boom = FixedQueue( queue, [  ] );

var log;
$.getJSON("XML/LastHour.json", function(json) {
  log = json;
});


function getData(a){
  if(debug){
    var t = timer("Loop "+count);
  }
   $('#container2').html('<h1>'+a['time_generated']+'</h1>');
   var IP1 = a["src"];
   var IP2 = a["dst"];
   var srccountry = a["srcname"];
   var attackdiv_slatlong = a["dstname"];
   var srclat = a["srclat"];
   var srclong = a["srclong"];
   var dstlat = a["dstlat"];
   var dstlong = a["dstlong"];
   var which_attack = a["subtype"];
   var atkname = a["threatid"];
   var strokeColor = a["severity"];

   hits.push( { origin : { latitude: +srclat, longitude: +srclong },
     destination : { latitude: +dstlat, longitude: +dstlong } } );
   map.arc(hits, {strokeWidth: 2, strokeColor: strokeColor});

  // add boom to the bubbles queue

  boom.push( { radius: 7, latitude: +dstlat, longitude: +dstlong,
               fillOpacity: 0.5, attk: which_attack} );
  map.bubbles(boom, {
       popupTemplate: function(geo, data) {
         return '<div class="hoverinfo">' + data.attk + '</div>';
       }
   });
   $('#attackdiv').append("<b>"+srccountry + "</b> (" + IP1 + ") " +
           " <span style='color:#FF7474'>attacks</span><br/> <b>" +
           attackdiv_slatlong+  "</b> (" + IP2 + ") <br>" +
           " <span style='color:"+strokeColor+"'> w/ " + atkname +
           "("+ which_attack + ")</span> " + "<br/>"+ "<br/>");

   $('#attackdiv').animate({scrollTop: $('#attackdiv').prop("scrollHeight")}, time);
}




$.each(log,function(idx,value){
  count = idx;
  getData(value);
});
