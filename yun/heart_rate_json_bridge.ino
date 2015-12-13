#include <Bridge.h>
#include <BridgeServer.h>
#include <BridgeClient.h>

/**
   Constants.
*/
#define POOL_SIZE 20
#define ABSENCE_TIMEOUT 1500
#define MIN_HB_INTERVAL 350
#define MAX_HB_INTERVAL 1200
#define COLLECTING_DATA 1
#define REPORTING_DATA 2
#define SOURCE_ABSENT 0

/**
   Global variables.
*/
int POOL_INDEX = 0;
double POOL[POOL_SIZE];
long last_heart_beat = millis();
long this_heart_beat = millis();
int state = SOURCE_ABSENT;
double hr = 0.0;

void init_pool() {
    for (int i = 0; i < POOL_SIZE; i++) {
        POOL[i] = (double) 0.0;
    }
}

void inter() {
    // update heart beat time
    last_heart_beat = this_heart_beat;
    this_heart_beat = millis();
    if (last_heart_beat > 0 && this_heart_beat > 0) {
        long interval = this_heart_beat - last_heart_beat;
        if (interval < MAX_HB_INTERVAL && interval > MIN_HB_INTERVAL) {
            POOL[POOL_INDEX++] = (this_heart_beat - last_heart_beat) / 1000.0;
            if (POOL_INDEX >= POOL_SIZE) POOL_INDEX = 0;
            hr = 60.0 / cacl();
            if (hr < 0) state = COLLECTING_DATA;
            else state = REPORTING_DATA;
        }
    }
}

void pp() {
    Serial.print("[");
    for (int i = 0; i < POOL_SIZE; i++) {
        Serial.print(POOL[i]);
        Serial.print(", ");
    }
    Serial.println("]");
}

void pa() {
    Serial.print("State: ");
    Serial.println(state);
    Serial.print("HR: ");
    Serial.println(hr);
    pp();
}

double cacl() {
    double sum = 0;
    for (int i = 0; i < POOL_SIZE; i++) {
        if (POOL[i] == 0) return -1.0;
        sum += POOL[i];
    }
    return sum / (double) POOL_SIZE;
}

// Listen to the default port 5555, the Yún webserver
// will forward there all the HTTP requests you send
BridgeServer server;

// Print the header for a success JSON reponse
void print_suc_resp_header(BridgeClient *client) {
    client->println("Status: 200");
    client->println("Content-type: application/json");
    client->println("Access-Control-Allow-Origin: *");
    client->println();
}

void process_command(BridgeClient *client) {
    // read the command
    String command = client->readStringUntil('/');

    // is "digital" command?
    if (command != "hr") {
        print_suc_resp_header(client);
        client->print("{ \"state\": ");
        client->print(state);
        client->print(", \"hr\": ");
        client->print(hr);
        client->print("}");
    }
}

void setup() {
    Serial.begin(9600);
    init_pool();
    attachInterrupt(digitalPinToInterrupt(2), inter, RISING);
    Bridge.begin();
    server.listenOnLocalhost();
    server.begin();
}

void loop() {
    // Get clients coming from server
    BridgeClient client = server.accept();

    // There is a new client?
    if (client) {
        // Process requests
        process_command(&client);

        // Close connection and free resources.
        client.stop();
    }
    if (millis() - this_heart_beat > ABSENCE_TIMEOUT) {
        state = SOURCE_ABSENT;
        init_pool();
        hr = 0;
    }
    pa();
}
