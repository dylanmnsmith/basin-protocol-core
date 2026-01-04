# Basin Protocol Proof of Work Integration

This document explains how to integrate SHA-256 hashing and Proof of Work (PoW) functionality into the Basin Protocol core execution loop.

## Overview

The integration adds cryptographic verification to the Basin Protocol by:

1. **SHA-256 Hashing**: Computing a cryptographic hash of the final agent output
2. **Proof of Work**: Performing computational work to find a hash with specific leading zeros
3. **JSON Logging**: Saving execution records with timestamps to local files
4. **Verification**: Ensuring the integrity of both the hash and proof of work

## Files Provided

### 1. `basin_pow_integration.py`
A standalone demonstration of Basin Protocol with Proof of Work integration.

**Features:**
- Complete integration with existing Basin engines
- Configurable Proof of Work difficulty
- Individual and batch execution modes
- Automatic JSON logging with timestamps

### 2. `basin_execution_loop_with_pow.py`
Modified main execution loop that integrates Proof of Work directly into the Basin Protocol workflow.

**Features:**
- Drop-in replacement for existing execution loops
- Graceful shutdown with final state hashing
- Comprehensive execution logging
- Batch processing capabilities

## Integration Steps

### Step 1: Add Required Imports

Add these imports to your existing Basin Protocol execution files:

```python
import hashlib
import json
import time
from datetime import datetime
```

### Step 2: Add Hashing Function

```python
def compute_sha256(self, data):
    """Compute SHA-256 hash of data"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()
```

### Step 3: Add Proof of Work Method

```python
def perform_proof_of_work(self, data, difficulty=4):
    """Perform Proof of Work on data"""
    target_prefix = '0' * difficulty
    nonce = 0
    
    while True:
        pow_data = f"{data}:{nonce}"
        hash_result = self.compute_sha256(pow_data)
        
        if hash_result.startswith(target_prefix):
            return {
                'hash': hash_result,
                'nonce': nonce,
                'difficulty': difficulty
            }
        nonce += 1
```

### Step 4: Integrate into Main Loop

```python
def execute_with_pow(self, prompt):
    # 1. Execute Basin Protocol
    result = self.engine.simulate_with_entropy_gate(prompt)
    
    # 2. Extract final output
    final_output = result.get('response', str(result))
    
    # 3. Compute hash
    output_hash = self.compute_sha256(final_output)
    
    # 4. Perform Proof of Work
    pow_result = self.perform_proof_of_work(final_output)
    
    # 5. Save to JSON
    self.save_execution_record({
        'timestamp': datetime.utcnow().isoformat(),
        'prompt': prompt,
        'output': final_output,
        'hash': output_hash,
        'proof_of_work': pow_result
    })
    
    return result
```

### Step 5: Add Shutdown Hook

```python
def shutdown_with_pow(self):
    """Graceful shutdown with final hash"""
    final_state = f"basin_session_{datetime.utcnow().isoformat()}_{self.execution_count}"
    final_hash = self.compute_sha256(final_state)
    
    self.save_execution_record({
        'type': 'shutdown',
        'timestamp': datetime.utcnow().isoformat(),
        'final_hash': final_hash,
        'total_executions': self.execution_count
    })
```

## Configuration Options

### Proof of Work Difficulty
- **Difficulty 1-2**: Fast execution, minimal security
- **Difficulty 3-4**: Balanced for testing and development
- **Difficulty 5+**: Production-level security, slower execution

### Output Directory
By default, all JSON files are saved to `pow_logs/`. This can be configured:

```python
execution_loop = BasinMainExecutionLoop(
    use_entropy_engine=True,
    pow_difficulty=4,
    output_dir="my_pow_logs"  # Custom directory
)
```

## Usage Examples

### Basic Usage
```python
# Initialize Basin with Proof of Work
basin_pow = BasinWithProofOfWork(use_entropy_engine=True, pow_difficulty=3)

# Execute with Proof of Work
result = basin_pow.execute_with_pow("Your prompt here")

# Results are automatically saved to JSON
```

### Batch Processing
```python
# Process multiple prompts
prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]
batch_results = basin_pow.batch_execute_with_pow(prompts)
```

### Custom Integration
```python
# Integrate into existing Basin execution
class EnhancedBasinEngine(EntropyAwareConsequenceEngine):
    def __init__(self):
        super().__init__()
        self.pow_difficulty = 4
        
    def execute_with_hashing(self, prompt):
        result = self.simulate_with_entropy_gate(prompt)
        final_output = result.get('response', str(result))
        
        # Add Proof of Work
        pow_result = self.perform_proof_of_work(final_output)
        
        # Save with timestamp
        self.save_to_json({
            'timestamp': datetime.utcnow().isoformat(),
            'output': final_output,
            'proof_of_work': pow_result
        })
        
        return result
```

## JSON Output Format

Each execution creates a JSON file with this structure:

```json
{
  "execution_id": 1,
  "timestamp": "2026-01-04T12:00:00.000000",
  "prompt": "Your input prompt",
  "basin_result": {
    "response": "Agent output",
    "entropy": 2.5,
    "status": "success"
  },
  "final_output": "Final agent output string",
  "output_hash": "a1b2c3d4e5f6...",
  "proof_of_work": {
    "hash": "000abc123def...",
    "nonce": 12345,
    "difficulty": 4,
    "mining_time": 0.123
  },
  "verification": {
    "hash_verified": true,
    "pow_verified": true
  }
}
```

## Verification

### Manual Verification
```python
# Verify a Proof of Work result
import hashlib
data = "Final output string"
nonce = 12345
expected_hash = "000abc123def..."

pow_data = f"{data}:{nonce}"
computed_hash = hashlib.sha256(pow_data.encode()).hexdigest()

assert computed_hash == expected_hash
assert expected_hash.startswith("0000")  # For difficulty 4
```

### Automated Verification
The integration includes automatic verification:
- Hash verification: Ensures output hash matches computed hash
- Proof verification: Validates the Proof of Work solution

## Security Considerations

1. **Hash Function**: SHA-256 provides strong cryptographic integrity
2. **Proof of Work**: Prevents tampering by requiring computational effort
3. **Timestamps**: UTC timestamps ensure chronological ordering
4. **File Integrity**: Each execution saved separately for audit trails

## Performance Impact

- **SHA-256 Hashing**: Negligible overhead (< 1ms)
- **Proof of Work**: Variable based on difficulty
  - Difficulty 3: ~0.1-1 seconds
  - Difficulty 4: ~1-10 seconds  
  - Difficulty 5: ~10-60 seconds

## Testing

Run the demonstration:

```bash
# Run standalone demonstration
python basin_pow_integration.py

# Run modified execution loop
python basin_execution_loop_with_pow.py
```

Expected output:
- Proof of Work mining progress
- Hash verification results
- JSON file locations
- Final shutdown summary

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure src/ directory is in Python path
2. **Slow Execution**: Reduce Proof of Work difficulty
3. **Memory Usage**: Process outputs in batches
4. **File Permissions**: Ensure write access to output directory

### Debug Mode

Enable debug output by setting environment variable:
```bash
export BASIN_DEBUG=1
```

## Next Steps

1. **Integrate with existing Basin Protocol codebase**
2. **Adjust Proof of Work difficulty for your use case**
3. **Add custom logging and monitoring**
4. **Implement distributed verification (optional)**
5. **Add backup and archival strategies**

## License

This integration maintains the same license as the original Basin Protocol.
