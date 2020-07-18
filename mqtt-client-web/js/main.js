/**
 * Author: Agustin Bassi
 * Date: July 2020
 * Licence: GPLv3+
 * Brief: TODO comment it
 */

//=======[ Settings & Data ]===================================================

const MAX_LOG_LINES = 10;

const DEFAULT_MQTT_HOST   = "localhost";
const DEFAULT_MQTT_PORT   = 9001;
const DEFAULT_MQTT_PATH   = "/path";
const DEFAULT_MQTT_CLIENT = "web_mqtt_client";
const MQTT_RECONNECT_TIMEOUT = 2000;

var MqttClientObj;

//=======[ Utils ]=============================================================

function send_data_to_view(server_response) {
    var json_response = JSON.parse(server_response);
    console.log("Data received is: " + server_response);
    document.getElementById("logs_textarea").innerHTML = server_response;
}

function append_data_to_view(server_response) {
    current_value = document.getElementById("logs_textarea").value; 
    // log_lines     = get_element_value("log_lines");
    // log_lines     = parseInt(log_lines);
    // if (current_value.split("\n").length-1 >= log_lines){
    if (current_value.split("\n").length-1 >= MAX_LOG_LINES){
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
    // mq_mqtt_host   = document.getElementById("mq_mqtt_host").value;
    // mq_mqtt_port  = document.getElementById("mq_mqtt_port").value;
    // mq_mqtt_topic = document.getElementById("mq_mqtt_topic").value;
    // mq_mqtt_client = document.getElementById("mq_mqtt_client").value;

    // console.log("mq_mqtt_host:   " + mq_mqtt_host);
    // console.log("mq_mqtt_port:  " + mq_mqtt_port);
    // console.log("mq_mqtt_topic: " + mq_mqtt_topic);
    // console.log("mq_mqtt_client: " + mq_mqtt_client);

    console.log("mq_mqtt_host:   " + "mq_mqtt_host");
    console.log("mq_mqtt_port:  " + "mq_mqtt_port");
    console.log("mq_mqtt_topic: " + "mq_mqtt_topic");
    console.log("mq_mqtt_client: " + "mq_mqtt_client");
}

function get_element_value(element_to_get){
    // if (element_to_get == "mq_mqtt_host" ||
    //     element_to_get == "mq_mqtt_port" ||
    //     element_to_get == "mq_mqtt_topic" ||
    //     element_to_get == "mq_mqtt_client"){
    //     return document.getElementById(element_to_get).value;
    // } 
    // // else if (element_to_get == "poll_checkbox"){
    // //     return document.getElementById(element_to_get).checked;
    // // } 
    // else {
    //     return null;
    // }
    return "";
}

//=======[ Module functions ]==================================================

// function execute_http_request(){

//     // at first los current settings
//     log_current_settings();

//     // obtain the HTML elements in a friendly way
//     request_url   = get_element_value("request_url");
//     request_data  = get_element_value("request_data");
//     poll_checkbox = get_element_value("poll_checkbox");
//     poll_secs     = get_element_value("poll_secs");
//     http_method   = get_element_value("http_method");

//     // callback when HTTP request is done
//     HttpHandler.onreadystatechange = function() {
//         if (this.readyState == 4 && (this.status == 200 || this.status == 201 )) {
//             if (is_interval_set()){
//                 append_data_to_view(HttpHandler.responseText);
//             } else {
//                 send_data_to_view(HttpHandler.responseText);
//             }
//         } else{
//             console.log("The server has returned an error code");
//         }
//     };

//     // clear view in order to start new log session
//     clear_view_data();

//     // clear interval if exists
//     clear_poll_interval();

//     // evaluate HTTP method
//     if(http_method.toLowerCase() == "get"){

//         HttpHandler.open("GET", request_url, true);
//         HttpHandler.setRequestHeader('Accept', 'application/json');
//         HttpHandler.send();

//         if(poll_checkbox == true){

//             console.log("Executing poll request each seconds " + poll_secs)
            
//             poll_secs = parseInt(poll_secs);
            
//             PollReqInterval = setInterval(function(){
//                 HttpHandler.open("GET", request_url, true);
//                 HttpHandler.setRequestHeader('Accept', 'application/json');
//                 HttpHandler.send();
//             }, poll_secs * 1000);
//         }

//     } else if(http_method.toLowerCase() == "post" || http_method.toLowerCase() == "put"){

//         // request_data = JSON.parse(request_data);

//         HttpHandler.open(http_method.toUpperCase(), request_url);
//         HttpHandler.setRequestHeader('Accept', 'application/json');
//         HttpHandler.setRequestHeader("Content-type", 'application/json;charset=UTF-8');
//         HttpHandler.send(JSON.stringify(request_data));

//         // The PUT or POST methods must not be executed in polling mode

//     } else if(http_method.toLowerCase() == "put"){

//     } else {
//         console.log("Unsupported HTTP Method selected by the user")
//     }
// }

//=======[ MQTT Management ]===================================================

function execute_mqtt_connection() {

    // at first los current settings
    log_current_settings();

    // obtain the HTML elements in a friendly way
    mq_mqtt_host   = "test"; //document.getElementById("mq_mqtt_host").value;
    mq_mqtt_port   = "test"; //document.getElementById("mq_mqtt_port").value;
    mq_mqtt_topic  = "test"; //document.getElementById("mq_mqtt_topic").value;
    mq_mqtt_client = "test"; //document.getElementById("mq_mqtt_client").value;
    mq_mqtt_path   = DEFAULT_MQTT_PATH;

    // topic          = '#';
    useTLS         = false;
    username       = null;
    password       = null;
    cleansession   = true;
    timeout        = 3;

    // MqttClientObj = new Paho.MQTT.Client(
    //     mq_mqtt_host,
    //     mq_mqtt_port,
    //     mq_mqtt_path,
    //     mq_mqtt_client
    // );

    // var options = {
    //     timeout      : timeout,
    //     useSSL       : useTLS,
    //     cleanSession : cleansession,
    //     onSuccess    : onConnect,
    //     onFailure    : onFailure 
    // };

    // MqttClientObj.onConnectionLost = onConnectionLost;
    // MqttClientObj.onMessageArrived = onMessageArrived;

    // // if (username != null) {
    // //     options.userName = username;
    // //     options.password = password;
    // // }

    // // console.log("Host="+ host + ", port=" + port + ", path=" + path + " TLS = " + useTLS + " username=" + username + " password=" + password);
    
    // MqttClientObj.connect(options);
}

function onFailure(message) {
    append_data_to_view("Connection failed: " + message.errorMessage + "Retrying");
    // $('#status').val("Connection failed: " + message.errorMessage + "Retrying");
    setTimeout(execute_mqtt_connection, MQTT_RECONNECT_TIMEOUT);
}
    
function onConnect() {

    topic = "#";

    // $('#status').val('Connected to ' + host + ':' + port + path);
    append_data_to_view("[ INFO ]: Connection to " + host + ':' + port + path);
    // Connection succeeded; subscribe to our topic
    MqttClientObj.subscribe(topic, {qos: 0});
    // $('#topic').val(topic);
}

function onConnectionLost(response) {
    setTimeout(execute_mqtt_connection, MQTT_RECONNECT_TIMEOUT);
    // $('#status').val("connection lost: " + responseObject.errorMessage + ". Reconnecting");
    append_data_to_view("[ ERROR ]: Connection lost (" + responseObject.errorMessage + "). Reconnecting...");
};

function onMessageArrived(message) {
    var topic = message.destinationName;
    var payload = message.payloadString;

    append_data_to_view("[ " + top + " ]" + " - " + payload)
    // $('#ws').prepend('<li>' + topic + ' = ' + payload + '</li>');
};

// $(document).ready(function() {
//     MQTTconnect();
// });

//=======[ End of file ]=======================================================
