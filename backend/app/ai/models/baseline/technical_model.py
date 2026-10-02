from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import numpy as np

def create_technical_baseline_model() -> Pipeline:
    """
    Creates the baseline Technical-Only model (Logistic Regression).
    Pipeline includes imputation for missing values and scaling.
    """
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
    ])
    return pipeline

def get_majority_class_prediction(y_train: np.ndarray, n_test: int) -> np.ndarray:
    """Trivial baseline: predicts the majority class of the training set for all test samples."""
    values, counts = np.unique(y_train[~np.isnan(y_train)], return_counts=True)
    majority_class = values[np.argmax(counts)]
    return np.full(n_test, majority_class)

def get_persistence_prediction(y_test_previous: np.ndarray) -> np.ndarray:
    """Trivial baseline: predicts the previous period's direction."""
    return y_test_previous
