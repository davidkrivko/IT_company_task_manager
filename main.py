from django.contrib.auth import get_user_model

get_user_model().objects.create_user(
    username="asdffsfdfs",
    password="12345678",
    position_id=1,
)
