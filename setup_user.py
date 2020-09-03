from assign_rights.models import User

if len(User.objects.all()) == 0:
    print("Creating user")
    User.objects.create_user("test", "test@example.com", "testpassword")

