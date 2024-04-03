function HTTPRequest(URL, method = "GET", body = null) {
  let xmlHttp = new XMLHttpRequest();
  xmlHttp.open(method, LIGHT_URL + URL, false);
  xmlHttp.send(body);
  return xmlHttp.responseText;
}

window.onload = () => {};
