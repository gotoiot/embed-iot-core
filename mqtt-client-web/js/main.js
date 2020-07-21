/**
 * Author: Agustin Bassi
 * Date: July 2020
 * Licence: GPLv3+
 * Brief: TODO comment it
 */

//=======[ Settings & Data ]===================================================

// DEFAULT SETTINGS IN CASE USER DONT SELECT THEM
const DEFAULT_MQTT_HOST       = "localhost";
const DEFAULT_MQTT_PORT       = 9001;
const DEFAULT_MQTT_PATH       = "/mqtt";
const DEFAULT_MQTT_CLIENT     = "MQ-Connection-Web-Client" + parseInt(Math.random() * 100, 10);
const DEFAULT_MQTT_TOPIC_SUB  = "#";
const DEFAULT_MQTT_TOPIC_PUB  = "mq-connection/default-topic";
const DEFAULT_MQTT_PAYLOAD    = "mq-connection/default-payload";
// UNIQUE SETTINGS OF APPLICATION
const MQTT_TIMEOUT            = 3;
const MQTT_TLS_FLAG           = false
const MQTT_CLEAN_SESSION_FLAG = true;
const MQTT_RECONNECT_TIMEOUT  = 2000;
const MQTT_USERNAME           = null;
const MQTT_PASSWOD            = null;
const LOG_MAX_LINES           = 50;

// The object where Paho MQTT instance is
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
    if (current_value.split("\n").length-1 >= LOG_MAX_LINES){
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
    // TODO: Evaluate other element types like checkbox, dropdown, etc.
    return document.getElementById(element_to_get).value;
}

function Utils_IsInvalidValue(value){
    if (value == null || value == "" || value == "undefined"){
        return true;
    }
    return false;
}

//=======[ MQTT Management ]===================================================

function Mqtt_LogSettings(mqttHost, mqttPort, mqttClient){
    console.log(
        "Connection to: " + 
        mqttHost + ":" + 
        mqttPort + "/" +
        mqttClient
        );
}

function Mqtt_OnSuccess(){
    View_AppendLogData("[ INFO ] - Connected to MQTT Broker correctly");
}

function Mqtt_OnFailure(message) {
    View_AppendLogData("[ERROR] - Connection failed: " + message.errorMessage + ". Retrying...");
    setTimeout(App_ConnectToMqttBroker, MQTT_RECONNECT_TIMEOUT);
}

function Mqtt_OnConnectionLost(message) {
    setTimeout(App_ConnectToMqttBroker, MQTT_RECONNECT_TIMEOUT);
    View_AppendLogData("[ ERROR ] - Connection lost: " + message.errorMessage + ". Reconnecting...");
};

function Mqtt_OnMessageArrived(message) {
    var topic = message.destinationName;
    var payload = message.payloadString;
    View_AppendLogData("[ INFO ] - '" + topic + "' -> " + payload)
};

//=======[ Module main code ]==================================================

function App_SubscribeMqttTopic(){
    // get topic value from UI or set default one
    let topic = Utils_GetElementValue("mqtt_topic_subscription");
    if (Utils_IsInvalidValue(topic)){
        topic = DEFAULT_MQTT_TOPIC_SUB;
    }
    // Try subscription to topic
    MqttClientObj.subscribe(topic, {qos: 0});
    // log action done
    View_AppendLogData("[ INFO ] - Subscribed to topic: '" + topic + "'");
}

function App_PublishMqttTopic(){
    // get topic value from UI or set default one
    let topic = Utils_GetElementValue("mqtt_topic_publish");
    if (Utils_IsInvalidValue(topic)){
        topic = DEFAULT_MQTT_TOPIC_PUB;
    }
    // get payload value from UI or set default one
    let payload = Utils_GetElementValue("mqtt_payload_publish");
    if (Utils_IsInvalidValue(payload)){
        payload = DEFAULT_MQTT_PAYLOAD;
    }
    // Send the message to broker
    let message = new Paho.MQTT.Message(payload);
    message.destinationName = topic;
    MqttClientObj.send(message); 
    // log action done
    View_AppendLogData("[ INFO ] - Publishing topic: '" + topic + "' -> '" + payload + "'");
}

function App_ConnectToMqttBroker(){
    // obtain the HTML elements in a friendly way (assign default if needed)
    let mqttHost   = Utils_GetElementValue("mqtt_host");
    if (Utils_IsInvalidValue(mqttHost)){
        mqttHost = DEFAULT_MQTT_HOST;
    }
    let mqttPort   = Utils_GetElementValue("mqtt_port");
    if (Utils_IsInvalidValue(mqttPort)){
        mqttPort = DEFAULT_MQTT_PORT;
    } else {
        mqttPort = parseInt(mqttPort);
    }
    let mqttClient = Utils_GetElementValue("mqtt_client"); 
    if (Utils_IsInvalidValue(mqttPort)){
        mqttPort = DEFAULT_MQTT_CLIENT;
    }
    // Show current settings
    Mqtt_LogSettings(mqttHost, parseInt(mqttPort), mqttClient);
    // connection option settings
    let timeout      = MQTT_TIMEOUT;
    let useTLS       = MQTT_TLS_FLAG;
    let cleanSession = MQTT_CLEAN_SESSION_FLAG;
    // authentication settings
    let username     = MQTT_USERNAME;
    let password     = MQTT_PASSWOD;
    // Create the client object from user settings
    MqttClientObj = new Paho.MQTT.Client(mqttHost, mqttPort, mqttClient);
    // Set connection config options
    var mqttOptions = {
        timeout      : timeout,
        useSSL       : useTLS,
        cleanSession : cleanSession,
        onSuccess    : Mqtt_OnSuccess,
        onFailure    : Mqtt_OnFailure
    };
    // Add authentication option if needed
    if (username != null) {
        mqttOptions.userName = username;
        mqttOptions.password = password;
    }
    // Set event callbacks
    MqttClientObj.onConnectionLost = Mqtt_OnConnectionLost;
    MqttClientObj.onMessageArrived = Mqtt_OnMessageArrived;
    // TODO: maybe here a good place to log current configuration
    MqttClientObj.connect(mqttOptions);
}

//=======[ End of file ]=======================================================
