$.extend($.ui.slider.prototype.options, {
  animate: 300
});


$("#flat-slider-mood")
  .slider({
    max: 10,
    min: 0,
    range: "min",
    value: 10
  }).on("slidechange slide", function (e, ui) {
    $("#num-mood").text(ui.value);
  });

$("#flat-slider-energy")
  .slider({
    max: 10,
    min: 0,
    range: "min",
    value: 5
  }).on("slidechange slide", function (e, ui) {
    $("#num-energy").text(ui.value);
  });

$("#flat-slider-preference")
  .slider({
    max: 10,
    min: 0,
    range: "min",
    value: 2
  }).on("slidechange slide", function (e, ui) {
    $("#num-preference").text(ui.value);
  });

$("#flat-slider-mood, #flat-slider-energy, #flat-slider-preference")
  .slider("pips", {
    first: "pip",
    last: "pip"
  })