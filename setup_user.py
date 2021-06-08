from aquila import config
from assign_rights.models import User

if not User.objects.filter(username=config.SUPERUSER_USERNAME).exists():
    user = User.objects.create_superuser(config.SUPERUSER_USERNAME, config.SUPERUSER_EMAIL, "testpassword")
