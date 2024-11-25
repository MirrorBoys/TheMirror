"""
This is a quick Proof Of Concept (POC) for writing to an NFC tag. Follow these steps to use/test it:

1. Connect the NFC reader according to the instructions (https://github.com/MirrorBoys/TheMirror/blob/main/docs/HARDWARE.md#nfc-card-reader) in the repository.
2. Run this code
"""

from mfrc522 import SimpleMFRC522

import RPi.GPIO as GPIO

reader = SimpleMFRC522()

try:
    text_to_write = input("Enter new data to write to the tag: ")
    print("Now place your tag to write")
    reader.write(text_to_write)
    print("Data written to the tag successfully")
finally:
    GPIO.cleanup()
