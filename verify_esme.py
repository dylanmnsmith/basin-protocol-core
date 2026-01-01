import hashlib, sys
REQUIRED_HASH = "f0e8fb0f34edddba8e1e0d92ecc40e84792fb396c2101bd8433a0d02bafc484a"
def check():
    try:
        with open("Esme", 'rb') as f: h = hashlib.sha256(f.read()).hexdigest()
        return h == REQUIRED_HASH
    except: return False
if not check(): print("FATAL: Esme keystone invalid."); sys.exit(1)
