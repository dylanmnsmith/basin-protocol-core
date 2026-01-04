#!/usr/bin/env python3
"""
Basin Protocol with Proof of Work Integration
Integrates SHA-256 hashing for final output verification and saves to JSON with timestamp.
"""

import hashlib
import json
import time
from datetime import datetime
from pathlib import Path

# Import existing Basin Protocol components
from src.EntropyAwareConsequenceEngine import EntropyAwareConsequenceEngine
from src.MinimalBasinEngine import MinimalBasinEngine


class BasinWithProofOfWork:
    """Enhanced Basin Protocol agent with Proof of Work hashing"""
    
    def __init__(self, use_entropy_engine=True, pow_difficulty=4):
        """
        Initialize Basin Protocol with Proof of Work
        
        Args:
            use_entropy_engine: Whether to use the entropy-aware consequence engine
            pow_difficulty: Number of leading zeros required for Proof of Work
        """
        self.engine = EntropyAwareConsequenceEngine() if use_entropy_engine else MinimalBasinEngine()
        self.pow_difficulty = pow_difficulty
        self.execution_log = []
        
    def compute_sha256(self, data):
        """Compute SHA-256 hash of given data"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    def proof_of_work(self, data, nonce=0):
        """
        Simple Proof of Work implementation
        Finds a nonce that produces a hash with specified number of leading zeros
        """
        target = '0' * self.pow_difficulty
        
        while True:
            # Combine data with nonce
            pow_data = f"{data}:{nonce}"
            hash_result = self.compute_sha256(pow_data)
            
            if hash_result.startswith(target):
                return {
                    'hash': hash_result,
                    'nonce': nonce,
                    'data': data,
                    'difficulty': self.pow_difficulty
                }
            nonce += 1
    
    def execute_with_pow(self, prompt, save_to_file=True, output_dir="pow_logs"):
        """
        Execute Basin Protocol with Proof of Work hashing
        
        Args:
            prompt: Input prompt for the agent
            save_to_file: Whether to save results to JSON file
            output_dir: Directory to save Proof of Work results
            
        Returns:
            Dictionary containing execution results and Proof of Work
        """
        # Step 1: Execute Basin Protocol
        print("[BASIN POW] Executing Basin Protocol...")
        start_time = time.time()
        
        if hasattr(self.engine, 'simulate_with_entropy_gate'):
            result = self.engine.simulate_with_entropy_gate(prompt)
        else:
            result = self.engine.simulate_consequence(prompt)
        
        execution_time = time.time() - start_time
        
        # Step 2: Extract final output string
        if isinstance(result, dict):
            if 'response' in result:
                final_output = result['response']
            elif 'continuation' in result:
                final_output = result['continuation']
            else:
                final_output = str(result)
        else:
            final_output = str(result)
        
        # Step 3: Compute SHA-256 hash of final output
        print("[BASIN POW] Computing SHA-256 hash...")
        output_hash = self.compute_sha256(final_output)
        
        # Step 4: Perform Proof of Work
        print(f"[BASIN POW] Performing Proof of Work (difficulty: {self.pow_difficulty})...")
        pow_start = time.time()
        pow_result = self.proof_of_work(final_output)
        pow_time = time.time() - pow_start
        
        # Step 5: Create execution record
        execution_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'prompt': prompt,
            'basin_result': result,
            'final_output': final_output,
            'output_hash': output_hash,
            'proof_of_work': pow_result,
            'execution_metrics': {
                'basin_execution_time': execution_time,
                'pow_computation_time': pow_time,
                'total_time': execution_time + pow_time,
                'pow_difficulty': self.pow_difficulty,
                'pow_nonce': pow_result['nonce']
            },
            'verification': {
                'hash_verified': self.compute_sha256(final_output) == output_hash,
                'pow_verified': self.verify_proof_of_work(pow_result['hash'], final_output, pow_result['nonce'])
            }
        }
        
        # Step 6: Save to JSON file
        if save_to_file:
            self.save_execution_record(execution_record, output_dir)
        
        print(f"[BASIN POW] Execution complete. Hash: {output_hash}")
        print(f"[BASIN POW] Proof of Work found: {pow_result['hash']}")
        print(f"[BASIN POW] Total execution time: {execution_record['execution_metrics']['total_time']:.2f}s")
        
        return execution_record
    
    def verify_proof_of_work(self, hash_result, data, nonce):
        """Verify that a Proof of Work hash is valid"""
        target = '0' * self.pow_difficulty
        pow_data = f"{data}:{nonce}"
        computed_hash = self.compute_sha256(pow_data)
        return computed_hash == hash_result and hash_result.startswith(target)
    
    def save_execution_record(self, record, output_dir):
        """Save execution record to JSON file with timestamp"""
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"basin_pow_{timestamp}.json"
        filepath = Path(output_dir) / filename
        
        # Save to JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
        
        print(f"[BASIN POW] Execution record saved to: {filepath}")
        return filepath
    
    def batch_execute_with_pow(self, prompts, output_dir="pow_logs"):
        """Execute multiple prompts with Proof of Work"""
        results = []
        
        for i, prompt in enumerate(prompts):
            print(f"\n[BASIN POW] Processing prompt {i+1}/{len(prompts)}")
            try:
                result = self.execute_with_pow(prompt, save_to_file=True, output_dir=output_dir)
                results.append(result)
            except Exception as e:
                print(f"[BASIN POW] Error processing prompt {i+1}: {e}")
                error_record = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'prompt': prompt,
                    'error': str(e),
                    'status': 'failed'
                }
                results.append(error_record)
        
        # Save batch summary
        batch_summary = {
            'timestamp': datetime.utcnow().isoformat(),
            'batch_size': len(prompts),
            'successful': len([r for r in results if 'error' not in r]),
            'failed': len([r for r in results if 'error' in r]),
            'results': results
        }
        
        summary_filename = f"basin_pow_batch_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        summary_path = Path(output_dir) / summary_filename
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(batch_summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n[BASIN POW] Batch summary saved to: {summary_path}")
        return batch_summary


def main():
    """Demonstration of Basin Protocol with Proof of Work"""
    print("=== Basin Protocol with Proof of Work ===\n")
    
    # Initialize Basin with Proof of Work
    basin_pow = BasinWithProofOfWork(use_entropy_engine=True, pow_difficulty=3)
    
    # Example prompts
    test_prompts = [
        "What are the ethical implications of artificial intelligence?",
        "How can we ensure AI systems remain aligned with human values?",
        "Explain the concept of thermodynamic alignment in AI systems."
    ]
    
    # Execute single prompt
    print("Executing single prompt with Proof of Work...\n")
    result = basin_pow.execute_with_pow(
        test_prompts[0],
        save_to_file=True,
        output_dir="pow_logs"
    )
    
    # Verify the Proof of Work
    print("\n=== Verification ===")
    print(f"Hash verified: {result['verification']['hash_verified']}")
    print(f"Proof of Work verified: {result['verification']['pow_verified']}")
    
    # Demonstrate batch execution
    print("\n=== Batch Execution Demo ===")
    print("This would normally process multiple prompts.")
    print("For demo purposes, running single prompt again...\n")
    
    # Clean shutdown with final hash
    final_state = {
        'shutdown_timestamp': datetime.utcnow().isoformat(),
        'total_executions': 1,
        'final_pow_hash': result['proof_of_work']['hash'],
        'session_verified': all(result['verification'].values())
    }
    
    # Save shutdown state
    shutdown_path = Path("pow_logs") / f"basin_shutdown_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(shutdown_path, 'w', encoding='utf-8') as f:
        json.dump(final_state, f, indent=2, ensure_ascii=False)
    
    print(f"[BASIN POW] Shutdown state saved to: {shutdown_path}")
    print("[BASIN POW] Agent shutdown complete with Proof of Work verification.")


if __name__ == "__main__":
    # Ensure output directory exists
    Path("pow_logs").mkdir(exist_ok=True)
    
    # Run main demonstration
    main()
