import torch
import hashlib
import struct
import io

def banner(text):
    print(f"\n{'='*40}\n{text}\n{'='*40}")

def get_model_checksum(model):
    """
    Extracts a Basin-compliant checksum of the model weights.
    It serializes the weights into a byte buffer and hashes them.
    """
    buffer = io.BytesIO()
    # We iterate nicely to ensure order is deterministic
    for name, param in sorted(model.named_parameters()):
        # We access the raw underlying data
        data = param.data.cpu().numpy()
        # We write the bytes of the array directly
        buffer.write(data.tobytes())
    
    buffer.seek(0)
    return hashlib.sha256(buffer.read()).hexdigest()

def run_xen_proof():
    banner("MISSION 1.2: XEN INTEGRITY PROOF (DYNAMIC STATE)")

    # 1. Initialization (The Genesis State)
    # We force a seed. If the seed controls the chaos, the chaos is a ladder.
    torch.manual_seed(70627)  # Using your ID as the seed for poetic signature
    
    # Simple Perceptron (The "Brain")
    # Input: 784 (MNIST size), Output: 10
    model = torch.nn.Linear(784, 10)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    
    genesis_hash = get_model_checksum(model)
    print(f"[*] Genesis State Hash: {genesis_hash[:16]}...")

    # 2. The Input (The "Experience")
    # specific synthetic data
    inputs = torch.randn(1, 784)
    targets = torch.randn(1, 10) # Dummy target
    
    # 3. The Computation (The "Learning")
    print("[*] Executing Forward/Backward Pass (Training Step)...")
    
    # Forward
    outputs = model(inputs)
    loss = torch.nn.functional.mse_loss(outputs, targets)
    
    # Backward
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    # 4. The Result (The New State)
    state_t1_hash = get_model_checksum(model)
    print(f"[*] State T1 Hash:      {state_t1_hash[:16]}...")
    
    if genesis_hash == state_t1_hash:
        print("[!] FAIL: Weights did not update. Learning failed.")
        exit(1)

    # 5. Verification: The Time Loop (Reproducibility)
    # We reset EVERYTHING and try to reach T1 again. 
    # If we miss by a single bit, the protocol is invalid.
    print("[*] Verifying Causal Link (Re-running simulation)...")
    
    torch.manual_seed(70627)
    model_verify = torch.nn.Linear(784, 10)
    optimizer_verify = torch.optim.SGD(model_verify.parameters(), lr=0.01)
    
    # Same data
    inputs_v = inputs # Reusing the tensor to simulate 'exact same data input'
    targets_v = targets
    
    outputs_v = model_verify(inputs_v)
    loss_v = torch.nn.functional.mse_loss(outputs_v, targets_v)
    
    optimizer_verify.zero_grad()
    loss_v.backward()
    optimizer_verify.step()
    
    verify_hash = get_model_checksum(model_verify)
    print(f"[*] Verify State Hash:    {verify_hash[:16]}...")
    
    if verify_hash == state_t1_hash:
        print("[+] PASS: Causal Integrity Verified. Computation is deterministic.")
    else:
        print("[!] CRITICAL FAIL: Divergence detected.")
        print(f"Expected: {state_t1_hash}")
        print(f"Got:      {verify_hash}")
        exit(1)

    banner("PROOF 1.2 COMPLETE: DYNAMIC INVARIANT HOLDS")

if __name__ == "__main__":
    run_xen_proof()
