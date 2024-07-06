import random
import string


def generate_id(n):
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))
