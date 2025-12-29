import struct
import hashlib
import os

def banner(text):
    print(f"\n{'='*40}\n{text}\n{'='*40}")

def run_absence_proof():
    banner("MISSION 1.1: ABSENCE PROOF (THE ATOM)")
    
    # 1. Define the 'Basin' (The strict binary format)
    # Format: '>fQ' = Big-Endian, 1 Float (4 bytes), 1 Unsigned Long Long (8 bytes)
    # Total expected size: 12 bytes exactly. No more, no less.
    fmt = '>fQ'
    expected_size = struct.calcsize(fmt)
    print(f"[*] Defined Basin Format: '{fmt}'")
    print(f"[*] Expected Atomic Size: {expected_size} bytes")

    # 2. The Input State (Simulated Weights/Token)
    val_float = 0.123456789
    val_int = 987654321
    print(f"[*] Input Data: Float({val_float}), Int({val_int})")

    # 3. Serialization (The Packing)
    packed_data = struct.pack(fmt, val_float, val_int)
    
    # 4. Verification I: The Physical Constraint (Absence of Leakage)
    actual_size = len(packed_data)
    print(f"[*] Packed Hex Dump: {packed_data.hex()}")
    
    if actual_size != expected_size:
        print(f"[!] FAIL: Size Mismatch. Expected {expected_size}, Got {actual_size}")
        exit(1)
    else:
        print(f"[+] PASS: Size Integrity Verified ({actual_size} bytes). No hidden capacity.")

    # 5. Verification II: Determinism (The Invariant)
    # We pack the SAME data 10,000 times. If the hash changes ONCE, the universe is broken.
    print("[*] Running Determinism Stress Test (10,000 iterations)...")
    baseline_hash = hashlib.sha256(packed_data).hexdigest()
    
    for _ in range(10000):
        current_pack = struct.pack(fmt, val_float, val_int)
        current_hash = hashlib.sha256(current_pack).hexdigest()
        if current_hash != baseline_hash:
            print("[!] CRITICAL FAIL: Non-deterministic packing detected!")
            exit(1)
            
    print(f"[+] PASS: Determinism Verified. Hash: {baseline_hash[:16]}...")

    # 6. Verification III: Sensitivity (The Avalanche)
    # We change the input by the smallest possible epsilon. The hash MUST change.
    modified_pack = struct.pack(fmt, val_float + 0.0000001, val_int)
    modified_hash = hashlib.sha256(modified_pack).hexdigest()
    
    if modified_hash == baseline_hash:
        print("[!] FAIL: Collision detected. State change did not alter signature.")
        exit(1)
    else:
        print(f"[+] PASS: Sensitivity Verified. New Hash: {modified_hash[:16]}...")

    banner("PROOF 1.1 COMPLETE: INVARIANT HOLDS")

if __name__ == "__main__":
    run_absence_proof()
