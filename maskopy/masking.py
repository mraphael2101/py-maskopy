import hashlib
import random
import datetime

def mask_email(email):
    """
    Masks the local part of an email address while keeping the first character visible.
    
    Example:
    'john.doe@example.com' -> 'j*******@example.com'
    
    Args:
        email (str): The original email address to be masked.
        
    Returns:
        str: The masked email address.
    """
    if not email or '@' not in email:
        return email
    local, domain = email.split('@')
    masked_local = local[0] + '*' * (len(local) - 1) if len(local) > 1 else '*'
    return f"{masked_local}@{domain}"

def mask_phone(phone):
    """
    Masks all characters of a phone number except for the last 4 digits.
    
    Example:
    '555-0101' -> '****0101'
    
    Args:
        phone (str): The original phone number to be masked.
        
    Returns:
        str: The masked phone number.
    """
    if not phone:
        return phone
    return '*' * (len(phone) - 4) + phone[-4:] if len(phone) > 4 else '****'

def mask_card(card):
    """
    Masks the middle digits of a credit card number in 'XXXX-XXXX-XXXX-XXXX' format.
    
    Example:
    '1234-5678-9012-3456' -> '1234-****-****-3456'
    
    Args:
        card (str): The original credit card number to be masked.
        
    Returns:
        str: The masked credit card number.
    """
    if not card:
        return card
    parts = card.split('-')
    if len(parts) == 4:
        return f"{parts[0]}-****-****-{parts[3]}"
    return "****"

# --- ADVANCED MASKOPY-INSPIRED METHODS ---

def mask_hash(value, salt="maskopy-salt"):
    """
    Performs deterministic hashing (SHA-256) on a value.
    This ensures the SAME input ALWAYS results in the SAME masked output,
    which is essential for maintaining relationships across different tables/databases.
    
    Example:
    '12345' -> 'a5d1... (hashed hex)'
    
    Args:
        value (str): The value to hash.
        salt (str): Optional salt to make the hash unique to the project.
        
    Returns:
        str: The first 12 characters of the hash in hexadecimal.
    """
    if not value:
        return value
    salted_value = f"{value}{salt}".encode('utf-8')
    return hashlib.sha256(salted_value).hexdigest()[:12]

def mask_date_shift(date_str, days_range=10, seed=None):
    """
    Randomly shifts a date by a certain number of days (positive or negative).
    This keeps the data 'realistic' (e.g., a birthday stays a birthday) but obfuscates the exact date.
    
    Example:
    '1990-05-20' -> '1990-05-15' (shifted by -5 days)
    
    Args:
        date_str (str): The original date in 'YYYY-MM-DD' format.
        days_range (int): The maximum number of days to shift by.
        seed (any): Optional seed for deterministic (reproducible) shifting.
        
    Returns:
        str: The shifted date in 'YYYY-MM-DD' format.
    """
    if not date_str:
        return date_str
    try:
        dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        if seed is not None:
            random.seed(str(seed))
        shift = random.randint(-days_range, days_range)
        shifted_dt = dt + datetime.timedelta(days=shift)
        return shifted_dt.strftime('%Y-%m-%d')
    except ValueError:
        return date_str

def mask_lookup(value, lookup_type='name'):
    """
    Replaces a sensitive value with a random entry from a lookup list of 'safe' values.
    This provides high-quality test data that looks completely real.
    
    Example:
    'John Doe' -> 'Michael Scott' (lookup replacement)
    
    Args:
        value (str): The original value.
        lookup_type (str): The type of lookup to perform ('name', 'city', 'company').
        
    Returns:
        str: A fake but realistic value.
    """
    lookups = {
        'name': ['Michael Scott', 'Jim Halpert', 'Pam Beesly', 'Dwight Schrute', 'Angela Martin'],
        'city': ['Scranton', 'New York', 'Stamford', 'Nashua', 'Tallahassee'],
        'company': ['Dunder Mifflin', 'Wernham Hogg', 'Saber', 'Prince Family Paper']
    }
    choices = lookups.get(lookup_type, ['Unknown'])
    # Deterministic choice based on the original value's hash
    idx = int(hashlib.md5(value.encode('utf-8')).hexdigest(), 16) % len(choices)
    return choices[idx]

def mask_scrub(value):
    """
    Completely removes/redacts a value. Used for data that is too sensitive to keep in any form.
    
    Example:
    'Secret Password' -> '[REDACTED]'
    
    Args:
        value (str): The original value.
        
    Returns:
        str: '[REDACTED]'
    """
    return "[REDACTED]"

def mask_fpe(value):
    """
    Simulates Format-Preserving Encryption (FPE).
    This keeps the data's length and character type (e.g., preserving dashes) but replaces
    characters with pseudo-random ones from the same set.
    
    Example:
    'ABC-123' -> 'X-Y-Z-0-1-2' (simulation)
    
    Args:
        value (str): The value to encrypt.
        
    Returns:
        str: A character-for-character replacement string.
    """
    if not value:
        return value
    result = []
    for char in str(value):
        if char.isdigit():
            result.append(str(random.randint(0, 9)))
        elif char.isalpha():
            result.append(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        else:
            result.append(char)
    return "".join(result)
