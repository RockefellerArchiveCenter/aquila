from assign_rights.models import User

if not User.objects.filter(username="test").exists():
    print("Creating user")
    User.objects.create_user("test", "test@example.com", "testpassword")
