#include <WiFi.h>
#include <PubSubClient.h>

const int SensorPin = 15; // PIR Sensor Pin
int SensorID = 1;
int SensorValue = 0;

// Replace the next variables with your SSID/Password combination
const char* ssid = "WBSENSOR";
const char* password = "eswerdelicht";

//const char* ssid = "Die Omi aus dem 1. Stock";
//const char* password = "1337buegeleisen";

// Add your MQTT Broker IP address, example:
//const char* mqtt_server = "192.168.0.92";
const char* mqtt_server = "192.168.0.2";

long lastMsg;

WiFiClient espClient;

PubSubClient client(espClient);


void setup() {
  Serial.begin(115200);
  
  pinMode(SensorPin, INPUT); // Sets the echoPin as an Input
  
  setup_wifi();
  
  client.setServer(mqtt_server, 1883);

}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    char StringID[2];
    dtostrf(SensorID, 2, 0, StringID);
    if (client.connect(StringID)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }

  }
}



void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  SensorValue = digitalRead(SensorPin);

  long now = millis();

  if ((now - lastMsg > 200) && SensorValue > 0) {
    lastMsg = now;
    
    char StringSend[2];
    
    dtostrf(SensorID, 2, 0, StringSend);

    Serial.println(StringSend);
        
    client.publish("esp32/pirsensor", StringSend);
  }

  delay(10);
}
