from aquila import settings
from assign_rights.models import User

if not User.objects.filter(username=settings.SUPERUSER_USERNAME).exists():
    user = User.objects.create_superuser(settings.SUPERUSER_USERNAME, settings.SUPERUSER_EMAIL, "testpassword")
