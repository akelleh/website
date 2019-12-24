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
