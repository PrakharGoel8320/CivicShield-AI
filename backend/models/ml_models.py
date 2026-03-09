"""
Machine Learning Models Module
Handles model training, evaluation, and predictions
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.svm import SVR, SVC
from sklearn.metrics import (
    mean_squared_error, r2_score, mean_absolute_error,
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)
from sklearn.preprocessing import StandardScaler
import joblib
from typing import Dict, List, Any, Tuple


class MLModelTrainer:
    """Class for training and evaluating ML models"""
    
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.is_classification = False
    
    def _detect_problem_type(self, y: pd.Series) -> str:
        """Detect if problem is classification or regression"""
        if y.dtype == 'object' or y.nunique() < 20:
            return 'classification'
        return 'regression'
    
    def _get_models(self, problem_type: str, model_types: List[str]) -> Dict:
        """Get model instances based on problem type"""
        if problem_type == 'regression':
            available_models = {
                'linear_regression': LinearRegression(),
                'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
                'decision_tree': DecisionTreeRegressor(random_state=42),
                'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
                'svm': SVR(kernel='rbf')
            }
        else:
            available_models = {
                'logistic_regression': LogisticRegression(random_state=42, max_iter=1000),
                'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
                'decision_tree': DecisionTreeClassifier(random_state=42),
                'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
                'svm': SVC(kernel='rbf', probability=True, random_state=42)
            }
        
        return {k: v for k, v in available_models.items() if k in model_types or model_types == ['all']}
    
    def _evaluate_regression(self, y_true, y_pred) -> Dict[str, float]:
        """Calculate regression metrics"""
        return {
            'mse': float(mean_squared_error(y_true, y_pred)),
            'rmse': float(np.sqrt(mean_squared_error(y_true, y_pred))),
            'mae': float(mean_absolute_error(y_true, y_pred)),
            'r2_score': float(r2_score(y_true, y_pred))
        }
    
    def _evaluate_classification(self, y_true, y_pred, y_pred_proba=None) -> Dict[str, float]:
        """Calculate classification metrics"""
        metrics = {
            'accuracy': float(accuracy_score(y_true, y_pred)),
            'precision': float(precision_score(y_true, y_pred, average='weighted', zero_division=0)),
            'recall': float(recall_score(y_true, y_pred, average='weighted', zero_division=0)),
            'f1_score': float(f1_score(y_true, y_pred, average='weighted', zero_division=0))
        }
        
        # Add ROC AUC for binary classification
        if y_pred_proba is not None and len(np.unique(y_true)) == 2:
            try:
                metrics['roc_auc'] = float(roc_auc_score(y_true, y_pred_proba[:, 1]))
            except:
                pass
        
        return metrics
    
    def train_models(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        model_types: List[str] = ['random_forest'],
        test_size: float = 0.2
    ) -> Dict[str, Any]:
        """Train multiple ML models and return model artifacts and metrics."""
        problem_type = self._detect_problem_type(y)
        self.is_classification = (problem_type == 'classification')

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        models = self._get_models(problem_type, model_types)

        results = {
            'models': {},
            'metrics': {},
            'feature_importance': {},
            'problem_type': problem_type
        }

        for model_name, model in models.items():
            print(f"Training {model_name}...")

            if model_name in ['svm', 'logistic_regression']:
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                y_pred_proba = model.predict_proba(X_test_scaled) if hasattr(model, 'predict_proba') else None
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None

            if problem_type == 'regression':
                metrics = self._evaluate_regression(y_test, y_pred)
            else:
                metrics = self._evaluate_classification(y_test, y_pred, y_pred_proba)

            results['models'][model_name] = model
            results['metrics'][model_name] = metrics

            if hasattr(model, 'feature_importances_'):
                importance = dict(zip(X.columns, model.feature_importances_))
                importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
                results['feature_importance'][model_name] = importance
            elif hasattr(model, 'coef_'):
                importance = dict(zip(X.columns, np.abs(model.coef_.flatten())))
                importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
                results['feature_importance'][model_name] = importance

        # Return preprocessing metadata so prediction can mirror training pipeline.
        results['scaler'] = self.scaler
        results['needs_scaling'] = {
            name: (name in ['svm', 'logistic_regression'])
            for name in models.keys()
        }

        self.models = results['models']
        return results
    
    def cross_validate(self, X: pd.DataFrame, y: pd.Series, model_name: str, cv: int = 5) -> Dict[str, Any]:
        """Perform cross-validation on a model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        model = self.models[model_name]
        
        # Perform cross-validation
        scores = cross_val_score(model, X, y, cv=cv, scoring='r2' if not self.is_classification else 'accuracy')
        
        return {
            'cv_scores': scores.tolist(),
            'mean_score': float(scores.mean()),
            'std_score': float(scores.std())
        }
    
    def save_model(self, model_name: str, filepath: str):
        """Save trained model to disk"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        joblib.dump({
            'model': self.models[model_name],
            'scaler': self.scaler,
            'is_classification': self.is_classification
        }, filepath)
    
    def load_model(self, filepath: str, model_name: str):
        """Load trained model from disk"""
        data = joblib.load(filepath)
        self.models[model_name] = data['model']
        self.scaler = data['scaler']
        self.is_classification = data['is_classification']
