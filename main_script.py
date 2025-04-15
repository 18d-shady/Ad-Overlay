import os
import time
import cv2
import numpy as np
import pyaudio
import threading
import paho.mqtt.client as mqtt

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Ad settings
AD_FOLDER = "ads"
AD_CHANGE_INTERVAL = 10

# HDMI capture device
VIDEO_DEVICE = 0

# MQTT settings
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "/overlay/toggle"

# Global flag to control ad display
ads_enabled = True


def load_ads():
    ads = []
    try:
        for img_file in os.listdir(AD_FOLDER):
            if img_file.endswith((".png", ".jpg")):
                img_path = os.path.join(AD_FOLDER, img_file)
                ad_image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
                if ad_image is not None:
                    target_width = SCREEN_WIDTH // 4
                    aspect_ratio = ad_image.shape[0] / ad_image.shape[1]
                    target_height = int(target_width * aspect_ratio)
                    ad_image = cv2.resize(ad_image, (target_width, target_height))

                    if ad_image.shape[2] == 3:
                        ad_image = cv2.cvtColor(ad_image, cv2.COLOR_BGR2BGRA)
                    ads.append(ad_image)
    except Exception as e:
        print(f"Error loading ads: {e}")
    return ads


def play_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, frames_per_buffer=1024)
    while True:
        data = stream.read(1024)
        stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()


def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    global ads_enabled
    message = msg.payload.decode().strip().lower()
    print(f"MQTT message received: {message}")
    if message == "turn_on":
        ads_enabled = True
    elif message == "turn_off":
        ads_enabled = False


def mqtt_listener():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()


def main():
    global ads_enabled

    ad_images = load_ads()
    if not ad_images:
        print("No ads found in the ads folder. Exiting...")
        return

    current_ad_index = 0
    last_ad_change_time = time.time()

    # Start audio in a separate thread
    audio_thread = threading.Thread(target=play_audio, daemon=True)
    audio_thread.start()

    # Start MQTT listener in a separate thread
    mqtt_thread = threading.Thread(target=mqtt_listener, daemon=True)
    mqtt_thread.start()

    cap = cv2.VideoCapture(VIDEO_DEVICE)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture video")
            break

        if ads_enabled:
            ad_image = ad_images[current_ad_index]
            ad_height, ad_width = ad_image.shape[:2]
            y_offset = 0
            x_offset = frame.shape[1] - ad_width

            for c in range(0, 3):
                frame[y_offset:y_offset + ad_height, x_offset:x_offset + ad_width, c] = \
                    ad_image[:, :, c] * (ad_image[:, :, 3] / 255.0) + \
                    frame[y_offset:y_offset + ad_height, x_offset:x_offset + ad_width, c] * (1.0 - ad_image[:, :, 3] / 255.0)

            current_time = time.time()
            if current_time - last_ad_change_time >= AD_CHANGE_INTERVAL:
                current_ad_index = (current_ad_index + 1) % len(ad_images)
                last_ad_change_time = current_time

        cv2.imshow("IPTV with Ads", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
