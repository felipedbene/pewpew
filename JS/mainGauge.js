var options = {
    id: "gauge",
    value: getRandomInt(0, 100),
    min: 0,
    max: 100,
    title: "SANS"
}

$(document).ready(function () {
    var g = new JustGage(options);
})

var jg1 = new JustGage({
    id: "gauge",
    value: Math.floor(Math.random() * 200),
    min: 0,
    max: 300,
    gaugeWidthScale: 0.6,
    customSectors: {
        percents: true,
        ranges: [
            {
                color: "#00d100",
                lo: 0,
                hi: 25
            }, {
                color: "#798f00",
                lo: 26,
                hi: 50
            }, {
                color: "#834500",
                lo: 51,
                hi: 75
            }, {
                color: "#76001e",
                lo: 76,
                hi: 100
            }
        ]
    },
    counter: true
});
