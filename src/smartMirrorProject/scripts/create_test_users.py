# This script will create regular Django users and a Django superuser. These users are for testing purposes.
from loginPage.models import User


def run():
    """
    Creates test users for the smart mirror project if they do not already exist.
    """
    test_users = [
        {
            "username": "bart",
            "password": "password123",
            "email": "bart@example.com",
            "first_name": "Bart",
            "last_name": "van de Griendt",
            "nfc_tag_id": "553760008684",
            "nfc_tag_data": "Syrup1-Aching",
        },
        {
            "username": "thorsten",
            "password": "password123",
            "email": "thorsten@example.com",
            "first_name": "Thorsten",
            "last_name": "Hol",
            "nfc_tag_id": "52958068524",
            "nfc_tag_data": "Pureness-Scabbed5",
        },
        {
            "username": "brian",
            "password": "password123",
            "email": "brian@example.com",
            "first_name": "Brian",
            "last_name": "Dreuning",
            "nfc_tag_id": "598485893029",
            "nfc_tag_data": "Rundown-Cozy",
        },
        {
            "username": "darren",
            "password": "password123",
            "email": "darren@example.com",
            "first_name": "Darren",
            "last_name": "Samuels",
            "nfc_tag_id": "658087044303",
            "nfc_tag_data": "Tiger3-Perjurer",
        },
    ]

    for user_data in test_users:
        if not User.objects.filter(username=user_data["username"]).exists():
            User.objects.create_user(
                username=user_data["username"],
                password=user_data["password"],
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                nfc_tag_id=user_data["nfc_tag_id"],
                nfc_tag_data=user_data["nfc_tag_data"],
            )
            print(f"{user_data['username']} created")
        else:
            print(f"{user_data['username']} already exists")

    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            password="adminpassword123",
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            nfc_tag_id="658087044303",
            nfc_tag_data="!Q@W#E$R%T",
        )
        print("admin created")
    else:
        print("admin already exists")
