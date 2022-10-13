# assign_rights/context_processors.py

from django.conf import settings


def mtm_id(request):
    return {'mtm_id': settings.MTM_ID}
