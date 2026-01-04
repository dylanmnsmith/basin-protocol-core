#!/usr/bin/env python3
"""
Modified Basin Protocol Main Execution Loop with Proof of Work
This integrates SHA-256 hashing and Proof of Work into the existing Basin execution flow.
"""

import hashlib
import json
import time
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

# Import Basin Protocol components
try:
    from EntropyAwareConsequenceEngine import EntropyAwareConsequenceEngine
    from MinimalBasinEngine import MinimalBasinEngine
except ImportError:
    print("[BASIN POW] Error: Could not import Basin Protocol components")
    print("[BASIN POW] Ensure src/ directory is in the correct location")
    sys.exit(1)


class BasinMainExecutionLoop:
    """Main execution loop for Basin Protocol with Proof of Work integration"""
    
    def __init__(self, use_entropy_engine=True, pow_difficulty=4, output_dir="pow_logs"):
        """
        Initialize Basin Protocol execution loop with Proof of Work
        
        Args:
            use_entropy_engine: Whether to use entropy-aware consequence engine
            pow_difficulty: Difficulty level for Proof of Work (leading zeros)
            output_dir: Directory to save Proof of Work results
        """
        self.use_entropy_engine = use_entropy_engine
        self.pow_difficulty = pow_difficulty
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Basin engine
        print("[BASIN MAIN] Initializing Basin Protocol engine...")
        if use_entropy_engine:
            self.engine = EntropyAwareConsequenceEngine()
            print("[BASIN MAIN] Using EntropyAwareConsequenceEngine")
        else:
            self.engine = MinimalBasinEngine()
            print("[BASIN MAIN] Using MinimalBasinEngine")
        
        # Execution state tracking
        self.execution_count = 0
        self.session_start_time = datetime.utcnow()
        self.execution_log = []
        
    def compute_sha256(self, data):
        """Compute SHA-256 hash of data"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    def perform_proof_of_work(self, data):
        """
        Perform Proof of Work on data
        Finds nonce that produces hash with specified leading zeros
        """
        target_prefix = '0' * self.pow_difficulty
        nonce = 0
        
        print(f"[BASIN POW] Mining for proof with {self.pow_difficulty} leading zeros...")
        start_time = time.time()
        
        while True:
            # Create proof data with nonce
            proof_data = f"{data}:{nonce}"
            hash_result = self.compute_sha256(proof_data)
            
            if hash_result.startswith(target_prefix):
                elapsed_time = time.time() - start_time
                print(f"[BASIN POW] Proof found! Nonce: {nonce}, Time: {elapsed_time:.2f}s")
                print(f"[BASIN POW] Proof hash: {hash_result}")
                
                return {
                    'hash': hash_result,
                    'nonce': nonce,
                    'difficulty': self.pow_difficulty,
                    'mining_time': elapsed_time
                }
            
            nonce += 1
            
            # Progress indicator for long mining operations
            if nonce % 100000 == 0:
                print(f"[BASIN POW] ... tried {nonce:,} nonces")
    
    def verify_proof_of_work(self, hash_result, data, nonce, difficulty=None):
        """Verify a Proof of Work result"""
        if difficulty is None:
            difficulty = self.pow_difficulty
            
        target_prefix = '0' * difficulty
        proof_data = f"{data}:{nonce}"
        computed_hash = self.compute_sha256(proof_data)
        
        return (computed_hash == hash_result and 
                hash_result.startswith(target_prefix))
    
    def execute_single(self, prompt, save_individual=True):
        """
        Execute Basin Protocol on a single prompt with Proof of Work
        
        Args:
            prompt: Input prompt
            save_individual: Whether to save individual execution record
            
        Returns:
            Execution record with Proof of Work
        """
        self.execution_count += 1
        execution_start = datetime.utcnow()
        
        print(f"\n[BASIN MAIN] Execution #{self.execution_count} started at {execution_start}")
        print(f"[BASIN MAIN] Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
        
        try:
            # Step 1: Execute Basin Protocol
            print("[BASIN MAIN] Running Basin Protocol consequence simulation...")
            basin_start = time.time()
            
            if self.use_entropy_engine and hasattr(self.engine, 'simulate_with_entropy_gate'):
                basin_result = self.engine.simulate_with_entropy_gate(prompt)
            else:
                basin_result = self.engine.simulate_consequence(prompt)
            
            basin_time = time.time() - basin_start
            
            # Step 2: Extract final output string
            if isinstance(basin_result, dict):
                if 'response' in basin_result:
                    final_output = basin_result['response']
                elif 'continuation' in basin_result:
                    final_output = basin_result['continuation']
                else:
                    final_output = str(basin_result)
            else:
                final_output = str(basin_result)
            
            # Step 3: Compute SHA-256 hash
            print("[BASIN MAIN] Computing SHA-256 hash of final output...")
            output_hash = self.compute_sha256(final_output)
            
            # Step 4: Perform Proof of Work
            pow_result = self.perform_proof_of_work(final_output)
            
            # Step 5: Create execution record
            execution_record = {
                'execution_id': self.execution_count,
                'timestamp': execution_start.isoformat(),
                'prompt': prompt,
                'basin_result': basin_result,
                'final_output': final_output,
                'output_hash': output_hash,
                'proof_of_work': pow_result,
                'metrics': {
                    'basin_execution_time': basin_time,
                    'pow_computation_time': pow_result['mining_time'],
                    'total_execution_time': basin_time + pow_result['mining_time'],
                    'output_length': len(final_output)
                },
                'verification': {
                    'hash_verified': self.compute_sha256(final_output) == output_hash,
                    'pow_verified': self.verify_proof_of_work(
                        pow_result['hash'], final_output, pow_result['nonce']
                    )
                }
            }
            
            # Step 6: Save individual record if requested
            if save_individual:
                self.save_execution_record(execution_record)
            
            # Add to execution log
            self.execution_log.append(execution_record)
            
            print(f"[BASIN MAIN] Execution #{self.execution_count} completed successfully")
            print(f"[BASIN MAIN] Hash: {output_hash}")
            print(f"[BASIN MAIN] Verification: {execution_record['verification']}")
            
            return execution_record
            
        except Exception as e:
            print(f"[BASIN MAIN] ERROR in execution #{self.execution_count}: {e}")
            error_record = {
                'execution_id': self.execution_count,
                'timestamp': execution_start.isoformat(),
                'prompt': prompt,
                'error': str(e),
                'status': 'failed'
            }
            self.execution_log.append(error_record)
            return error_record
    
    def save_execution_record(self, record):
        """Save individual execution record to JSON file"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"basin_execution_{record['execution_id']:04d}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
        
        print(f"[BASIN MAIN] Execution record saved to: {filepath}")
        return filepath
    
    def execute_batch(self, prompts, save_batch_summary=True):
        """Execute multiple prompts with Proof of Work"""
        print(f"\n[BASIN MAIN] Starting batch execution of {len(prompts)} prompts")
        
        for i, prompt in enumerate(prompts):
            print(f"\n{'='*60}")
            print(f"[BASIN MAIN] Processing prompt {i+1}/{len(prompts)}")
            self.execute_single(prompt, save_individual=True)
        
        # Save batch summary
        if save_batch_summary:
            self.save_batch_summary()
        
        return self.execution_log
    
    def save_batch_summary(self):
        """Save batch execution summary"""
        successful_executions = [
            record for record in self.execution_log 
            if record.get('status') != 'failed'
        ]
        
        summary = {
            'session_start': self.session_start_time.isoformat(),
            'session_end': datetime.utcnow().isoformat(),
            'total_executions': len(self.execution_log),
            'successful_executions': len(successful_executions),
            'failed_executions': len(self.execution_log) - len(successful_executions),
            'pow_difficulty': self.pow_difficulty,
            'engine_type': 'EntropyAwareConsequenceEngine' if self.use_entropy_engine else 'MinimalBasinEngine',
            'execution_log': self.execution_log
        }
        
        # Calculate aggregate metrics
        if successful_executions:
            total_pow_time = sum(
                record['proof_of_work']['mining_time'] 
                for record in successful_executions
            )
            total_basin_time = sum(
                record['metrics']['basin_execution_time'] 
                for record in successful_executions
            )
            
            summary['aggregate_metrics'] = {
                'total_basin_execution_time': total_basin_time,
                'total_pow_computation_time': total_pow_time,
                'average_basin_time': total_basin_time / len(successful_executions),
                'average_pow_time': total_pow_time / len(successful_executions),
                'total_hashes_computed': sum(
                    record['proof_of_work']['nonce'] + 1
                    for record in successful_executions
                )
            }
        
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"basin_batch_summary_{timestamp}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n[BASIN MAIN] Batch summary saved to: {filepath}")
        return filepath
    
    def shutdown_with_pow(self):
        """Graceful shutdown with final Proof of Work summary"""
        print(f"\n{'='*60}")
        print("[BASIN MAIN] Initiating graceful shutdown with Proof of Work...")
        
        # Create final shutdown record
        shutdown_record = {
            'shutdown_timestamp': datetime.utcnow().isoformat(),
            'session_duration': str(datetime.utcnow() - self.session_start_time),
            'total_executions': len(self.execution_log),
            'successful_verifications': sum(
                1 for record in self.execution_log
                if record.get('verification', {}).get('hash_verified') and 
                   record.get('verification', {}).get('pow_verified')
            ),
            'pow_difficulty_used': self.pow_difficulty,
            'engine_type': 'EntropyAwareConsequenceEngine' if self.use_entropy_engine else 'MinimalBasinEngine',
            'final_state_hash': None  # Will be computed below
        }
        
        # Create final state summary for hashing
        state_summary = f"basin_session_{self.session_start_time.isoformat()}_{len(self.execution_log)}_executions"
        final_hash = self.compute_sha256(state_summary)
        shutdown_record['final_state_hash'] = final_hash
        
        # Save shutdown record
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"basin_shutdown_{timestamp}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(shutdown_record, f, indent=2, ensure_ascii=False)
        
        print(f"[BASIN MAIN] Shutdown record saved to: {filepath}")
        print(f"[BASIN MAIN] Final session hash: {final_hash}")
        print(f"[BASIN MAIN] Agent shutdown complete with Proof of Work verification.")
        
        return shutdown_record


def main():
    """Main demonstration of Basin Protocol with Proof of Work"""
    print("="*60)
    print("Basin Protocol Main Execution Loop with Proof of Work")
    print("="*60)
    
    # Initialize execution loop
    execution_loop = BasinMainExecutionLoop(
        use_entropy_engine=True,
        pow_difficulty=3,  # Lower difficulty for demo (adjust as needed)
        output_dir="pow_logs"
    )
    
    # Test prompts
    test_prompts = [
        "What are the ethical considerations in developing advanced AI systems?",
        "How can we ensure AI alignment with human values?",
        "Explain the Basin Protocol approach to AI safety."
    ]
    
    try:
        # Execute single prompt
        print("\n" + "="*60)
        print("SINGLE EXECUTION DEMO")
        print("="*60)
        
        result = execution_loop.execute_single(test_prompts[0])
        
        # Verify results
        if result.get('verification', {}).get('hash_verified') and result.get('verification', {}).get('pow_verified'):
            print("\n✓ All verifications passed!")
        else:
            print("\n✗ Verification failed!")
        
        # Execute batch (commented out for demo - uncomment to test)
        # print("\n" + "="*60)
        # print("BATCH EXECUTION DEMO")
        # print("="*60)
        # execution_loop.execute_batch(test_prompts)
        
    except KeyboardInterrupt:
        print("\n\n[BASIN MAIN] Interrupted by user")
    except Exception as e:
        print(f"\n[BASIN MAIN] Error during execution: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Always perform graceful shutdown with Proof of Work
        execution_loop.shutdown_with_pow()


if __name__ == "__main__":
    main()
