from loginPage.models import User


def run():
    if not User.objects.filter(username="testuser").exists():
        User.objects.create_user(
            username="testuser",
            password="password123",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            nfc_tag_id="553760008684",
            nfc_tag_data="^Y&U*I(O)P",
        )
        print("testuser created")
    else:
        print("testuser already exists")

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
