from assign_rights.models import User
from django.contrib.auth.models import Group

if not User.objects.filter(username="test").exists():
    print("Creating user")
    User.objects.create_user("test", "test@example.com", "testpassword")
    user = User.objects.get(username='test')
    group = Group.objects.get(name='edit')
    user.groups.add(group)
