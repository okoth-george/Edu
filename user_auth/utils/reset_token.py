from django.core.cache import cache
import random

def generate_reset_token(user_id):
    token = ''.join(random.choices("0123456789", k=6))  # 6-digit
    cache.set(f"reset_token_{user_id}", token, timeout=300)  # 10 min expiry
    return token

def verify_reset_token(user_id, token):
    saved_token = cache.get(f"reset_token_{user_id}")
    return saved_token == token
