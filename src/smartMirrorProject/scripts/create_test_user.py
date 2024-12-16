from django.contrib.auth.models import User


def run():
    if not User.objects.filter(username="testuser").exists():
        User.objects.create_user(
            username="testuser",
            password="password123",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
        )
        print("Testgebruiker created")
    else:
        print("Testgebruiker already exists")
