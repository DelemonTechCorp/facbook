import hashlib

def generate_barrier_token(admin_email, phone_number, created_time):
    """
    Generate a barrier token based on admin's email, phone number, and creation time.
    """
    # Concatenate admin details into a single string
    data_to_hash = f"{admin_email}{phone_number}{created_time}"
    
    # Hash the concatenated string using SHA-256 algorithm
    hashed_token = hashlib.sha256(data_to_hash.encode()).hexdigest()
    
    return hashed_token
