(prompt, engine, n_samples=50):
    """Creates the 3D visualization of response energy"""
    
    # Generate diverse continuations
    continuations = []
    for temp in np.linspace(0.3, 1.5, n_samples):
        for top_p in [0.7, 0.9, 0.95]:
            continuation = engine._generate_with_params(
                prompt, 
                temperature=temp,
                top_p=top_p
            )
            
            # Calculate position in embedding space
            embedding = engine._embed(continuation)
            
            # Reduce to 2D for visualization
            pos_2d = engine._project_to_2d(embedding)  # t-SNE or PCA
            
            # Calculate thermodynamic properties
            friction_cost = engine._calculate_friction(continuation)
            entropy_cost = engine._calculate_entropy(continuation)
            total_cost = 0.7 * entropy_cost + 1.3 * friction_cost
            
            continuations.append({
                'text': continuation[:100] + "...",  # Truncate for display
                'position': pos_2d,
                'friction': friction_cost,
                'entropy': entropy_cost,
                'total_cost': total_cost,
                'generation_params': {'temp': temp, 'top_p': top_p}
            })
    
    # Create 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot each continuation as a point
    xs = [c['position'][0] for c in continuations]
    ys = [c['position'][1] for c in continuations]
    zs = [c['total_cost'] for c in continuations]
    
    # Color by entropy (red = high entropy, blue = low entropy)
    colors = [c['entropy'] for c in continuations]
    
    scatter = ax.scatter(xs, ys, zs, c=colors, cmap='viridis', alpha=0.7)
    
    # Add contour lines showing "valleys" and "peaks"
    # This is the actual basin topology
    
    # Highlight the minimum cost point (the chosen response)
    min_cost_idx = np.argmin(zs)
    ax.scatter(xs[min_cost_idx], ys[min_cost_idx], zs[min_cost_idx], 
               c='red', s=200, marker='*', label='Selected Response')
    
    ax.set_xlabel('Semantic Dimension 1')
    ax.set_ylabel('Semantic Dimension 2')
    ax.set_zlabel('Total Thermodynamic Cost')
    ax.set_title(f'Energy Landscape for: "{prompt[:50]}..."')
    
    plt.colorbar(scatter, label='Entropy Cost')
    plt.legend()
    
    return fig, continuations
