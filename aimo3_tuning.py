"""
AIMO3 Tuning Module - Hyperparameter Optimization for Math Problem Solving

This module provides Optuna-based hyperparameter tuning for the AIMO3 competition.
It can be imported by the notebook or run standalone for tuning experiments.

Usage:
    from aimo3_tuning import TuningConfig, run_tuning, load_best_config
    
    # Quick tune
    result = run_tuning(mode="quick")
    
    # Full tune  
    result = run_tuning(mode="full")
    
    # Load saved config
    config = load_best_config()
"""

import os
import json
import time
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Callable
from collections import Counter


@dataclass
class TuningConfig:
    """Configuration for hyperparameter tuning."""
    
    # Search space bounds
    k_min: int = 4
    k_max: int = 16
    temperature_min: float = 0.3
    temperature_max: float = 1.0
    max_tokens_min: int = 1024
    max_tokens_max: int = 4096
    max_tokens_step: int = 512
    top_p_min: float = 0.8
    top_p_max: float = 1.0
    
    # Prompt styles to try
    prompt_styles: List[str] = field(default_factory=lambda: ["strict_final", "tir"])
    
    # Selection strategies to try
    selection_strategies: List[str] = field(default_factory=lambda: [
        "majority_vote", "verifier_weighted", "consensus"
    ])
    
    # Tuning settings
    quick_trials: int = 10
    full_trials: int = 30
    timeout_quick: int = 1800  # 30 min
    timeout_full: int = 3600   # 1 hour
    
    # Paths
    config_save_path: str = "/kaggle/working/best_config.json"
    
    # Evaluation settings
    time_budget_per_problem: float = 180.0
    time_penalty_weight: float = 0.1


def get_search_space(trial, config: TuningConfig = None) -> Dict[str, Any]:
    """
    Define Optuna search space for hyperparameter tuning.
    
    Args:
        trial: Optuna trial object
        config: TuningConfig with search bounds
        
    Returns:
        Dictionary of sampled hyperparameters
    """
    config = config or TuningConfig()
    
    return {
        "k": trial.suggest_int("k", config.k_min, config.k_max),
        "temperature": trial.suggest_float("temperature", config.temperature_min, config.temperature_max),
        "max_new_tokens": trial.suggest_int(
            "max_new_tokens", 
            config.max_tokens_min, 
            config.max_tokens_max, 
            step=config.max_tokens_step
        ),
        "prompt_style": trial.suggest_categorical("prompt_style", config.prompt_styles),
        "selection_strategy": trial.suggest_categorical("selection_strategy", config.selection_strategies),
        "top_p": trial.suggest_float("top_p", config.top_p_min, config.top_p_max),
    }


def create_objective(
    problems_df,
    solve_fn: Callable,
    config: TuningConfig = None
) -> Callable:
    """
    Create Optuna objective function for tuning.
    
    Args:
        problems_df: DataFrame with 'id', 'problem', 'answer' columns
        solve_fn: Function to solve a problem: solve_fn(problem_id, problem_text, config) -> (answer, telemetry)
        config: TuningConfig with tuning settings
        
    Returns:
        Objective function for Optuna
    """
    config = config or TuningConfig()
    n_problems = len(problems_df)
    
    def objective(trial):
        # Sample hyperparameters
        hp_config = get_search_space(trial, config)
        
        correct = 0
        total_time = 0
        
        for idx, row in problems_df.iterrows():
            problem_id = str(row["id"])
            problem_text = row["problem"]
            expected = int(row["answer"])
            
            # Solve with sampled config
            predicted, telemetry = solve_fn(problem_id, problem_text, config=hp_config)
            
            if predicted == expected:
                correct += 1
            
            total_time += telemetry.get("elapsed_sec", 0)
            
            # Report intermediate for pruning
            trial.report(correct / (idx + 1), idx)
            
            if trial.should_prune():
                import optuna
                raise optuna.TrialPruned()
        
        accuracy = correct / n_problems
        avg_time = total_time / n_problems
        
        # Penalize slow configs
        time_penalty = max(0, (avg_time - config.time_budget_per_problem) / config.time_budget_per_problem)
        score = accuracy - config.time_penalty_weight * time_penalty
        
        return score
    
    return objective


def run_tuning(
    problems_df,
    solve_fn: Callable,
    mode: str = "quick",
    config: TuningConfig = None,
    seed: int = 42
) -> Dict[str, Any]:
    """
    Run Optuna hyperparameter tuning.
    
    Args:
        problems_df: DataFrame with reference problems
        solve_fn: Solver function
        mode: "quick" or "full"
        config: TuningConfig
        seed: Random seed
        
    Returns:
        Dictionary with best config and results
    """
    try:
        import optuna
        from optuna.pruners import MedianPruner
        from optuna.samplers import TPESampler
    except ImportError:
        import subprocess
        subprocess.run(["pip", "install", "optuna", "-q"])
        import optuna
        from optuna.pruners import MedianPruner
        from optuna.samplers import TPESampler
    
    config = config or TuningConfig()
    
    n_trials = config.quick_trials if mode == "quick" else config.full_trials
    timeout = config.timeout_quick if mode == "quick" else config.timeout_full
    
    # Create study
    sampler = TPESampler(seed=seed)
    pruner = MedianPruner(n_startup_trials=3, n_warmup_steps=2)
    
    study = optuna.create_study(
        direction="maximize",
        sampler=sampler,
        pruner=pruner,
        study_name=f"aimo3_tuning_{mode}"
    )
    
    objective = create_objective(problems_df, solve_fn, config)
    
    print(f"Starting {mode} tuning: {n_trials} trials, {timeout}s timeout")
    
    try:
        study.optimize(objective, n_trials=n_trials, timeout=timeout, show_progress_bar=True)
    except KeyboardInterrupt:
        print("Tuning interrupted")
    
    # Get results
    best_config = study.best_params
    best_score = study.best_value
    
    result = {
        "best_config": best_config,
        "best_score": best_score,
        "n_trials": len(study.trials),
        "mode": mode,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    # Save config
    with open(config.config_save_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\nBest config (score={best_score:.4f}):")
    for k, v in best_config.items():
        print(f"  {k}: {v}")
    
    return result


def load_best_config(path: str = None) -> Dict[str, Any]:
    """Load best config from previous tuning run."""
    path = path or "/kaggle/working/best_config.json"
    
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
        return data.get("best_config", {})
    
    return {}


# Default configurations for different scenarios
DEFAULT_CONFIGS = {
    "conservative": {
        "k": 8,
        "temperature": 0.5,
        "max_new_tokens": 2048,
        "prompt_style": "strict_final",
        "selection_strategy": "consensus",
        "top_p": 0.9,
    },
    "exploratory": {
        "k": 12,
        "temperature": 0.8,
        "max_new_tokens": 3072,
        "prompt_style": "strict_final",
        "selection_strategy": "verifier_weighted",
        "top_p": 0.95,
    },
    "fast": {
        "k": 4,
        "temperature": 0.3,
        "max_new_tokens": 1024,
        "prompt_style": "tir",
        "selection_strategy": "majority_vote",
        "top_p": 0.9,
    },
}


if __name__ == "__main__":
    print("AIMO3 Tuning Module")
    print("===================")
    print("\nDefault configs available:")
    for name, cfg in DEFAULT_CONFIGS.items():
        print(f"\n{name}:")
        for k, v in cfg.items():
            print(f"  {k}: {v}")
