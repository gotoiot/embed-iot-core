/**
 * Author: Agustin Bassi
 * Date: July 2020
 * Licence: GPLv3+
 * Brief: TODO comment it
 */

//=======[ Settings & Data ]===================================================

const MAX_LOG_LINES = 10;
const DEFAULT_URL   = "http://localhost:5000/api/v1/ibeacons_settings/";

var HttpHandler     = new XMLHttpRequest();
var PollReqInterval = null;

//=======[ Utils ]=============================================================

function send_data_to_view(server_response) {
    var json_response = JSON.parse(server_response);
    console.log("Data received is: " + server_response);
    document.getElementById("logs_textarea").innerHTML = server_response;
}

function append_data_to_view(server_response) {
    current_value = document.getElementById("logs_textarea").value; 
    log_lines     = get_element_value("log_lines");
    log_lines     = parseInt(log_lines);
    if (current_value.split("\n").length-1 >= log_lines){
        clear_view_data();
        current_value = "";
    } 
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
        element_to_get == "log_lines" ||
        element_to_get == "http_method"){
        return document.getElementById(element_to_get).value;
    } else if (element_to_get == "poll_checkbox"){
        return document.getElementById(element_to_get).checked;
    } else {
        return null;
    }
}

function clear_poll_interval(){
    if(PollReqInterval != null){
        clearInterval(PollReqInterval);
        PollReqInterval = null;
    }
}

function is_interval_set(){
    return PollReqInterval != null;
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
    HttpHandler.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status == 200 || this.status == 201 )) {
            if (is_interval_set()){
                append_data_to_view(HttpHandler.responseText);
            } else {
                send_data_to_view(HttpHandler.responseText);
            }
        } else{
            console.log("The server has returned an error code");
        }
    };

    // clear view in order to start new log session
    clear_view_data();

    // clear interval if exists
    clear_poll_interval();

    // evaluate HTTP method
    if(http_method.toLowerCase() == "get"){

        HttpHandler.open("GET", request_url, true);
        HttpHandler.setRequestHeader('Accept', 'application/json');
        HttpHandler.send();

        if(poll_checkbox == true){

            console.log("Executing poll request each seconds " + poll_secs)
            
            poll_secs = parseInt(poll_secs);
            
            PollReqInterval = setInterval(function(){
                HttpHandler.open("GET", request_url, true);
                HttpHandler.setRequestHeader('Accept', 'application/json');
                HttpHandler.send();
            }, poll_secs * 1000);
        }

    } else if(http_method.toLowerCase() == "post" || http_method.toLowerCase() == "put"){

        // request_data = JSON.parse(request_data);

        HttpHandler.open(http_method.toUpperCase(), request_url);
        HttpHandler.setRequestHeader('Accept', 'application/json');
        HttpHandler.setRequestHeader("Content-type", 'application/json;charset=UTF-8');
        HttpHandler.send(JSON.stringify(request_data));

        // The PUT or POST methods must not be executed in polling mode

    } else if(http_method.toLowerCase() == "put"){

    } else {
        console.log("Unsupported HTTP Method selected by the user")
    }
}

//=======[ End of file ]=======================================================
