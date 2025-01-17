from django.http import JsonResponse
import json
import threading

nfc_lock = threading.Lock()


def checkIfPi(request=None):
    """
    Check if the current device is a Raspberry Pi.

    This function attempts to read the device model from the file
    "/proc/device-tree/model".

    Args:
        request: Optional; the HTTP request object (default is None).

    Returns:
        JsonResponse: A JSON response with a key "is_raspberry_pi"
        set to True if the device is a Raspberry Pi, otherwise False.
    """
    try:
        with open("/proc/device-tree/model", "r") as model_file:
            model = model_file.read().strip().lower()
            if "raspberry pi" in model:
                return JsonResponse({"is_raspberry_pi": True})
    except FileNotFoundError:
        return JsonResponse({"is_raspberry_pi": False})


# Only import NFC related packages if app is ran on a Raspberry Pi
response = checkIfPi()
isPi = json.loads(response.content)["is_raspberry_pi"]
if isPi:
    import RPi.GPIO as GPIO
    from mfrc522 import SimpleMFRC522


def fetchNfcTag(request):
    """
    Fetches NFC tag data using an NFC reader. This function attempts to read an NFC tag using
    the NFC reader.
    Returns:
        JsonResponse: A JSON response containing the tag ID and formatted tag data, or an error
        message if an exception occurs.
    """
    tagId = None
    tagData = None
    try:
        with nfc_lock:
            import RPi.GPIO as GPIO
            from mfrc522 import SimpleMFRC522

            reader = SimpleMFRC522()
            tagId, tagData = reader.read()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    finally:
        GPIO.cleanup()
    tagData = formatNfcData(tagData)
    return JsonResponse({"tagId": tagId, "tagData": tagData})


def writeNfcTag(request, data):
    """
    Writes data to an NFC tag and returns the tag ID and written data in a JSON response.
    Args:
        data (str): The data to be written to the NFC tag.
    Returns:
        JsonResponse: A JSON response containing the tag ID and written data if successful, or an
        error message if an exception occurs.
    """
    try:
        with nfc_lock:
            import RPi.GPIO as GPIO
            from mfrc522 import SimpleMFRC522

            reader = SimpleMFRC522()
            reader.write(data)
            tagId = reader.read_id()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    finally:
        GPIO.cleanup()
    return JsonResponse({"tagId": tagId, "writtenData": data})


def formatNfcData(data: str):
    """
    Formats the given NFC data by stripping leading and trailing whitespace.
    Future enhancements can be added to this function as needed.
    Args:
        data (str): The NFC data to be formatted.
    Returns:
        str: The formatted NFC data with leading and trailing whitespace removed.
    """
    return data.strip()
