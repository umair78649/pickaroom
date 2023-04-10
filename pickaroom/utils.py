from django.utils.crypto import get_random_string
import string


def generate_reference_no():
    return get_random_string(length=10, allowed_chars=string.ascii_uppercase)
