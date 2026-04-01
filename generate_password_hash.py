#!/usr/bin/env python3
"""
Generate SHA-256 hash for your dashboard password
Run this to create a secure password hash for index-secure.html
"""

import hashlib
import getpass

print("🔐 BePelican — Password Hash Generator")
print("=" * 50)
print("\nThis generates a SHA-256 hash of your password.")
print("Use this hash in index-secure.html for secure authentication.\n")

password = getpass.getpass("Enter your dashboard password: ")
confirm = getpass.getpass("Confirm password: ")

if password != confirm:
    print("❌ Passwords do not match!")
    exit(1)

# Generate SHA-256 hash
password_hash = hashlib.sha256(password.encode()).hexdigest()

print("\n✅ Password hash generated:\n")
print(f"PASSWORD_HASH = \"{password_hash}\"")
print("\n📋 Copy the hash above and paste it in index-secure.html at line ~180")
print("Replace: PASSWORD_HASH = \"...\"")
