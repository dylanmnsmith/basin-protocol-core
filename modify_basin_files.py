#!/usr/bin/env python3
"""
Guide for modifying existing Basin Protocol files to add Proof of Work
This shows the exact modifications needed for integration
"""

import os
from pathlib import Path


class BasinModificationGuide:
    """Guide for modifying Basin Protocol files"""
    
    def __init__(self):
        self.modifications = {
            "EntropyAwareConsequenceEngine.py": self.get_entropy_engine_mods(),
            "MinimalBasinEngine.py": self.get_minimal_engine_mods(),
            "basin_autonomous.ps1": self.get_powershell_mods(),
        }
    
    def get_entropy_engine_mods(self):
        """Modifications for EntropyAwareConsequenceEngine.py"""
        return {
            "imports_addition": """
import hashlib
import json
from datetime import datetime
""",
            "methods_to_add": """
    def compute_sha256(self, data):
        \"\"\"Compute SHA-256 hash of data\"\"\"
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    def perform_proof_of_work(self, data, difficulty=4):
        \"\"\"Perform Proof of Work on data\"\"\"
        target = '0' * difficulty
        nonce = 0
        
        print(f"[BASIN] Mining for proof with {difficulty} leading zeros...")
        import time
        start_time = time.time()
        
        while True:
            pow_data = f"{data}:{nonce}"
            hash_result = self.compute_sha256(pow_data)
            
            if hash_result.startswith(target):
                elapsed = time.time() - start_time
                print(f"[BASIN] Proof found! Nonce: {nonce}, Time: {elapsed:.2f}s")
                return {'hash': hash_result, 'nonce': nonce, 'difficulty': difficulty}
            nonce += 1
    
    def execute_with_pow(self, prompt, save_to_file=True):
        \"\"\"Execute with Proof of Work and save to JSON\"\"\"
        # Execute normal Basin protocol
        result = self.simulate_with_entropy_gate(prompt)
        
        # Extract final output
        final_output = result.get('response', str(result))
        
        # Compute hash
        output_hash = self.compute_sha256(final_output)
        
        # Perform Proof of Work
        pow_result = self.perform_proof_of_work(final_output)
        
        # Create record
        record = {
            'timestamp': datetime.utcnow().isoformat(),
            'prompt': prompt,
            'result': result,
            'final_output': final_output,
            'output_hash': output_hash,
            'proof_of_work': pow_result
        }
        
        # Save to file
        if save_to_file:
            from pathlib import Path
            Path("pow_logs").mkdir(exist_ok=True)
            filename = f"basin_pow_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = Path("pow_logs") / filename
            with open(filepath, 'w') as f:
                json.dump(record, f, indent=2)
            print(f"[BASIN] Saved to: {filepath}")
        
        return result
"""
        }
    
    def get_minimal_engine_mods(self):
        """Modifications for MinimalBasinEngine.py"""
        return {
            "imports_addition": """
import hashlib
import json
from datetime import datetime
""",
            "methods_to_add": """
    def compute_sha256(self, data):
        \"\"\"Compute SHA-256 hash of data\"\"\"
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    def execute_with_hashing(self, prompt):
        \"\"\"Execute with SHA-256 hashing\"\"\"
        result = self.simulate_consequence(prompt)
        
        # Extract final output
        if isinstance(result, dict) and 'continuation' in result:
            final_output = result['continuation']
        else:
            final_output = str(result)
        
        # Compute hash
        output_hash = self.compute_sha256(final_output)
        
        # Save record
        record = {
            'timestamp': datetime.utcnow().isoformat(),
            'prompt': prompt,
            'output': final_output,
            'hash': output_hash
        }
        
        from pathlib import Path
        Path("pow_logs").mkdir(exist_ok=True)
        filename = f"basin_hash_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = Path("pow_logs") / filename
        with open(filepath, 'w') as f:
            json.dump(record, f, indent=2)
        
        print(f"[BASIN] Hash: {output_hash}")
        print(f"[BASIN] Saved to: {filepath}")
        
        return result
"""
        }
    
    def get_powershell_mods(self):
        """Modifications for basin_autonomous.ps1"""
        return {
            "add_after_verification": """
# Proof of Work Integration
echo "[BASIN] Starting Proof of Work integration..."

# Create Python script for PoW integration
cat > basin_pow_wrapper.py << 'EOF'
import sys
sys.path.append('src')
from EntropyAwareConsequenceEngine import EntropyAwareConsequenceEngine
import datetime

# Initialize engine
engine = EntropyAwareConsequenceEngine()

# Example execution with Proof of Work
prompt = "Execute Basin Protocol with Proof of Work verification"
result = engine.execute_with_pow(prompt)

print(f"[BASIN] Execution completed at {datetime.datetime.utcnow()}")
EOF

# Execute with Proof of Work
python basin_pow_wrapper.py

# Final shutdown with hash
echo "[BASIN] Creating final state hash..."
python -c "
import hashlib, datetime, json
state = f'basin_session_{datetime.datetime.utcnow().isoformat()}'
final_hash = hashlib.sha256(state.encode()).hexdigest()
record = {'final_hash': final_hash, 'timestamp': datetime.datetime.utcnow().isoformat()}
with open('pow_logs/basin_shutdown.json', 'w') as f:
    json.dump(record, f, indent=2)
print(f'[BASIN] Final hash: {final_hash}')
"
"""
        }
    
    def create_modified_file(self, original_file, modifications):
        """Create modified version of a file"""
        # This would read the original file and insert modifications
        # For now, we'll create example files showing the changes
        pass
    
    def generate_integration_script(self):
        """Generate a script that applies the modifications"""
        script_content = '''#!/usr/bin/env python3
"""
Basin Protocol Proof of Work Integration Script
This script helps integrate PoW into existing Basin files
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


def backup_original_file(filepath):
    """Create backup of original file"""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{filepath}.backup_{timestamp}"
    shutil.copy2(filepath, backup_path)
    print(f"[INTEGRATION] Backup created: {backup_path}")
    return backup_path


def add_imports_to_file(filepath):
    """Add required imports to Python file"""
    imports_to_add = [
        "import hashlib",
        "import json", 
        "from datetime import datetime"
    ]
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find the end of existing imports
    lines = content.split('\\n')
    insert_index = 0
    
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            insert_index = i + 1
    
    # Add new imports
    new_lines = lines[:insert_index] + imports_to_add + lines[insert_index:]
    new_content = '\\n'.join(new_lines)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    print(f"[INTEGRATION] Imports added to {filepath}")


def add_methods_to_entropy_engine(filepath):
    """Add PoW methods to EntropyAwareConsequenceEngine"""
    methods = """
    def compute_sha256(self, data):
        \"\"\"Compute SHA-256 hash of data\"\"\"
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    def perform_proof_of_work(self, data, difficulty=4):
        \"\"\"Perform Proof of Work on data\"\"\"
        target = '0' * difficulty
        nonce = 0
        
        print(f"[BASIN] Mining for proof with {difficulty} leading zeros...")
        import time
        start_time = time.time()
        
        while True:
            pow_data = f"{data}:{nonce}"
            hash_result = self.compute_sha256(pow_data)
            
            if hash_result.startswith(target):
                elapsed = time.time() - start_time
                print(f"[BASIN] Proof found! Nonce: {nonce}, Time: {elapsed:.2f}s")
                return {'hash': hash_result, 'nonce': nonce, 'difficulty': difficulty}
            nonce += 1
    
    def execute_with_pow(self, prompt, save_to_file=True):
        \"\"\"Execute with Proof of Work and save to JSON\"\"\"
        # Execute normal Basin protocol
        result = self.simulate_with_entropy_gate(prompt)
        
        # Extract final output
        final_output = result.get('response', str(result))
        
        # Compute hash
        output_hash = self.compute_sha256(final_output)
        
        # Perform Proof of Work
        pow_result = self.perform_proof_of_work(final_output)
        
        # Create record
        record = {
            'timestamp': datetime.utcnow().isoformat(),
            'prompt': prompt,
            'result': result,
            'final_output': final_output,
            'output_hash': output_hash,
            'proof_of_work': pow_result
        }
        
        # Save to file
        if save_to_file:
            from pathlib import Path
            Path("pow_logs").mkdir(exist_ok=True)
            filename = f"basin_pow_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = Path("pow_logs") / filename
            with open(filepath, 'w') as f:
                json.dump(record, f, indent=2)
            print(f"[BASIN] Saved to: {filepath}")
        
        return result
"""
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Add methods at the end of the class
    # Find the last method or the end of the class
    lines = content.split('\\n')
    insert_index = len(lines) - 1
    
    # Look for the end of the class
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == "" and i > 0:
            insert_index = i
            break
    
    new_lines = lines[:insert_index] + methods.split('\\n') + lines[insert_index:]
    new_content = '\\n'.join(new_lines)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    print(f"[INTEGRATION] Methods added to {filepath}")


def main():
    """Main integration function"""
    print("Basin Protocol Proof of Work Integration")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("src").exists():
        print("[ERROR] src/ directory not found. Please run from Basin Protocol root.")
        return
    
    # Create output directory
    Path("pow_logs").mkdir(exist_ok=True)
    
    # Modify EntropyAwareConsequenceEngine
    engine_file = Path("src/EntropyAwareConsequenceEngine.py")
    if engine_file.exists():
        print(f"\\n[INTEGRATION] Modifying {engine_file}")
        backup_original_file(engine_file)
        add_imports_to_file(engine_file)
        add_methods_to_entropy_engine(engine_file)
    else:
        print(f"[ERROR] File not found: {engine_file}")
    
    print("\\n[INTEGRATION] Integration complete!")
    print("[INTEGRATION] You can now use engine.execute_with_pow(prompt)")
    print("[INTEGRATION] Check pow_logs/ directory for output files.")


if __name__ == "__main__":
    main()
'''
        
        # Save the integration script
        with open("integrate_pow.py", "w") as f:
            f.write(script_content)
        
        print("Created: integrate_pow.py")
        return "integrate_pow.py"
    
    def print_modification_summary(self):
        """Print summary of all modifications"""
        print("="*60)
        print("BASIN PROTOCOL PROOF OF WORK INTEGRATION GUIDE")
        print("="*60)
        print("\nThis guide shows how to modify existing Basin Protocol files")
        print("to add SHA-256 hashing and Proof of Work functionality.\n")
        
        for filename, modifications in self.modifications.items():
            print(f"\n{'-'*60}")
            print(f"FILE: {filename}")
            print(f"{'-'*60}")
            
            print("\n1. ADD THESE IMPORTS:")
            print(modifications["imports_addition"])
            
            print("\n2. ADD THESE METHODS:")
            print(modifications["methods_to_add"])
        
        print(f"\n{'='*60}")
        print("INTEGRATION SCRIPT")
        print("="*60)
        print("Run 'python modify_basin_files.py' to generate an integration script")
        print("that can automatically apply these modifications.")
        
        print(f"\n{'='*60}")
        print("ALTERNATIVE: DROP-IN REPLACEMENT")
        print("="*60)
        print("Instead of modifying existing files, you can use:")
        print("- basin_execution_loop_with_pow.py (recommended)")
        print("- basin_pow_integration.py (standalone demo)")
        print("\nThese files provide the same functionality without")
        print("modifying your existing codebase.")


def main():
    """Main function"""
    guide = BasinModificationGuide()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-script":
        # Generate integration script
        script_path = guide.generate_integration_script()
        print(f"\nGenerated integration script: {script_path}")
        print("Run 'python integrate_pow.py' to apply modifications")
    else:
        # Print modification guide
        guide.print_modification_summary()


if __name__ == "__main__":
    import sys
    main()
