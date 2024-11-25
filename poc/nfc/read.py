"""
This is a quick Proof Of Concept (POC) for reading an NFC tag. Follow these steps to use/test it:

1. Connect the NFC reader according to the instructions (https://github.com/MirrorBoys/TheMirror/blob/main/docs/HARDWARE.md#nfc-card-reader) in the repository.
2. Run this code
"""

from mfrc522 import SimpleMFRC522

import RPi.GPIO as GPIO

reader = SimpleMFRC522()

try:
    print("Hold a tag near the reader")
    id, text = reader.read()
    print(f"ID: {id}")
    print(f"Text: {text}")
finally:
    GPIO.cleanup()
