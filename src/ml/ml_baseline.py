import pandas as pd
import numpy as np
from pathlib import Path
import typer  # Step 1: Import typer

def make_sample_feature_table(
    root: Path = typer.Option(None, help="The root directory of the project"), 
    n_users: int = typer.Option(50, help="Number of users to generate"), 
    seed: int = typer.Option(42, help="Random seed for reproducibility")
):
    """Write a small, deterministic feature table for local demos."""
    
    # 1. Handle the Root Path
    # If no root is provided, use the current directory
    #base_path = root if root is not None else Path.cwd()
    
    # 2. Define Folder Path (Don't include the filename yet!)
    root = Path(__file__).resolve().parent.parent.parent
    data_folder =  root/ "data" / "processed" 
    
    # 3. Create the directory (the folders) if they don't exist
    data_folder.mkdir(parents=True, exist_ok=True)
    
    # 4. Define the final file path
    output_path = data_folder / "sample_feature.csv"
    
    rng = np.random.default_rng(seed)
    
    # Generate synthetic features
    user_id = [f"u{i:03d}" for i in range(1, n_users + 1)]
    country = rng.choice(["US", "CA", "GB"], size=n_users, replace=True)
    n_orders = rng.integers(1, 10, size=n_users)
    avg_amount = rng.normal(loc=10, scale=3, size=n_users).clip(min=1)
    
    total_amount = n_orders * avg_amount
    is_high_value = (total_amount >= 65).astype(int)
    
    # Build the DataFrame
    df = pd.DataFrame({
        "user_id": user_id,
        "country": country,
        "n_orders": n_orders,
        "avg_amount": avg_amount.round(2),
        "total_amount": total_amount.round(2),
        "is_high_value": is_high_value
    })
    
    # 5. Save to CSV
    df.to_csv(output_path, index=False)

    typer.secho(f"Success! Sample feature table saved to: {output_path}", fg=typer.colors.GREEN)

# Step 2: Make the script runnable from command line
if __name__ == "__main__":
    typer.run(make_sample_feature_table)