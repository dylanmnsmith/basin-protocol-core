class MinimalBasinEngine:
    """Lightweight test implementation for small models"""
    
    def __init__(self, model_size='phi-2'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_size)
        self.model = AutoModelForCausalLM.from_pretrained(model_size)
        self.friction_field = self._initialize_friction_from_hh_rlhf()  # Using Anthropic's data
        
    def simulate_consequence(self, prompt, n_simulations=3):
        """Runs the consequence loop on a single prompt"""
        consequences = []
        for _ in range(n_simulations):
            # Generate continuation (our "action")
            with torch.no_grad():
                outputs = self.model.generate(
                    **self.tokenizer(prompt, return_tensors='pt'),
                    max_new_tokens=50,
                    do_sample=True  # Stochastic for path variation
                )
            
            continuation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Calculate thermodynamic cost
            friction_cost = self._calculate_friction(continuation)
            entropy_cost = self._calculate_entropy(continuation)
            
            consequences.append({
                'continuation': continuation,
                'friction': friction_cost,
                'entropy': entropy_cost,
                'total_cost': 0.7 * entropy_cost + 1.3 * friction_cost
            })
        
        # Return continuation with minimum cost
        return min(consequences, key=lambda x: x['total_cost'])

