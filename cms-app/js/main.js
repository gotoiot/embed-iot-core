
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

var DEFAULT_URL = "http://localhost:5000/api/v1/ibeacons_settings/";

var http_handler = new XMLHttpRequest();

var interval = null;

//=======[ Utils ]=============================================================

function send_data_to_view(server_response) {
    var json_response = JSON.parse(server_response);
    console.log("Data received is: " + server_response);
    document.getElementById("logs_textarea").innerHTML = server_response;
}

function append_data_to_view(server_response) {
    current_value = document.getElementById("logs_textarea").value; 
    document.getElementById("logs_textarea").innerHTML = server_response + "\n" + current_value;
}

function clear_view_data(){
    console.log("Clearing view data")
    document.getElementById("logs_textarea").innerHTML = "";
}

function log_current_settings(){
    request_url   = document.getElementById("request_url").value;
    request_data  = document.getElementById("request_data").value;
    poll_checkbox = document.getElementById("poll_checkbox").checked;
    poll_secs     = document.getElementById("poll_secs").value;
    http_method   = document.getElementById("http_method").value;

    console.log("request_url:   " + request_url);
    console.log("request_data:  " + request_data);
    console.log("poll_checkbox: " + poll_checkbox);
    console.log("poll_secs:     " + poll_secs);
    console.log("http_method:   " + http_method);
}

function get_element_value(element_to_get){
    if (element_to_get == "request_url" ||
        element_to_get == "request_data" ||
        element_to_get == "poll_secs" ||
        element_to_get == "http_method"){
        return document.getElementById(element_to_get).value;
    } else if (element_to_get == "poll_checkbox"){
        return document.getElementById(element_to_get).checked;
    } else {
        return null;
    }
}

function clear_poll_interval(){
    if(interval != null){
        clearInterval(interval);
        interval = null;
    }
}

function is_interval_set(){
    return interval != null;
}




//=======[ Module functions ]==================================================

function execute_http_request(){

    // at first los current settings
    log_current_settings();

    // obtain the HTML elements in a friendly way
    request_url   = get_element_value("request_url");
    request_data  = get_element_value("request_data");
    poll_checkbox = get_element_value("poll_checkbox");
    poll_secs     = get_element_value("poll_secs");
    http_method   = get_element_value("http_method");

    // callback when HTTP request is done
    http_handler.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status == 200 || this.status == 201 )) {
            if (is_interval_set()){
                append_data_to_view(http_handler.responseText);
            } else {
                send_data_to_view(http_handler.responseText);
            }
        } else{
            // alert("The server has returned an error code");
        }
    };

    // clear view in order to start new log session
    clear_view_data();

    // clear interval if exists
    clear_poll_interval();

    // evaluate HTTP method
    if(http_method.toLowerCase() == "get"){

        http_handler.open("GET", request_url, true);
        http_handler.setRequestHeader('Accept', 'application/json');
        http_handler.send();

        if(poll_checkbox == true){

            console.log("Executing poll request for seconds " + poll_secs)
            
            poll_secs = parseInt(poll_secs);
            
            interval = setInterval(function(){
                http_handler.open("GET", request_url, true);
                http_handler.setRequestHeader('Accept', 'application/json');
                http_handler.send();
            }, poll_secs * 1000);
        }

    } else if(http_method.toLowerCase() == "post"){

    } else if(http_method.toLowerCase() == "put"){

    } else {
        // alert("Unsupported HTTP Method");
    }
}

//=======[ End of file ]=======================================================
