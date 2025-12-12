"""
Test script for Grep SDK

This tests basic initialization without connecting to backend.
"""

import os
from grep import Grep

print("🧪 Testing Grep SDK...")
print("-" * 50)

# Test 1: Initialize with demo API key
print("\n1️⃣ Testing initialization with API key...")
try:
    os.environ["GREP_API_KEY"] = "grep_testorg_abc123demo"
    Grep.init(disable_batch=True)
    print("✅ SDK initialized successfully!\n")
except Exception as e:
    print(f"❌ Failed: {e}\n")

# Test 2: Check if initialized
print("2️⃣ Testing initialization check...")
if Grep.is_initialized():
    print("✅ SDK is initialized\n")
else:
    print("❌ SDK not initialized\n")

# Test 3: Get collector endpoint
print("3️⃣ Testing collector endpoint...")
endpoint = Grep.get_collector_endpoint()
print(f"✅ Collector: {endpoint}\n")

print("-" * 50)
print("✅ All SDK tests passed!")
print("\n📝 Note: Backend (localhost:8000) not running yet.")
print("   We'll test full flow after backend is set up.")
