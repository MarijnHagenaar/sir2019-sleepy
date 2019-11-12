/*
 * Components for the page views:
 * Each component is a function that optionally accepts an args object
 *  and returns a jQuery object.
 * The args object is passed from the tablet_config redis message via main.js.
 * Any required event handlers should be attached inside the function.
 */

// English flag to change language to English
function EnglishFlagComponent() {
  // Create the component
  var $component = $('<img src="img/english_flag.png" id="english-flag" />');

  $component.click(function changeToEnglish() {
    sendToChannel(
      "audio_language",
      "en-US",
      function succeeded() {
        location.reload();
      },
      errorAlert
    )
  });
  return($component);
}

// Button to stop everything on the robot
function SayGoodbyeComponent() {
  var $component = $('<button id="say-goodbye">Say Goodbye</button>');
  $component.click(function() {
    sendToChannel(
      "tablet_answer",
      "stop",
      function succeeded() { $("body").html("") },
      function failed() { alert("Could not stop conversation, request failed.") }
    )
  });
  return($component);
}

// Show a custom logo similarly to the VU logo
function CompanyLogoComponent(args) {
  var $component = $('<img id="company-logo" class="logo">');

  // Set the URL of the image to the URL passed in the redis message
  $component.attr('src', args.image);
  return($component);
}

// Show the result of the speech-to-text system
function SpeechDisplayComponent(args) {
  const waitTime = 500; // milliseconds
  var $component = $('<div id="speech-display"></div>');

  // This function calls itself on a delay, so only need to call once
  speechDisplayLoop();

  return($component);

  function speechDisplayLoop() {
    getFromChannel(
      "text_speech",
      function whenHasMessage(request) {
        $component.html(JSON.parse(request.response).message);
        setTimeout(speechDisplayLoop, waitTime);
      },
      function whenNoResponse(request) {
        setTimeout(speechDisplayLoop, waitTime);
      }
    );
  }
}

// Allow the user to skip a specific question
function SkipQuestionComponent(args) {
  // Create the button
  var $component = $('<button id="skip-question"></button>');

  // Set the text depending on the language
  if (lang === "nl-NL") {
    $component.html("SLA OVER");
  } else {
    $component.html("SKIP");
  }  

  // On click, send an empty string to tablet_answer (signifying that the question was skipped)
  //   and clear the screen.
  $component.click(function skipQuestion() {
    sendToChannel(
      "tablet_answer",
      "",
      function succeeded() { $("body").html("") },
      function failed() { alert("Could not skip question.") }
    )
  });

  return $component;
}
