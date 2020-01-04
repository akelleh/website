function getRequest(theUrl){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function turnOff(host, port){
    baseUrl = window.location.protocol + "//" + host + ":" + port;
    theUrl = baseUrl + "/power?on=0";
    getRequest(theUrl)
}

function turnOn(host, port){
    baseUrl = window.location.protocol + "//" + host + ":" + port;
    theUrl = baseUrl + "/power?on=1";
    getRequest(theUrl)
}

function updateOnOffButton(host, port, div){
    baseUrl = window.location.protocol + "//" + host + ":" + port;
    theUrl = baseUrl + "/status";
    console.log(theUrl)

    var buttonStatus = getRequest(theUrl);
    if ( buttonStatus == 'On') {
        buttonHtml = "<button class=\"w3-button w3-padding-large w3-white w3-border\" onClick=\"turnOff(\'" + host + "\',\'" + port + "\');updateOnOffButton(\'" + host + "\',\'" + port + "\',\'" + div + "\')\"><div id=\"on-off-button-text-" + div + "\">Turn Off Camera</div></button>"
    }
    else {
        buttonHtml = "<button class=\"w3-button w3-padding-large w3-white w3-border\" onClick=\"turnOn(\'" + host + "\',\'" + port + "\');updateOnOffButton(\'" + host + "\',\'" + port + "\',\'" + div + "\')\"><div id=\"on-off-button-text-" + div + "\">Turn On Camera</div></button>"
    }
    console.log(buttonHtml)
    div = "#" + div;
    $(div).html(buttonHtml);
}