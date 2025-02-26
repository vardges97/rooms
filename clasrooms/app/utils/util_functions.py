import secrets
import string
import json

def generate_api_key(num_keys=20, key_length=32, restrictions=None):
    """
    Generate API keys with optional restrictions.

    Args:
        num_keys (int): Number of keys to generate.
        key_length (int): Length of each API key.
        restrictions (dict): Dictionary of restrictions to assign to keys.

    Returns:
        dict: A dictionary of API keys and their associated restrictions.
    """
    keys = {}
    for _ in range(num_keys):
        # Generate a random API key
        key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(key_length))
        
        # Assign restrictions if provided
        keys[key] = restrictions if restrictions else {}

    return keys

def save_keys_to_file(keys, filename="api_keys.json"):
    """
    Save API keys to a file in JSON format.

    Args:
        keys (dict): API keys and their restrictions.
        filename (str): File name to save the keys.
    """
    with open(filename, "w") as file:
        json.dump(keys, file, indent=4)
    print(f"API keys saved to {filename}")

# # Example usage
# if __name__ == "__main__":
#     # Define restrictions (optional)
#     restrictions_example = {
#         "usage_limit": 1000,  # Max API calls
#         "valid_until": "2025-12-31"  # Expiration date
#     }

#     # Generate 20 API keys with restrictions
#     api_keys = generate_api_key(num_keys=20, key_length=40, restrictions=restrictions_example)

#     # Save to a file
#     save_keys_to_file(api_keys)
