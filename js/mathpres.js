function mathPres() {
  self = this;
  $(".frame").hide();
  $("#frame-0").show();
  self.numframes = $(".frame").length;
  self.frame = 0
  $("#right").on('click', function () {
    $("#frame-" + self.frame).hide();
    self.frame = (self.frame + 1) % self.numframes;
    $("#frame-" + self.frame).fadeIn();
  });
  $("#left").on('click', function () {
    $("#frame-" + self.frame).hide();
    if (0 == self.frame) {
      self.frame = self.numframes - 1;
    } else {
      self.frame = (self.frame - 1) % self.numframes;
    }
    $("#frame-" + self.frame).fadeIn();
  });
}
