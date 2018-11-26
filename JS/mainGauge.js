var g1;

initial_value = 20;
document.addEventListener("DOMContentLoaded", function (event) {
    g1 = new JustGage({
        id: "gauge",
        title: "Nivel de Riesgo",
        value: initial_value,
        min: 0,
        max: 100,
        gaugeWidthScale: 1,
        pointer: true,
        customSectors: {
            percents: false,
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
        counter: false,
        titleFontColor: "white",
        titleFontFamily: "sans serif",
        titlePosition: "above",
        valueFontColor: "white",
        valueFontFamily: "sans serif"
    });
    setInterval(function () {
        g1.refresh(getRandomInt(0, 100));
    }, 2500);
});
