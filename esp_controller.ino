#include <WiFi.h>
#include <WebServer.h>

// Wi-Fi credentials
const char* ssid = "akash";
const char* password = "123456789";

// LED pin (GPIO 2)
const int ledPin = 2;

// Brightness value (0 to 255)
int brightness = 128;

WebServer server(80);

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWi-Fi connected.");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());

//  const int MIN_BRIGHTNESS = 20;  // Never go below this value

  
  // Setup LED PWM
  ledcAttachPin(ledPin, 0);      // Attach LED pin to channel 0
  ledcSetup(0, 5000, 8);         // 5 kHz PWM, 8-bit resolution
  ledcWrite(0, brightness);      // Initial brightness

  // === Instant ON ===
  server.on("/fist_open", []() {
    brightness = 100;
    ledcWrite(0, brightness);  // Instant change
    server.send(200, "text/plain", "LED FULL ON");
    Serial.println("Gesture: Fist Open → LED FULL ON");
  });

  // === Instant OFF ===
  server.on("/fist_close", []() {
    brightness = 0;
    ledcWrite(0, brightness);  // Instant change
    server.send(200, "text/plain", "LED OFF");
    Serial.println("Gesture: Fist Closed → LED OFF");
  });

  // === Smooth Increase ===
  server.on("/thumbs_up", []() {
    fadeTo(min(brightness + 50, 255));  // Gradual fade up
    server.send(200, "text/plain", "Brightness Increased");
    Serial.println("Gesture: Thumbs Up → Brightness +");
  });

  server.on("/thumbs_down", []() {
    brightness = max(brightness - 50, 0);
    ledcWrite(0, brightness);
    server.send(200, "text/plain", "Brightness Decreased");
    Serial.println("Gesture: Thumbs Down → - Brightness");
  });


  server.begin();
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("HTTP Server started.");
}

void loop() {
  server.handleClient();

}
