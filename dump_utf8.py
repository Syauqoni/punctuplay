import json
from django.core.management import call_command

with open("data.json", "w", encoding="utf-8") as f:
    call_command(
        "dumpdata",
        exclude=["auth.permission", "contenttypes"],
        stdout=f
    )
