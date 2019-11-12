/* Templates for use by Squirrely.
 * The main object contains two keys, "en-US" and "nl-NL". This can be extended for other
 *  languages. When creating a template, add it to the respective language.
 * Information on how to write a template can be found on Confluence.
 */
var TEMPLATE = {
  "en-US": {
    "question_yn": `
      <h1>{{question}}</h1>
      <button type="button" class="multiple-choice-btn yn" id="yes">YES</button>
      <button id="no" class="multiple-choice-btn yn" type="button">NO</button>
    `,

    "question_rate_5": `
      <h1>{{question}}</h1>
      <img class="feedback-btn" src="img/smiley2.png" title="terrible" />
      <img class="feedback-btn" src="img/smiley3.png" title="bad" />
      <img class="feedback-btn" src="img/smiley4.png" title="neutral" />
      <img class="feedback-btn" src="img/smiley5.png" title="good" />
      <img class="feedback-btn" src="img/smiley6.png" title="great" />
    `,

    "question_rate_7": `
      <h1>{{question}}</h1>
      <img src="img/smiley1.png" title="terrible" class="feedback-btn-smaller" />
      <img src="img/smiley2.png" title="very bad" class="feedback-btn-smaller" />
      <img src="img/smiley3.png" title="bad" class="feedback-btn-smaller" />
      <img src="img/smiley4.png" title="neutral" class="feedback-btn-smaller" />
      <img src="img/smiley5.png" title="good" class="feedback-btn-smaller" />
      <img src="img/smiley6.png" title="very good" class="feedback-btn-smaller" />
      <img src="img/smiley7.png" title="amazing" class="feedback-btn-smaller" />
    `,

    "question_rate_10": `
      <h1>{{question}}</h1>
      <button class="multiple-choice-btn" title="0">0</button>
      <button class="multiple-choice-btn" title="1">1</button>
      <button class="multiple-choice-btn" title="2">2</button>
      <button class="multiple-choice-btn" title="3">3</button>
      <button class="multiple-choice-btn" title="4">4</button>
      <button class="multiple-choice-btn" title="5">5</button>
      <button class="multiple-choice-btn" title="6">6</button>
      <button class="multiple-choice-btn" title="7">7</button>
      <button class="multiple-choice-btn" title="8">8</button>
      <button class="multiple-choice-btn" title="9">9</button>
      <button class="multiple-choice-btn" title="10">10</button>
    `,

    "text": `
      <h1>{{text}}</h1>
    `,

    "caption": `
      <img src="{{image_src}}" />
      <h3>{{caption}}</h3>
    `,

    "overlay": `
      <img src="{{overlay_src}}" border="0" style="max-height: 100vh; background: url({{image_src}}) center center black;" />
    `,

    "input_name": `
      <h1>Is {{heard}} correct?</h1>
      <button id="name-correct" class="input-btns">
        Yes, this is correct.
      </button>
      <p>If not, please correct me using the text box below.</p>
      <form>
      <input type="text" class="text-field" id="name-input" required />
      <br>
      <input type="submit" value="Use my input" class="input-btns" id="name-submit" />
      </form>
    `,

    "input_date": `
      <h1>{{question}}</h1>
      <form>
      <input type="date" class="text-field" id="text-input" required />
      <br>
      <input id="submit-btn" class="input-btns" type="submit" value="OK">
      </form>
    `,

    "input_numbers_2": `
      <h1>{{question}}</h1>
      <form>
        <input id="text-input" class="text-field" type="number" required pattern="[0-9]{2}" title="Please enter a two-digit number" />
        <br>
        <input id="submit-btn" class="input-btns" type="submit" value="OK" />
      </form>
    `,

    "input_numbers_4": `
      <h1>{{question}}</h1>
      <form>
        <input id="text-input" class="text-field" type="number" required pattern="[0-9]{4}" title="Please enter a four-digit number" />
        <br>
        <input id="submit-btn" class="input-btns" type="submit" value="OK" />
      </form>
    `,

    "input_text": `
      <h1>{{question}}</h1>
      <form>
      <input type="text" class="text-field" id="text-input" required />
      <br>
      <input type="submit" value="OK" class="input-btns" id="submit-btn" />
      </form>
    `,
	
    "input_multiple": `
      <h1>{{question}}</h1>
      <div id="answer-options">
      </div>
      `,
	
    "stream": `
      <img id="stream" src="{{url}}">
      `
  },
  "nl-NL": {
    "question_yn": `
      <h1>{{question}}</h1>
      <button type="button" class="multiple-choice-btn yn" id="yes">JA</button>
      <button id="no" class="multiple-choice-btn yn" type="button">NEE</button>
      `
  }
}
