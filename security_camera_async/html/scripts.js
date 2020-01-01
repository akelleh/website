function getRequest(theUrl){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function turnOff(){
    baseUrl = window.location.protocol + "//" + window.location.host;
    theUrl = baseUrl + "/power?on=0";
    getRequest(theUrl)
}

function turnOn(){
    baseUrl = window.location.protocol + "//" + window.location.host;
    theUrl = baseUrl + "/power?on=1";
    getRequest(theUrl)
}

function updateOnOffButton(){
    baseUrl = window.location.protocol + "//" + window.location.host;
    theUrl = baseUrl + "/status";
    var buttonStatus = getRequest(theUrl);
    if ( buttonStatus == 'On') {
        buttonHtml = "<button onClick=\"turnOff();updateOnOffButton()\"><div id=\"on-off-button-text\">Turn Off Camera</div></button>"
    }
    else {
        buttonHtml = "<button onClick=\"turnOn();updateOnOffButton()\"><div id=\"on-off-button-text\">Turn On Camera</div></button>"
    }
    $("#on-off-button").html(buttonHtml);
}