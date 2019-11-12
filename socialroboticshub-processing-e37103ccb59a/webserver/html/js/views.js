/* Views
 * These are inserted into the HTML page in main.js.
 * They are selected and configured using URL parameters.
 * e.g. /index.html?view=text&text=Hello
 */

// Image with caption
// URL parameters:
// * image_src: URL of the image
// * caption: the text to show under the image
function view_caption($container) {
  $container.append (
    Sqrl.Render(TEMPLATE["en-US"].caption, {
      image_src: getUrlParameter("image_src"),
      caption: getUrlParameter("caption")
    })
  );
}

// Image with overlay
// URL parameters:
// * image_src: URL of the main image
// * overlay_src: URL of the overlay umage
function view_overlay($container) {
  $container.append (
    Sqrl.Render(TEMPLATE["en-US"].overlay, {
      image_src: getUrlParameter("image_src"),
      overlay_src: getUrlParameter("overlay_src")
    })
  );
}

// User input for n digits
// URL parameters:
// * digits: the number of digits to ask for and enforce
// * q: the question to display to the user
function view_input_numbers($container) {
  var digits = getUrlParameter("digits")
  var template;
  if (digits == 2) {
    template = Sqrl.Render(TEMPLATE["en-US"].input_numbers_2, {
      question: getUrlParameter("q")
    })
  } else if (digits == 4) {
    template = Sqrl.Render(TEMPLATE["en-US"].input_numbers_4, {
      question: getUrlParameter("q")
    })
  }
  $container.append(template);

  // Hide text whenever the input field is selected, because
  //  otherwise the input field would end up under the keyboard on Pepper.
  $("input#text-input").focus(function() {
    $("h1").hide()
    $(".input-btns").hide()
	sendToChannel("tablet_focus", "", function() {}, function() {});
  });
  $("input#text-input").blur(function() {
    $("h1").show()
    $(".input-btns").show()
  });

  // Send whatever's entered to redis
  $("form").submit(function(e) {
    e.preventDefault();

    sendToChannel(
      "tablet_answer",
      $("input").val(),
      clearPage,
      errorAlert
    );
  });
}

// User input for a date
// URL parameters:
// * q: the question to display to the user
function view_input_date($container) {
  $container.append (
    Sqrl.Render(TEMPLATE["en-US"].input_date, {
      question: getUrlParameter("q")
    })
  );

  // Hide text whenever the input field is selected, because
  //  otherwise the input field would end up under the keyboard on Pepper.
  $("input#text-input").focus(function() {
    $("h1").hide()
    $(".input-btns").hide()
	sendToChannel("tablet_focus", "", function() {}, function() {});
  });
  $("input#text-input").blur(function() {
    $("h1").show()
    $(".input-btns").show()
  });

  // Send whatever's entered to redis
  $("form").submit(function(e) {
    e.preventDefault();

    sendToChannel(
      "tablet_answer",
      $("input").val(),
      clearPage,
      errorAlert
    );
  });
}


// Rating on a scale
// URL parameters:
// * scale: the number of options to display
// * q: the question to display to the user
function view_question_rate($container) {
  var scale = getUrlParameter("scale");
  var template;
  if (scale == 7) {
    template = Sqrl.Render(TEMPLATE["en-US"].question_rate_7, {
      question: getUrlParameter("q")
    })
  } else if (scale == 5) {
    template = Sqrl.Render(TEMPLATE["en-US"].question_rate_5, {
      question: getUrlParameter("q")
    })
  } else {
    template = Sqrl.Render(TEMPLATE["en-US"].question_rate_10, {
      question: getUrlParameter("q")
    })
  }

  $container.append(template);

  // Send the selected option to redis
  $(".feedback-btn, .feedback-btn-smaller, .multiple-choice-btn").click(function(e) {
    sendToChannel(
      "tablet_answer",
      $(e.target).attr("title"),
      clearPage,
      errorAlert
    );
  });
}

// Ask the user a yes/no question
// URL parameters:
// * q: the question to display to the user
function view_question_yn($container) {
  // For yes/no in English and ja/nee in Dutch, the right template has to be selected.
  $container.append (
    Sqrl.Render(TEMPLATE[lang].question_yn, {
      question: getUrlParameter("q")
    })
  );

  // Send the user's response to redis
  $("button.yn").click(function(e) {
    sendToChannel(
      "tablet_answer",
      'answer_'+$(e.target).attr('id'),
      clearPage,
      errorAlert
    )
  });
}

// Display a message to the user
// URL parameters:
// * text: the text to display
function view_text($container) {
  $container.append (
    Sqrl.Render(TEMPLATE["en-US"].text, {
      text: getUrlParameter("text")
    })
  );
}

// Ask the user if the name the speech-to-text system detected is correct, and
//  ask them to correct the name if it's not.
// URL parameters:
// * name: the name that was heard by Pepper
function view_input_name($container) {
  $container.append (
    Sqrl.Render(TEMPLATE["en-US"].input_name, {
      heard: getUrlParameter("name")
    })
  );

  // If the user enters a correction, send it to redis
  $("form").submit(function(e) {
    e.preventDefault();

    sendToChannel(
      "tablet_answer",
      $("input").val(),
      $container.html("<p>Correction saved.</p>"),
      errorAlert
    );
  });

  // If the user confirms the heard name, send it to redis
  $("button#name-correct").click(function(e) {
    sendToChannel(
      "tablet_answer",
      getUrlParameter("name"),
      clearPage,
      errorAlert
    );
  });

  // Hide text whenever the input field is selected, because
  //  otherwise the input field would end up under the keyboard on Pepper.
  $("input#name-input").focus(function() {
    $("h1").hide()
    $("button#name-correct").hide()
	sendToChannel("tablet_focus", "", function() {}, function() {});
  });
  $("input#name-input").blur(function() {
    $("h1").show()
    $("button#name-correct").show()
  });
}

// Ask the user to input some text
// URL parameters:
// * q: the question to display to the user
function view_input_text($container) {
  $container.append (
    Sqrl.Render(TEMPLATE["en-US"].input_text, {
      question: getUrlParameter("q")
    })
  );

  // Hide text whenever the input field is selected, because
  //  otherwise the input field would end up under the keyboard on Pepper.
  $("input#text-input").focus(function() {
    $("h1").hide()
    $(".input-btns").hide()
	sendToChannel("tablet_focus", "", function() {}, function() {});
  });
  $("input#text-input").blur(function() {
    $("h1").show()
    $(".input-btns").show()
  });

  // Send the user's input to redis
  $("form").submit(function(e) {
    e.preventDefault();

    sendToChannel(
      "tablet_answer",
      $("input").val(),
      clearPage,
      errorAlert
    );
  });
}

// Ask the user to select from a few choices
// URL parameters:
// * q: the question to display to the user
// * n: the number of options
// * options: semicolon-separated multiple choice options
function view_input_multiple($container) {
  $container.append (
    Sqrl.Render(TEMPLATE["en-US"].input_multiple, {
      question: getUrlParameter("q")
    })
  );

  var n_options = getUrlParameter("n");
  var options = getUrlParameter("options").split(";");

  // Each option is a button
  for (i = 0; i < n_options; i++) {
    var button = `<button id="${i}" class="multiple-choice-btn">${options[i]}</button>`;
    $("#answer-options").append(button);
  }

  // Send the clicked button to redis
  $("button.multiple-choice-btn").click(function(e) {
    sendToChannel(
      "tablet_answer",
      $(e.target).text(),
      clearPage,
      errorAlert
    );
  });
}

function view_stream($container) {
  $container.append (
    Sqrl.Render(TEMPLATE["en-US"].stream, {
		url: "http://"+CONFIG.server+":8001"
	})
  );
}
