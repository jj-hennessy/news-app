async function setValueOfCheckbox(url) {
  // LEFT OFF HERE TRYING TO FIGURE OUT HOW TO CHANGE THE VALUE OF A TARGET INPUT BOX RATHER THAN HAVING IT JUST SELECT THE FIRST ONE IT FINDS
  var currentValue = document.getElementById("news-source").value
  var newValue = null
  if(currentValue == "on") {
    newValue = "off"
  }
  else {
    newValue = "on"
  }
  document.getElementById("news-source").value = newValue
}

async function getValueOfInputs() {
  var currentValues = document.getElementsByClassName("news-source")
  var onOrOff = []
  var urls = []
  for(var i=0; i<currentValues.length; i++) {
    onOrOff.push(currentValues[i].value)
    urls.push(currentValues[i].getAttribute("data-url"))
  }
  var inputValues = [urls, onOrOff]
  console.log(inputValues)
  return inputValues
}

async function getArticlesFromPage() {
  let [urls, onOrOff] = await getValueOfInputs();

  urlsToScrape = []
  for(var i=0; i<urls.length; i++) {
    if(onOrOff[i] == "on") {
      urlsToScrape.push(urls[i])
    }
  }

  let finalHTML = await eel.generateHTML(urlsToScrape)();

  document.getElementById("article-container").innerHTML += finalHTML

  // element.innerHTML += "additional HTML code"
}


async function printResults(n) {
  console.log("Results: ".concat(n));
}

async function getNumOfLinks() {
  document.getElementById("progressReporter").innerHTML = "Calculating number of links..."

  var enteredURL = document.getElementById("urlInput").value;

  let numberOfLinks = await eel.getNumLinks(enteredURL)();
  window.alert(numberOfLinks);

  document.getElementById("progressReporter").innerHTML = "";

}
