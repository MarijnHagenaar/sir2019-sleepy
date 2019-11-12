/* Various utility scripts
 */

// Constants to avoid magic numbers
const STATUS_OK = 200;
const STATUS_CREATED = 201;
const STATUS_NOCONTENT = 204;
const baseUri = "http://"+CONFIG.server+":8000"
const repeatedRequestIntervalMsec = 500;

// Get a message from a Redis channel.
// channel is a string, on_success is a function, on_else is a function.
// Passed functions can be named or anonymous, but named is recommended for readability.
function getFromChannel(channel, on_success, on_else) {
  var request = new XMLHttpRequest();
  var addr = baseUri+"/"+channel;
  request.open("GET", addr);
  request.onreadystatechange = function() {
    if (request.readyState === XMLHttpRequest.DONE) {
      if (request.status === STATUS_OK)
        on_success(request);
      else
        on_else(request);
    }
  }
  request.send();
}

// Send a message to a Redis channel.
// channel is a string, data is a string, on_success is a function, on_else is a function.
function sendToChannel(channel, data, on_success, on_else) {
  var request = new XMLHttpRequest();
  var addr = baseUri+"/"+channel;
  request.open("POST", addr, false);
  request.setRequestHeader("Content-Type", "application/json");
  request.onreadystatechange = function() {
    if (request.readyState === XMLHttpRequest.DONE) {
      if (request.status === STATUS_OK || request.status === STATUS_CREATED)
        on_success(request);
      else
        on_else(request);
    }
  }
  request.send(JSON.stringify({"message": data}));
}

// Get the value of a URL parameter
function getUrlParameter(param) {
  var pageURL = window.location.search.substring(1),
    urlVariables = pageURL.split('&'),
    parameterName, i;
  for (i = 0; i < urlVariables.length; i++) {
    parameterName = urlVariables[i].split('=');
    if (parameterName[0] === param) {
      return parameterName[1] === undefined ? true : decodeURIComponent(parameterName[1]);
    }
  }
};

// Alert to tell the user that I messed up
function errorAlert() {
  alert("Something went wrong with the HTTP request.");
}
