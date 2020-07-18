/**
 * Author: Agustin Bassi
 * Date: July 2020
 * Licence: GPLv3+
 * Brief: TODO comment it
 */

//=======[ Settings & Data ]===================================================

const MAX_LOG_LINES = 50;

const DEFAULT_MQTT_HOST   = "localhost";
const DEFAULT_MQTT_PORT   = 9001;
const DEFAULT_MQTT_PATH   = "/mqtt";
const DEFAULT_MQTT_CLIENT = "web_mqtt_client";
const MQTT_RECONNECT_TIMEOUT = 2000;

var MqttClientObj;

//=======[ Utils ]=============================================================

function View_ShowLogData(server_response) {
    var json_response = JSON.parse(server_response);
    console.log("Data received is: " + server_response);
    document.getElementById("logs_textarea").innerHTML = server_response;
}

function View_AppendLogData(server_response) {
    current_value = document.getElementById("logs_textarea").value; 
    // clear logs text area when lines superates MAX_LOG_LINES
    if (current_value.split("\n").length-1 >= MAX_LOG_LINES){
        View_ClearLogData();
        current_value = "";
    } 
    document.getElementById("logs_textarea").innerHTML = server_response + "\n" + current_value;
}

function View_ClearLogData(){
    console.log("Clearing view data")
    document.getElementById("logs_textarea").innerHTML = "";
}

function Utils_GetElementValue(element_to_get){
    if (element_to_get == "mqtt_host" ||
        element_to_get == "mqtt_port" ||
        element_to_get == "mqtt_client" ||
        element_to_get == "mqtt_topic_subscription" ||
        element_to_get == "mqtt_topic_publish" ||
        element_to_get == "mqtt_payload_publish"){
        return document.getElementById(element_to_get).value;
    } 
    else {
        return null;
    }
}

//=======[ MQTT Management ]===================================================

function Mqtt_LogSettings(){
    console.log("MQTT host:   " + Utils_GetElementValue("mqtt_host"));
    console.log("MQTT port:   " + Utils_GetElementValue("mqtt_port"));
    console.log("MQTT client: " + Utils_GetElementValue("mqtt_client"));
}


function Mqtt_OnSuccess(){
    View_AppendLogData("[ INFO ] - Connection to " + host + ':' + port + path);
}


function Mqtt_OnFailure(message) {
    View_AppendLogData("[ERROR] - Connection failed: " + message.errorMessage + ". Retrying");
    setTimeout(ConnectToMqttBroker, MQTT_RECONNECT_TIMEOUT);
}

function Mqtt_OnConnectionLost(message) {
    setTimeout(ConnectToMqttBroker, MQTT_RECONNECT_TIMEOUT);
    View_AppendLogData("[ ERROR ] - Connection lost: " + message.errorMessage + ". Reconnecting...");
};

function Mqtt_OnMessageArrived(message) {
    var topic = message.destinationName;
    var payload = message.payloadString;
    View_AppendLogData("[ INFO ] - '" + topic + "' -> " + payload)
};

//=======[ User actions ]======================================================

function SubscribeMqttTopic(){
    topic = Utils_GetElementValue("mqtt_topic_subscription");
    if (topic == null || topic == "" || topic == "undefined"){
        topic = "#";
    }
    View_AppendLogData("[ INFO ] - Subscribed to topic: '" + topic + "'");
    MqttClientObj.subscribe(topic, {qos: 0});
}

function PublishMqttTopic(){

}

function ConnectToMqttBroker(){

    // at first los current settings
    Mqtt_LogSettings();

    // obtain the HTML elements in a friendly way
    mqtt_host   = host; // '127.0.0.1';      // document.getElementById("mqtt_host");
    mqtt_port   = port; //9001;             // document.getElementById("mqtt_port");
    mqtt_topic  = topic; //"#";              // document.getElementById("mqtt_topic");
    mqtt_client = "web-client-" + parseInt(Math.random() * 100, 10);     // document.getElementById("mqtt_client");
    // mqtt_path   = DEFAULT_MQTT_PATH;

    if (typeof path == "undefined") {
		path = '/mqtt';
    }
    
    useTLS         = false;
    username       = null;
    password       = null;
    cleansession   = true;
    timeout        = 3;
    reconnectTimeout = 2000;

    MqttClientObj = new Paho.MQTT.Client(
        mqtt_host,
        mqtt_port,
        path,
        mqtt_client
    );

    var mqttOptions = {
        timeout      : timeout,
        useSSL       : useTLS,
        cleanSession : cleansession,
        onSuccess    : Mqtt_OnSuccess,
        onFailure    : Mqtt_OnFailure
    };

    MqttClientObj.onConnectionLost = Mqtt_OnConnectionLost;
    MqttClientObj.onMessageArrived = Mqtt_OnMessageArrived;

    if (username != null) {
        mqttOptions.userName = username;
        mqttOptions.password = password;
    }
    // TODO: maybe here a good place to log current configuration
    MqttClientObj.connect(mqttOptions);
}


//=======[ End of file ]=======================================================
