import RPi.GPIO as GPIO
import time
import requests

BUTTON_PIN = 11  # physical pin number (BOARD numbering)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

WLED_IP="10.42.0.142"
LOUD_PLAYLIST_ID = 26
QUIET_PLAYLIST_ID = 25


def set_playlist(playlist_id: int):
    """Tell WLED to start the given playlist id."""
    try:
        # Switch playlist
        requests.post(
            f"http://{WLED_IP}/json/state",
            json={"ps": playlist_id}
        )

        # Next Preset
        requests.post(
            f"http://{WLED_IP}/json/state",
            json={"np": True}
        )

    except requests.RequestException as exc:
        print("Failed to set WLED playlist %s: %s", playlist_id, exc)


# Locally tracked toggle state
state = {"next": LOUD_PLAYLIST_ID}

def on_press():
    playlist_to_set = state["next"]

    set_playlist(playlist_to_set)
    
    # flip which one we'll set next time, regardless of success/failure
    state["next"] = LOUD_PLAYLIST_ID if playlist_to_set == QUIET_PLAYLIST_ID else QUIET_PLAYLIST_ID

print("Waiting for button press (Ctrl+Z to exit)...")
try:
    while True:
        # Falling edge = button pressed (pin pulled to GND)
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING, bouncetime=200)
        print("Button pressed!")
        on_press()

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()