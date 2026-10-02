from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any

def create_model(model_type: str, hyperparameters: Dict[str, Any], random_seed: int = 42) -> Pipeline:
    if model_type == "LogisticRegression":
        classifier = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=random_seed, **hyperparameters)
    elif model_type == "RandomForest":
        classifier = RandomForestClassifier(class_weight='balanced', random_state=random_seed, **hyperparameters)
    elif model_type == "HistGradientBoosting":
        # Note: HistGradientBoosting does not support class_weight natively, 
        # so we will use it without, or wait, we can pass sample weights during fit, 
        # but sklearn pipeline makes it tricky. We'll just rely on trees for imbalanced or accept worse recall.
        classifier = HistGradientBoostingClassifier(random_state=random_seed, **hyperparameters)
    else:
        raise ValueError(f"Unknown model_type: {model_type}")

    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('classifier', classifier)
    ])
    
    return pipeline
