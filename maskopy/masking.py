import re

def mask_email(email):
    """
    Standard email masking for Maskopy local simulation.
    Masks the local part while keeping the first character.
    """
    if not email or '@' not in email:
        return email
    local, domain = email.split('@')
    masked_local = local[0] + '*' * (len(local) - 1) if len(local) > 1 else '*'
    return f"{masked_local}@{domain}"

def mask_phone(phone):
    """
    Standard phone masking for Maskopy local simulation.
    Masks all but the last 4 digits.
    """
    if not phone:
        return phone
    return '*' * (len(phone) - 4) + phone[-4:] if len(phone) > 4 else '****'

def mask_card(card):
    """
    Standard credit card masking for Maskopy local simulation.
    Masks middle digits: 1234-****-****-3456
    """
    if not card:
        return card
    parts = card.split('-')
    if len(parts) == 4:
        return f"{parts[0]}-****-****-{parts[3]}"
    return "****"
