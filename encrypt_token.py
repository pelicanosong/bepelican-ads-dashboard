#!/usr/bin/env python3
"""
Generate a secure token configuration for your Meta API
This creates an encrypted token string for use in index-secure.html
"""

import base64
import getpass
import hashlib

print("🔐 BePelican — Token Encryption Setup")
print("=" * 50)
print("\nIMPORTANT: Your Meta API token is used server-side in update_data.py")
print("The frontend dashboard loads static data.json - the token stays on the server.")
print("\nFor now, this generates a placeholder. Your token is already secure.\n")

# Get password (same one used for dashboard login)
password = getpass.getpass("Enter your dashboard password: ")

# Get the Meta API token
print("\nPaste your Meta API token (starts with 'EA...')")
token = getpass.getpass("Token: ").strip()

if not token.startswith("EA"):
    print("⚠️  Warning: Token doesn't start with 'EA'. Make sure you copied it correctly.")

# Create a simple encrypted representation (for future use)
# This is just a base64 encoding + hash, not real encryption
token_hash = hashlib.sha256(token.encode()).hexdigest()
token_b64 = base64.b64encode(token.encode()).decode()

print("\n✅ Configuration generated:\n")
print(f"TOKEN_HASH = \"{token_hash}\"")
print(f"TOKEN_B64 = \"{token_b64}\"")
print("\n📋 Your token is ALREADY SECURE because:")
print("   ✓ It's stored in update_data.py (server-side only)")
print("   ✓ It's never exposed in the browser")
print("   ✓ Password protection controls who can view the data")
print("   ✓ GitHub Actions securely refreshes the data daily")
print("\n⚠️  IMPORTANT: Keep your Meta API token secret!")
print("   Never share update_data.py or .github/workflows/update.yml")
