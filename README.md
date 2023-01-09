# S7-protocol-example

# Table of Contents
1. [Overview](README.md#Overview)
2. [Installation](README.md#installation)
2. [Run instructions](README.md#run-instructions)

## 1 Overview
This is a simple example of a Server and Client S7 server.

We assume the server is running on a Cooling Machine. When the machine is OFF, the temperature rises (up to a maximum of 20). When the machine is ON, the temperature decreases (down to a minimum of 0). The machine doesn't do any kind of regulation, can only be turned ON or OFF.
The regulation of the temperature is done on the client side, by trying to keep it in a band of 2 degrees around the setpoint:
   - when the temperature is 2 degress lower than the setpoint, the client sends the OFF command to the machine
   - when the temperature is 2 degrees higher then the setpoint, the client sends the ON command to the machine

## 2 Installation
### 2.1 Clone repository

```
git clone git@github.com:shiflux/S7-protocol-example.git
```

### 2.2 Install python requirements

```
cd S7-protocol-example
pip3 install -r requirements.txt
```

## 3 Run instructions
### 3.1 Run server

```
python3 server.py
```

### 3.2 Run client

```
python3 client.py
```