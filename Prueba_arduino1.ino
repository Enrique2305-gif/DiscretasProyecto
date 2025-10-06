const int sensorEntrada = 2;  // Pin del sensor de entrada
const int sensorSalida = 3;   // Pin del sensor de salida
const int motorPin1 = 8;      // Pin 1 del L293D
const int motorPin2 = 9;      // Pin 2 del L293D
int contadorAutos = 0;
const int maxAutos = 14;

void setup() {
  pinMode(sensorEntrada, INPUT);
  pinMode(sensorSalida, INPUT);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
}

void loop() {
  if (digitalRead(sensorEntrada) == HIGH && contadorAutos < maxAutos) {
    contadorAutos++;
  }
  if (digitalRead(sensorSalida) == HIGH && contadorAutos > 0) {
    contadorAutos--;
  }

  if (contadorAutos >= maxAutos) {
    // Cerrar puerta
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, HIGH);
  } else {
    // Abrir puerta
    digitalWrite(motorPin1, HIGH);
    digitalWrite(motorPin2, LOW);
  }
}
