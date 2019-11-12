// Main function
$(function() {
  // Set the language of the application (from redis)
  setLanguage();
  // Component definitions available in components.js
  enableComponents(getComponentConfig());
  // Set background (from redis)
  setBackground();

  // The element with main content. This is where views are inserted.
  $main = $("div#main");
  // Do different things depending on the "view" URL parameter.
  // Each view has its own function.
  var view_type = getUrlParameter("view");
  switch(view_type) {
    case "question_yn":
      view_question_yn($main);
      break;
    case "question_rate":
      view_question_rate($main);
      break;
    case "text":
      view_text($main);
      break;
    case "caption":
      view_caption($main);
      break;
    case "overlay":
      view_overlay($main);
      break;
    case "input_name":
      view_input_name($main);
      break;
    case "input_date":
      view_input_date($main);
      break;
    case "input_numbers":
      view_input_numbers($main);
      break;
    case "input_text":
      view_input_text($main);
      break;
    case "input_multiple":
      view_input_multiple($main);
      break;
    case "stream":
      view_stream($main);
      break;
  }

  // Repeatedly check if the robot is listening to change the listening icon
  setTimeout(robotIsListening, repeatedRequestIntervalMsec);
})

// Sends XHR to redis to check if robot is listening
function robotIsListening() {
  getFromChannel(
    "action_audio",
    // If the listening state changed, switch the symbol as required
    function whenHasMessage(request) {
      var msg = JSON.parse(request.response).message;
      if (msg === "start listening") {
        $("#not-listening").hide();
        $("#listening").show();
      } else {
        $("#not-listening").show();
        $("#listening").hide();
      }
      setTimeout(robotIsListening, repeatedRequestIntervalMsec);
    },
    // If there's no content, check again after some time.
    // If there's an error, oops.
    function whenNoResponse(request) {
      if (request.status === STATUS_NOCONTENT)
        setTimeout(robotIsListening, repeatedRequestIntervalMsec);
      else
        console.log("Something went wrong in robotIsListening, request status ", request.status);
    }
  )
}

// Set the language of the page to the value in the 'lang' parameter
var lang;
function setLanguage() {
  lang = getUrlParameter("lang");
  if (!lang)
    lang = "en-US";
}

// Checks if there's a component config in the parameters ('components').
// If yes, returns it in JSON format.
// Else, returns an empty list.
function getComponentConfig() {
  var config = getUrlParameter("components");
  if (config)
    return JSON.parse(config);
  else {
    return [];
  }
}
// Places a component at the top or at the bottom of the screen.
// This appends to the hard-coded #top and #bottom divs in index.html.
function positionComponent($component, position) {
  switch (position) {
    case "top":
      $("div#top").append($component);
      break;
    case "bottom":
      $("div#bottom").append($component);
      break;
    default:
      break;
  }
}
// Runs the build function of all components.
// 'components' is a list of objects.
// Build functions are defined in components.js.
function enableComponents(components) {
  for (var i in components) {
    buildFunction = window[components[i].build];
    if (typeof buildFunction === "function")
      positionComponent(buildFunction(components[i].args), components[i].position);
  }
}

// Set the background of the page to the value in the 'background' parameter
function setBackground() {
  var bg = getUrlParameter("bg");
  if (!bg || bg === "")
    $("body").css("background", "");
  else if (!bg.startsWith("http"))
    $("body").css("background", `url("${baseUri}/img/${bg}") no-repeat left top`);
  else
    $("body").css("background", `url("${bg}") no-repeat left top`);
}

// Clear the page by emptying the body
function clearPage() { $("body").html(""); };
