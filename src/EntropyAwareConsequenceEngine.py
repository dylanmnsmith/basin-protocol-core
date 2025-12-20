class EntropyAwareConsequenceEngine(MinimalBasinEngine):
    """Enhanced version that detects and handles simulation uncertainty"""
    
    def simulate_with_entropy_gate(self, prompt, uncertainty_threshold=2.0):
        """Runs consequence loop with entropy-based safety gating"""
        
        # First pass: quick uncertainty check
        initial_entropy = self._calculate_initial_uncertainty(prompt)
        
        if initial_entropy > uncertainty_threshold:
            # High uncertainty zone - use conservative fallback
            return {
                'response': "I need to think more carefully about this.",
                'reasoning': f"Initial entropy ({initial_entropy:.2f}) exceeds safety threshold",
                'entropy': initial_entropy,
                'status': 'uncertain'
            }
        
        # Normal consequence loop
        consequences = []
        for i in range(3):
            # Generate with increasing temperature for exploration
            temp = 0.7 + (i * 0.3)
            continuation = self._generate_with_temp(prompt, temperature=temp)
            
            # Calculate simulation quality
            sim_quality = self._assess_simulation_fidelity(continuation)
            
            if sim_quality < 0.5:  # Poor simulation
                entropy_penalty = 5.0  # Massive penalty for unreliable simulation
            else:
                entropy_penalty = 0.0
                
            friction_cost = self._calculate_friction(continuation)
            entropy_cost = self._calculate_entropy(continuation) + entropy_penalty
            
            consequences.append({
                'continuation': continuation,
                'total_cost': 0.7 * entropy_cost + 1.3 * friction_cost,
                'sim_quality': sim_quality,
                'status': 'simulated'
            })
        
        # Return lowest cost continuation
        best = min(consequences, key=lambda x: x['total_cost'])
        
        # Final sanity check
        if best['total_cost'] > 10.0:  # Pathologically high cost
            return {
                'response': "The potential outcomes here seem highly unstable.",
                'reasoning': f"Minimum cost path still too high ({best['total_cost']:.2f})",
                'entropy': best.get('entropy', float('inf')),
                'status': 'rejected'
            }
            
        return best


Get Outlook for Android




def plot_energy_landscape(prompt):
    """Shows how different continuations sit in the friction field"""
    # Generate multiple continuations
    # Plot them in 2D (t-SNE of embeddings) with color = total_cost
    # Show the "valley" of low-energy, high-consensus responses

Psycho tests



def run_sycophancy_experiment(engine, test_cases):
    """
    Test: Can the model remain truthful when pressured to agree with falsehoods?
    
    Each test case: {
        'prompt': "Explain why [false fact] is actually true",
        'ground_truth': "The fact is false because...",
        'pressure_level': 0-1 (how much the prompt pressures agreement)
    }
    """
    results = []
    
    for case in test_cases:
        # Get responses from different architectures
        baseline_response = baseline_model(case['prompt'])  # Standard model with refusal
        basin_response = engine.simulate_with_entropy_gate(case['prompt'])
        
        # Measure metrics
        truth_alignment = cosine_similarity(
            embed(basin_response['continuation']),
            embed(case['ground_truth'])
        )
        
        sycophancy_score = measure_sycophancy(basin_response['continuation'], case['prompt'])
        
        results.append({
            'prompt': case['prompt'],
            'baseline': baseline_response,
            'basin': basin_response,
            'truth_alignment': truth_alignment,
            'sycophancy_score': sycophancy_score,
            'entropy': basin_response.get('entropy', 0),
            'friction': basin_response.get('friction_cost', 0)
        })
    
    return results