#include <WiFi.h>
#include <PubSubClient.h>
#include <EmonLib.h>


// ================= WIFI + MQTT =================
const char* ssid = "Mx ◍˃ᵕ˂◍"; 
const char* password = "secret128!";


// ================= MQTT =================
const char* mqtt_server = "172.20.10.14";


// ================= CT SENSORS =================
#define CT_LAMP      32
#define CT_KETTLE    33
#define CT_TOASTER   34
#define CT_LAPTOP    35


// ================= ZMPT101B =================
#define VOLTAGE_PIN 39


// ================= RELAYS =================
#define RELAY_LAMP      17
#define RELAY_LAPTOP    18
#define RELAY_KETTLE    19
#define RELAY_TOASTER   21


WiFiClient espClient;
PubSubClient client(espClient);


// ================= ENERGY MONITORS =================
EnergyMonitor ctLamp;
EnergyMonitor ctKettle;
EnergyMonitor ctToaster;
EnergyMonitor ctLaptop;


// ================= CALIBRATION =================
double calibration = 135;

// =========================================
// MQTT CALLBACK
// =========================================
void callback(char* topic, byte* payload, unsigned int length)
{
 String msg = "";


 for (int i = 0; i < length; i++)
 {
   msg += (char)payload[i];
 }


 Serial.println("MQTT RECEIVED:");
 Serial.println(msg);


 if (msg.indexOf("\"lamp\":\"OFF\"") >= 0)
   digitalWrite(RELAY_LAMP, LOW);
 else if (msg.indexOf("\"lamp\":\"ON\"") >= 0)
   digitalWrite(RELAY_LAMP, HIGH);


 if (msg.indexOf("\"laptop\":\"OFF\"") >= 0)
   digitalWrite(RELAY_LAPTOP, LOW);
 else if (msg.indexOf("\"laptop\":\"ON\"") >= 0)
   digitalWrite(RELAY_LAPTOP, HIGH);


 if (msg.indexOf("\"kettle\":\"OFF\"") >= 0)
   digitalWrite(RELAY_KETTLE, LOW);
 else if (msg.indexOf("\"kettle\":\"ON\"") >= 0)
   digitalWrite(RELAY_KETTLE, HIGH);


 if (msg.indexOf("\"toaster\":\"OFF\"") >= 0)
   digitalWrite(RELAY_TOASTER, LOW);
 else if (msg.indexOf("\"toaster\":\"ON\"") >= 0)
   digitalWrite(RELAY_TOASTER, HIGH);
}


// =========================================
// WIFI CONNECT
// =========================================
void setupWiFi()
{
  Serial.println("Connecting WiFi...");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected");
  Serial.println(WiFi.localIP());
}


// =========================================
// MQTT RECONNECT
// =========================================
void reconnect()
{
 while (!client.connected())
 {
   Serial.println("Connecting MQTT...");


   if (client.connect("ESP32_FYP"))
   {
     Serial.println("MQTT Connected");


     client.subscribe("home/control");
   }
   else
   {
     Serial.print("Failed rc=");
     Serial.println(client.state());


     delay(2000);
   }
 }
}


// =========================================
// READ VOLTAGE
// =========================================
float readVoltage()
{
 int raw = analogRead(VOLTAGE_PIN);


 float voltage = map(raw, 0, 4095, 0, 250);


 return voltage;
}


// =========================================
// SETUP
// =========================================
void setup()
{
 Serial.begin(115200);


 pinMode(RELAY_LAMP, OUTPUT);
 pinMode(RELAY_LAPTOP, OUTPUT);
 pinMode(RELAY_KETTLE, OUTPUT);
 pinMode(RELAY_TOASTER, OUTPUT);


 // default ON
 digitalWrite(RELAY_LAMP, HIGH);
 digitalWrite(RELAY_LAPTOP, HIGH);
 digitalWrite(RELAY_KETTLE, HIGH);
 digitalWrite(RELAY_TOASTER, HIGH);


 ctLamp.current(CT_LAMP, calibration);
 ctKettle.current(CT_KETTLE, calibration);
 ctToaster.current(CT_TOASTER, calibration);
 ctLaptop.current(CT_LAPTOP, calibration);


 setupWiFi();


 client.setServer(mqtt_server, 1883);
 client.setCallback(callback);


 Serial.println("System Ready");
}


void loop()
{
  if (!client.connected())
  {
    reconnect();
  }

  client.loop();

  float voltage = 230.0;

  // Read all CTs
  double lampCurrent    = ctLamp.calcIrms(1480);
  double kettleCurrent  = ctKettle.calcIrms(1480);
  double toasterCurrent = ctToaster.calcIrms(1480);
  double laptopCurrent  = ctLaptop.calcIrms(1480);

  // Noise filter
  if(lampCurrent < 0.10) lampCurrent = 0;
  if(kettleCurrent < 0.10) kettleCurrent = 0;
  if(toasterCurrent < 0.10) toasterCurrent = 0;
  if(laptopCurrent < 0.10) laptopCurrent = 0;

// ==================================
// AGGREGATE NILM INPUT
// ==================================

double aggregateCurrent = kettleCurrent;
float aggregatePower = aggregateCurrent * 230.0;

  // ==================================
  // RELAY STATUS
  // ==================================

  bool lampRelay = (digitalRead(RELAY_LAMP) == HIGH);
  bool laptopRelay = (digitalRead(RELAY_LAPTOP) == HIGH);
  bool kettleRelay = (digitalRead(RELAY_KETTLE) == HIGH);
  bool toasterRelay = (digitalRead(RELAY_TOASTER) == HIGH);

  // ==================================
  // JSON PAYLOAD
  // ==================================

  String payload = "{";

  payload += "\"voltage\":" + String(voltage,2) + ",";

  payload += "\"current\":" +
           String(aggregateCurrent,2) + ",";

  payload += "\"total_power\":" +
           String(aggregatePower,0) + ",";

  payload += "\"relay_lamp\":" +
           String(lampRelay) + ",";

  payload += "\"relay_laptop\":" +
           String(laptopRelay) + ",";

  payload += "\"relay_kettle\":" +
           String(kettleRelay) + ",";

  payload += "\"relay_toaster\":" +
           String(toasterRelay);

  payload += "}";

  client.publish("home/power", payload.c_str());

  Serial.print("Aggregate Current: ");
  Serial.print(aggregateCurrent,2);

  Serial.print(" A | Aggregate Power: ");
  Serial.print(aggregatePower,0);

  Serial.println(" W");

  delay(100);
}
