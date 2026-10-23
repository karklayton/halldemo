import bluetooth
from micropython import const
from machine import Pin

# BLE event codes
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_NUS_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_NUS_TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY)
_NUS_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    bluetooth.FLAG_WRITE | bluetooth.FLAG_WRITE_NO_RESPONSE,
)
_SENS_RX = (
    bluetooth.UUID("6E400004-B5A3-F393-E0A9-E50E24DCCA9E"),
    bluetooth.FLAG_WRITE | bluetooth.FLAG_WRITE_NO_RESPONSE,
)
_NUS_SERVICE = (_NUS_UUID, (_NUS_TX, _NUS_RX, _SENS_RX))

NAME = "ESP32-Thing"
led = Pin(13, Pin.OUT)  # blue LED on board

# Pins the "pin" command must never touch:
# 0 = boot mode, 1/3 = USB serial (REPL), 6-11 = internal flash, 34-39 = input only
_BLOCKED_PINS = (0, 1, 3, 6, 7, 8, 9, 10, 11, 34, 35, 36, 37, 38, 39)

ble = bluetooth.BLE()
ble.active(True)

((tx_handle, rx_handle, sens_handle),) = ble.gatts_register_services((_NUS_SERVICE,))

conn = None

MODES = ("pump", "police", "got", "never", "tetris")
mode = "police"
sensitivity = .6


def make_adv():
    # Advertising packet: flags + device name
    name = NAME.encode()
    adv = bytes([2, 0x01, 0x06]) + bytes([len(name) + 1, 0x09]) + name
    # Scan response: 128-bit service UUID (little-endian)
    uuid = bytes(reversed(bytes.fromhex("6E400001B5A3F393E0A9E50E24DCCA9E")))
    resp = bytes([17, 0x07]) + uuid
    return adv, resp


def advertise():
    adv, resp = make_adv()
    ble.gap_advertise(100_000, adv_data=adv, resp_data=resp)
    print("Advertising as", NAME)


def send(text):
    if conn is not None:
        ble.gatts_notify(conn, tx_handle, text.encode())


def handle(msg):
    global mode
    parts = msg.lower().split()  # "pin 27 1" -> ["pin", "27", "1"]
    if not parts:
        return
    cmd, args = parts[0], parts[1:]

    try:
        if cmd == "on":
            led.value(1)
            send("LED on\n")
        elif cmd == "off":
            led.value(0)
            send("LED off\n")
        elif cmd == "pin" and len(args) == 2:  # e.g. "pin 27 1"
            n, v = int(args[0]), int(args[1])
            if n in _BLOCKED_PINS:
                send("Pin %d is not allowed\n" % n)
            else:
                Pin(n, Pin.OUT).value(v)
                send("Pin %d = %d\n" % (n, v))
        elif cmd in MODES:
            mode = cmd
            send("Mode set: " + mode + "\n")
        elif cmd == "help":
            send("Commands: mode <name>, on, off, pin <n> <0|1>, help\n")
        else:
            send("Unknown: " + msg + "\n")
    except Exception as e:
        print("Error: " + str(e) + "\n")
        send("Error: " + str(e) + "\n")

def set_sensitivity(value):
    global sensitivity
    try:
        sensitivity = value
        send("Hall trigger set: " + value + "\n")
    except Exception as e:
        send("Error: " + str(e) + "\n")

def irq(event, data):
    global conn
    if event == _IRQ_CENTRAL_CONNECT:
        conn, _, _ = data
        print("Connected")
    elif event == _IRQ_CENTRAL_DISCONNECT:
        conn = None
        print("Disconnected")
        advertise()
    elif event == _IRQ_GATTS_WRITE:
        _, value_handle = data
        if value_handle == rx_handle:
            msg = ble.gatts_read(rx_handle).decode().strip()
            print("Received:", msg)
            handle(msg)
        elif value_handle == sens_handle:
            msg = ble.gatts_read(sens_handle).decode().strip()
            print("Sensitivity received:", msg)
            set_sensitivity(msg)


def init_ble():
    ble.irq(irq)