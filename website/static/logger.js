

function httpGetAsync(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous
    xmlHttp.send(null);
}

const encodeGetParams = p =>
  Object.entries(p).map(kv => kv.map(encodeURIComponent).join("=")).join("&");

function log_click(click_type, item_id, item_position, user_id, ts, event_id) {
  params = {"click_type": click_type,
            "item_id": item_id,
            "item_position": item_position,
            "user_id": user_id,
            "ts_": ts,
            "event_id": event_id}
  var url = "logger:8889/?" + encodeGetParams(params)
  httpGetAsync(url)
}

