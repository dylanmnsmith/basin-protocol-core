import hashlib, sys, os
REQUIRED_HASH = "55aee5640f46a9ec386598482abf683940a64d8004a8769a511b85be0c084127"
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
