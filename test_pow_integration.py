#!/usr/bin/env python3
"""
Test script for Basin Protocol Proof of Work integration
Demonstrates SHA-256 hashing and Proof of Work without full Basin engine
"""

import hashlib
import json
import time
from datetime import datetime
from pathlib import Path


class ProofOfWorkTester:
    """Simple Proof of Work demonstration without Basin Protocol dependencies"""
    
    def __init__(self, difficulty=3):
        self.difficulty = difficulty
        self.results = []
        
    def compute_sha256(self, data):
        """Compute SHA-256 hash"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    def mine_proof_of_work(self, data, max_attempts=None):
        """Mine for Proof of Work"""
        target = '0' * self.difficulty
        nonce = 0
        
        print(f"[POW TEST] Mining for hash with {self.difficulty} leading zeros...")
        print(f"[POW TEST] Target prefix: {target}")
        print(f"[POW TEST] Data: {data[:50]}{'...' if len(data) > 50 else ''}")
        
        start_time = time.time()
        
        while True:
            if max_attempts and nonce >= max_attempts:
                print(f"[POW TEST] Max attempts ({max_attempts}) reached, stopping.")
                return None
            
            # Create proof data
            proof_data = f"{data}:{nonce}"
            hash_result = self.compute_sha256(proof_data)
            
            # Check if we found a valid proof
            if hash_result.startswith(target):
                elapsed_time = time.time() - start_time
                
                result = {
                    'data': data,
                    'nonce': nonce,
                    'hash': hash_result,
                    'difficulty': self.difficulty,
                    'attempts': nonce + 1,
                    'time_seconds': elapsed_time,
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                print(f"\n[POW TEST] ✓ Proof of Work found!")
                print(f"[POW TEST]   Nonce: {nonce:,}")
                print(f"[POW TEST]   Hash: {hash_result}")
                print(f"[POW TEST]   Time: {elapsed_time:.3f} seconds")
                print(f"[POW TEST]   Attempts: {nonce + 1:,}")
                
                return result
            
            # Progress indicator
            if nonce > 0 and nonce % 50000 == 0:
                elapsed = time.time() - start_time
                rate = nonce / elapsed if elapsed > 0 else 0
                print(f"[POW TEST] ... {nonce:,} attempts ({rate:.0f} H/s)")
            
            nonce += 1
    
    def verify_proof(self, hash_result, data, nonce, difficulty=None):
        """Verify a Proof of Work result"""
        if difficulty is None:
            difficulty = self.difficulty
            
        target = '0' * difficulty
        proof_data = f"{data}:{nonce}"
        computed_hash = self.compute_sha256(proof_data)
        
        is_valid = (
            computed_hash == hash_result and 
            hash_result.startswith(target)
        )
        
        print(f"\n[POW TEST] Verification:")
        print(f"[POW TEST]   Expected: {hash_result}")
        print(f"[POW TEST]   Computed: {computed_hash}")
        print(f"[POW TEST]   Matches:  {computed_hash == hash_result}")
        print(f"[POW TEST]   Target:   {target}")
        print(f"[POW TEST]   Starts:   {hash_result.startswith(target)}")
        print(f"[POW TEST]   Valid:    {is_valid}")
        
        return is_valid
    
    def test_with_sample_data(self):
        """Test Proof of Work with sample data"""
        print("="*60)
        print("PROOF OF WORK DEMONSTRATION")
        print("="*60)
        
        # Test with different difficulty levels
        test_cases = [
            {"data": "Hello, Basin Protocol!", "difficulty": 2},
            {"data": "The quick brown fox jumps over the lazy dog", "difficulty": 3},
            {"data": "Basin Protocol: Thermodynamic Alignment for AI", "difficulty": 3},
        ]
        
        for i, test_case in enumerate(test_cases):
            print(f"\n{'-'*60}")
            print(f"Test Case {i+1}: Difficulty {test_case['difficulty']}")
            print(f"{'-'*60}")
            
            # Set difficulty
            original_difficulty = self.difficulty
            self.difficulty = test_case['difficulty']
            
            # Mine proof of work
            result = self.mine_proof_of_work(test_case['data'], max_attempts=1000000)
            
            if result:
                # Verify the proof
                is_valid = self.verify_proof(
                    result['hash'], 
                    result['data'], 
                    result['nonce'],
                    result['difficulty']
                )
                
                # Save result
                result['verification_passed'] = is_valid
                self.results.append(result)
                
                # Save to JSON
                self.save_result(result, f"pow_test_{i+1}")
            else:
                print(f"[POW TEST] Mining failed or was stopped.")
            
            # Restore original difficulty
            self.difficulty = original_difficulty
    
    def test_hashing_speed(self):
        """Test SHA-256 hashing speed"""
        print(f"\n{'='*60}")
        print("HASHING SPEED TEST")
        print("="*60)
        
        test_sizes = [100, 1000, 10000, 100000]  # bytes
        
        for size in test_sizes:
            # Generate test data
            test_data = "x" * size
            
            # Time hashing
            start_time = time.time()
            iterations = 0
            
            while time.time() - start_time < 1.0:  # Run for 1 second
                self.compute_sha256(test_data)
                iterations += 1
            
            elapsed = time.time() - start_time
            rate = iterations / elapsed
            
            print(f"[POW TEST] {size:6d} bytes: {rate:8.0f} hashes/second")
    
    def demonstrate_difficulty_scaling(self):
        """Show how difficulty affects mining time"""
        print(f"\n{'='*60}")
        print("DIFFICULTY SCALING DEMONSTRATION")
        print("="*60)
        
        test_data = "Difficulty scaling test data"
        max_difficulty = 5
        
        for difficulty in range(1, max_difficulty + 1):
            print(f"\n[POW TEST] Testing difficulty {difficulty}...")
            
            # Set difficulty
            self.difficulty = difficulty
            
            # Mine with time limit
            start_time = time.time()
            result = self.mine_proof_of_work(test_data, max_attempts=100000)
            elapsed = time.time() - start_time
            
            if result:
                expected_time = (16 ** difficulty) / 100000  # Rough estimate
                print(f"[POW TEST]   Expected ~{expected_time:.3f}s, Actual: {elapsed:.3f}s")
            else:
                print(f"[POW TEST]   Did not complete within attempt limit")
    
    def save_result(self, result, filename_prefix):
        """Save result to JSON file"""
        output_dir = Path("pow_logs")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"[POW TEST] Result saved to: {filepath}")
        return filepath
    
    def create_summary_report(self):
        """Create a summary report of all tests"""
        if not self.results:
            print("[POW TEST] No results to summarize.")
            return
        
        print(f"\n{'='*60}")
        print("SUMMARY REPORT")
        print("="*60)
        
        total_time = sum(result['time_seconds'] for result in self.results)
        total_attempts = sum(result['attempts'] for result in self.results)
        
        print(f"[POW TEST] Total tests: {len(self.results)}")
        print(f"[POW TEST] Total mining time: {total_time:.3f} seconds")
        print(f"[POW TEST] Total attempts: {total_attempts:,}")
        print(f"[POW TEST] Average time per test: {total_time/len(self.results):.3f} seconds")
        print(f"[POW TEST] All verifications passed: {all(r['verification_passed'] for r in self.results)}")
        
        # Save summary
        summary = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_tests': len(self.results),
            'total_mining_time': total_time,
            'total_attempts': total_attempts,
            'average_time_per_test': total_time / len(self.results),
            'all_verifications_passed': all(r['verification_passed'] for r in self.results),
            'results': self.results
        }
        
        self.save_result(summary, "pow_summary")


def main():
    """Run Proof of Work tests"""
    print("Proof of Work Integration Test for Basin Protocol")
    print("="*60)
    print("This demonstrates SHA-256 hashing and Proof of Work")
    print("without requiring the full Basin Protocol setup.\n")
    
    # Create tester
    tester = ProofOfWorkTester(difficulty=3)
    
    try:
        # Run tests
        tester.test_with_sample_data()
        tester.test_hashing_speed()
        tester.demonstrate_difficulty_scaling()
        tester.create_summary_report()
        
        print(f"\n{'='*60}")
        print("All tests completed!")
        print("Check the pow_logs/ directory for JSON output files.")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n[POW TEST] Interrupted by user")
    except Exception as e:
        print(f"\n[POW TEST] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
