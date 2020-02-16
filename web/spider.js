async function setValueOfCheckbox(index) {
  var currentValue = document.getElementsByClassName("input-field")[index].value
  var newValue = null
  if(currentValue == "on") {
    newValue = "off"
  }
  else {
    newValue = "on"
  }
  document.getElementsByClassName("input-field")[index].value = newValue
}

async function getValueOfInputs() {
  var newsSources = document.getElementsByClassName("news-source")
  var subjects = document.getElementsByClassName("subject")
  var chosenSources = []
  var chosenSubjects = []
  for(var i=0; i<newsSources.length; i++) {
    if(newsSources[i].value == "on") {
      chosenSources.push(newsSources[i].getAttribute("data-sourceName"))
    }
  }
  for(var i=0; i<subjects.length; i++) {
    if(subjects[i].value == "on") {
      chosenSubjects.push(subjects[i].getAttribute("data-subject"))
    }
  }

  inputValues = [chosenSources, chosenSubjects, chosenSubjects.length]
  return inputValues
}

async function getArticlesFromPage() {
  var siteDictionary = {
    'New York Times': {
      'science': 'https://www.nytimes.com/section/science',
      'tech': 'https://www.nytimes.com/section/technology',
      'business': 'https://www.nytimes.com/section/business'
    },
    'The Verge': {
      'science': 'https://www.theverge.com/science',
      'tech': 'https://www.theverge.com/tech'
    },
    'Neuroscience News': {
      'science': 'https://neurosciencenews.com/',
      'tech': 'https://neurosciencenews.com/neuroscience-topics/artificial-intelligence-2/'
    }
  }

  let [chosenSources, chosenSubjects] = await getValueOfInputs();

  urlsToScrape = []
  for(var i=0;i<chosenSources.length; i++) {
    for(var e=0; e<chosenSubjects.length; e++) {
      if(siteDictionary[chosenSources[i]].hasOwnProperty(chosenSubjects[e]) == true) {
        urlsToScrape.push([siteDictionary[chosenSources[i]][chosenSubjects[e]], chosenSubjects[e], chosenSources[i]])
      }
    }
  }

  let finalHTML = await eel.generateHTML(urlsToScrape, chosenSubjects)();

  document.getElementById("article-container").innerHTML = ""
  document.getElementById("article-container").innerHTML += finalHTML

  // element.innerHTML += "additional HTML code"
}
