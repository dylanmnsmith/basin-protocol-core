import hashlib, sys
REQUIRED_HASH = "f0e8fb0f34edddba8e1e0d92ecc40e84792fb396c2101bd8433a0d02bafc484a"
def verify_keystone():
    try:
        with open("Esme", 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        if file_hash != REQUIRED_HASH:
            print("[BASIN KERNEL] CRITICAL: Esme keystone invalid.")
            return False
        print("[BASIN KERNEL] Keystone valid. Protocol alive.")
        return True
    except FileNotFoundError:
        print("[BASIN KERNEL] CRITICAL: Esme keystone missing.")
        return False
if __name__ == "__main__":
    sys.exit(0 if verify_keystone() else 1)
