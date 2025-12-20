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