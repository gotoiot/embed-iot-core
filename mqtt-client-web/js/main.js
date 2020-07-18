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
    View_AppendLogData("[ INFO ] - Connected to MQTT Broker correctly");// + host + ':' + port + path);
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
    topic = Utils_GetElementValue("mqtt_topic_subscription");
    if (topic == null || topic == "" || topic == "undefined"){
        topic = "#";
    }
    // Try subscription to topic
    MqttClientObj.subscribe(topic, {qos: 0});
    // log action done
    View_AppendLogData("[ INFO ] - Subscribed to topic: '" + topic + "'");
}

function App_PublishMqttTopic(){
    // get topic value from UI or set default one
    topic = Utils_GetElementValue("mqtt_topic_publish");
    if (topic == null || topic == "" || topic == "undefined"){
        topic = "mq-connection/default-topic";
    }
    // get payload value from UI or set default one
    payload = Utils_GetElementValue("mqtt_payload_publish");
    if (payload == null || payload == "" || payload == "undefined"){
        payload = "default-payload";
    }
    // Send the message to broker
    message = new Paho.MQTT.Message(payload);
    message.destinationName = topic;
    MqttClientObj.send(message); 
    // log action done
    View_AppendLogData("[ INFO ] - Publishing topic: '" + topic + "' -> '" + payload + "'");
}

function App_ConnectToMqttBroker(){
    // at first los current settings
    Mqtt_LogSettings();
    // obtain the HTML elements in a friendly way
    const mqttHost   = Utils_GetElementValue("mqtt_host");
    const mqttPort   = parseInt(Utils_GetElementValue("mqtt_port"));
    const mqttClient = Utils_GetElementValue("mqtt_client"); 
    // connection option settings
    let timeout      = 3;
    let useTLS       = false;
    let cleansession = true;
    // authentication settings
    let username       = null;
    let password       = null;
    // Create the client object from user settings
    MqttClientObj = new Paho.MQTT.Client(
        mqttHost,
        mqttPort,
        mqttClient
    );
    // Set connection config options
    var mqttOptions = {
        timeout      : timeout,
        useSSL       : useTLS,
        cleanSession : cleansession,
        onSuccess    : Mqtt_OnSuccess,
        onFailure    : Mqtt_OnFailure
    };
    // Set event callbacks
    MqttClientObj.onConnectionLost = Mqtt_OnConnectionLost;
    MqttClientObj.onMessageArrived = Mqtt_OnMessageArrived;
    // Add authentication option if needed
    if (username != null) {
        mqttOptions.userName = username;
        mqttOptions.password = password;
    }
    // TODO: maybe here a good place to log current configuration
    MqttClientObj.connect(mqttOptions);
}

//=======[ End of file ]=======================================================
