
// const http_handler = new XMLHttpRequest();

// const URL = 'http://localhost:5000/api/v1/ibeacons_settings/';

// http_handler.open("GET", URL);
// // Http.setRequestHeader('Content-Type', 'application/json');
// http_handler.setRequestHeader('Accept', 'application/json');

// http_handler.send();

// http_handler.onreadystatechange = (e) => {
//   console.log(http_handler.responseText)
// }

// function execute_http_request(){
    
// }

// var http_handler = new XMLHttpRequest();

// var URI = "http://localhost:5000/api/v1/ibeacons_settings/";

// http_handler.onreadystatechange = function() {
//     if (this.readyState == 4 && this.status == 200) {

//         var json_response = JSON.parse(http_handler.responseText);
//         parse_response(json_response);
//         // console.log(http_handler.responseText);
//     }
// };

// http_handler.open("GET", URI, true);
// http_handler.setRequestHeader('Accept', 'application/json');
// http_handler.send();

// function parse_response(json_response) {
//     console.log("Data received is: " + json_response);
//     document.getElementById("logs_textarea").innerHTML = json_response;
// }

/**
 * Author: Agustin Bassi
 * Date: July 2020
 * Licence: GPLv3+
 * Brief: TODO comment it
 */

//=======[ Settings & Data ]===================================================

var URI = "http://localhost:5000/api/v1/ibeacons_settings/";

var http_handler = new XMLHttpRequest();

//=======[ Utils ]=============================================================

function parse_server_response(server_response) {
    var json_response = JSON.parse(server_response);
    console.log("Data received is: " + server_response);
    document.getElementById("logs_textarea").innerHTML = server_response;
}

function log_current_settings(){
    url           = document.getElementById("post_url").value;
    data          = document.getElementById("post_data").value;
    poll_checkbox = document.getElementById("poll_checkbox").checked;
    poll_secs     = document.getElementById("poll_secs").value;
    http_method   = document.getElementById("http_method").value;

    console.log("url:           " + url);
    console.log("data:          " + data);
    console.log("poll_checkbox: " + poll_checkbox);
    console.log("poll_secs:     " + poll_secs);
    console.log("http_method:   " + http_method);

}

//=======[ Module functions ]==================================================

function execute_http_request(){

    log_current_settings();

    http_handler.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            parse_server_response(http_handler.responseText);
        }
    };
    
    http_handler.open("GET", URI, true);
    http_handler.setRequestHeader('Accept', 'application/json');
    http_handler.send();
}
