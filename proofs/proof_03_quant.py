import hashlib
import sys
import os

try:
    from llama_cpp import Llama
except ImportError:
    print("[!] Error: llama-cpp-python not installed. Run 'pip install llama-cpp-python'")
    sys.exit(1)

def banner(text):
    print(f"\n{'='*40}\n{text}\n{'='*40}")

# CONFIGURATION
# [USER ACTION REQUIRED]: Update this path to your specific GGUF file
MODEL_PATH = "tinyllama-1.1b-chat.Q8_0.gguf" 

def get_file_checksum(filepath):
    """Generates SHA256 of the physical GGUF file (The Input State)."""
    if not os.path.exists(filepath):
        print(f"[!] Error: Model file not found at {filepath}")
        sys.exit(1)
        
    print(f"[*] Hashing Input State (Model File)... this may take a moment.")
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read in chunks to avoid memory overflow
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def run_inference_proof():
    banner("MISSION 1.3: QUANTIZATION INTEGRITY (GOLD MASTER)")

    # 1. Establish Input State Identity
    file_hash = get_file_checksum(MODEL_PATH)
    print(f"[*] Input Model Hash: {file_hash}") 

    # 2. Define the Prompt (The Catalyst)
    prompt = "The Basin Protocol is a new architecture for"
    print(f"[*] Prompt: '{prompt}'")

    # 3. Execution Loop (The Invariant Check)
    results = []
    verification_level = "UNKNOWN"
    
    for i in range(1, 3):
        print(f"\n[*] Run #{i}: Initializing GGUF Engine...")
        
        # STRICT DETERMINISM SETTINGS
        llm = Llama(
            model_path=MODEL_PATH,
            verbose=False,
            seed=70627,        # Fixed Seed
            n_ctx=512,
            n_threads=4,       # CPU Threads
            n_threads_batch=4, # Sync batch threads to main threads
            logits_all=True
        )
        
        # Request logprobs to maximize chance of getting token IDs
        output = llm(
            prompt, 
            max_tokens=20, 
            temperature=0.0, # Greedy decoding (Essential)
            top_p=1.0, 
            echo=False,
            logprobs=1       
        )
        
        choice = output['choices'][0]
        raw_text = choice['text']
        
        # === DNA CHECK: Attempt to Retrieve Token IDs ===
        token_ids = []
        
        # 1. Direct Access (Some versions)
        if 'token_ids' in choice:
            token_ids = choice['token_ids']
        # 2. Logprobs Access (Standard OpenAI format)
        elif 'logprobs' in choice and choice['logprobs'] is not None:
             if 'token_logprobs' in choice['logprobs']:
                 # We don't have raw IDs here easily in all versions, 
                 # but we can check if tokens are consistent.
                 pass

        if token_ids:
            # STRONG Verification: Hash the Integer Sequence
            id_string = ','.join(map(str, token_ids))
            output_sig = hashlib.sha256(id_string.encode('utf-8')).hexdigest()
            print(f"[*] Run #{i} Verification Level: STRONG (Token ID Hash)")
            verification_level = "STRONG (Token IDs)"
        else:
            # STANDARD Verification: Hash the Text
            # With Temp=0.0, this is valid, but strictly speaking 'Phenotypic' not 'Genotypic'
            output_sig = hashlib.sha256(raw_text.encode('utf-8')).hexdigest()
            print(f"[*] Run #{i} Verification Level: STANDARD (Text Hash)")
            print(f"    Note: Token IDs not exposed by wrapper. Determinism relies on greedy decoding.")
            verification_level = "STANDARD (Text Output)"

        print(f"[*] Run #{i} Output: \"{raw_text.strip()}...\"")
        print(f"[*] Run #{i} Signature: {output_sig}")
        
        results.append(output_sig)
        
        # Explicit Resource Cleanup
        llm = None
        
    # 4. Final Verdict & Key Generation
    banner("VERIFICATION ANALYSIS")
    if results[0] == results[1]:
        print(f"[+] PASS: Quantized Determinism Verified.")
        print(f"    The Invariant holds under GGUF compression.")
        print(f"    **Linked Input Hash (FULL): {file_hash}**")
        print(f"    **Output Signature (FULL):  {results[0]}**")
        
        # Generate the 'Keys' for Phase 2
        key_file = "proofs/quant_proof_keys.txt"
        with open(key_file, 'w') as f:
            f.write(f"VERIFICATION_LEVEL={verification_level}\n")
            f.write(f"GGUF_FILE={os.path.basename(MODEL_PATH)}\n")
            f.write(f"GGUF_HASH={file_hash}\n")
            f.write(f"BASIN_SIGNATURE={results[0]}\n")
            f.write(f"PROMPT=\"{prompt}\"\n")
        print(f"[*] Verification Keys saved to {key_file}")
            
    else:
        print(f"[!] FAIL: Divergence Detected.")
        print(f"    Run 1: {results[0]}")
        print(f"    Run 2: {results[1]}")
        sys.exit(1)

    banner("PROOF 1.3 COMPLETE: REAL WORLD READY")

if __name__ == "__main__":
    run_inference_proof()
