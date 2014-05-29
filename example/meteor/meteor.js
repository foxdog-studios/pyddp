Meteor.methods({
  upper: function (text) {
    check(text, String);
    return text.toUpperCase();
  }
});

