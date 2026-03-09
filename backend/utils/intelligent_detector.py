"""
Intelligent Target and Feature Detector
Automatically identifies target columns and relevant features from CSV data
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
import logging

logger = logging.getLogger(__name__)


class IntelligentDetector:
    """Automatically detect target columns and features from datasets"""
    
    # Keywords that indicate a column is likely a target
    TARGET_KEYWORDS = [
        'risk', 'level', 'severity', 'class', 'category', 'grade',
        'prediction', 'forecast', 'count', 'incidents', 'rate',
        'score', 'index', 'status', 'condition', 'quality',
        'detected', 'present', 'pothole', 'damage', 'alert'
    ]
    
    # Keywords that indicate a column should NOT be a target (metadata)
    EXCLUDE_KEYWORDS = [
        'id', 'name', 'date', 'time', 'timestamp', 'location',
        'address', 'street', 'city', 'coordinates', 'lat', 'lon',
        'longitude', 'latitude', 'zone', 'area', 'district'
    ]
    
    def __init__(self):
        self.target_column = None
        self.feature_columns = []
        self.column_scores = {}
    
    def detect_target_column(self, df: pd.DataFrame) -> str:
        """
        Automatically detect the most likely target column
        
        Strategy:
        1. Check for explicit target indicators in column names
        2. Analyze column data characteristics
        3. Prefer columns with limited unique values (classification)
        4. Consider column position (rightmost often target)
        """
        scores = {}
        
        for col in df.columns:
            score = 0
            col_lower = col.lower().replace('_', ' ')
            
            # Check if column should be excluded
            if any(keyword in col_lower for keyword in self.EXCLUDE_KEYWORDS):
                scores[col] = -1000
                continue
            
            # Keyword matching (highest priority)
            for keyword in self.TARGET_KEYWORDS:
                if keyword in col_lower:
                    score += 50
                    break
            
            # Check data characteristics
            dtype = df[col].dtype
            unique_count = df[col].nunique()
            total_count = len(df)
            unique_ratio = unique_count / total_count
            
            # Numerical columns are better candidates
            if pd.api.types.is_numeric_dtype(dtype):
                score += 20
                
                # Classification targets typically have fewer unique values
                if unique_count <= 10:
                    score += 30
                elif unique_count <= 20:
                    score += 20
                elif unique_count <= 50:
                    score += 10
                
                # Check if values look like categories (integers 0-10)
                if df[col].dtype in [np.int64, np.int32]:
                    min_val = df[col].min()
                    max_val = df[col].max()
                    if 0 <= min_val <= 1 and max_val <= 10:
                        score += 15
            
            # Categorical columns can also be targets
            elif pd.api.types.is_object_dtype(dtype) or pd.api.types.is_categorical_dtype(dtype):
                if unique_count <= 20:
                    score += 25
            
            # Position bonus - rightmost columns often targets
            col_position = list(df.columns).index(col)
            if col_position >= len(df.columns) - 3:
                score += 5
            
            scores[col] = score
        
        self.column_scores = scores
        
        # Select column with highest score
        if not scores:
            raise ValueError("No suitable target column found")
        
        target = max(scores.items(), key=lambda x: x[1])
        
        if target[1] <= 0:
            raise ValueError(f"Could not confidently detect target column. Scores: {scores}")
        
        logger.info(f"🎯 Auto-detected target: '{target[0]}' (score: {target[1]})")
        logger.info(f"   Column scores: {scores}")
        
        self.target_column = target[0]
        return target[0]
    
    def detect_feature_columns(
        self, 
        df: pd.DataFrame, 
        target_column: str,
        max_features: Optional[int] = None
    ) -> List[str]:
        """
        Automatically select relevant feature columns
        
        Strategy:
        1. Exclude metadata columns (IDs, names, dates)
        2. Calculate feature importance using mutual information
        3. Remove highly correlated features
        4. Return ranked features
        """
        # Start with all columns except target
        potential_features = [col for col in df.columns if col != target_column]
        
        # Filter out metadata columns
        features = []
        for col in potential_features:
            col_lower = col.lower().replace('_', ' ')
            
            # Skip metadata columns
            if any(keyword in col_lower for keyword in self.EXCLUDE_KEYWORDS):
                logger.info(f"   ⊗ Excluding metadata column: '{col}'")
                continue
            
            # Skip non-numeric columns for now (can be enhanced later)
            if not pd.api.types.is_numeric_dtype(df[col].dtype):
                logger.info(f"   ⊗ Excluding non-numeric column: '{col}'")
                continue
            
            # Skip columns with too many missing values
            missing_ratio = df[col].isnull().sum() / len(df)
            if missing_ratio > 0.5:
                logger.info(f"   ⊗ Excluding column with high missing values: '{col}' ({missing_ratio:.1%})")
                continue
            
            features.append(col)
        
        if not features:
            raise ValueError("No suitable feature columns found")
        
        # Calculate feature importance using mutual information
        X = df[features].fillna(df[features].median())
        y = df[target_column]
        
        # Determine if classification or regression
        is_classification = df[target_column].nunique() <= 20
        
        if is_classification:
            importance = mutual_info_classif(X, y, random_state=42)
        else:
            importance = mutual_info_regression(X, y, random_state=42)
        
        # Rank features by importance
        feature_importance = sorted(
            zip(features, importance),
            key=lambda x: x[1],
            reverse=True
        )
        
        logger.info(f"📊 Feature importance ranking:")
        for feat, imp in feature_importance[:10]:
            logger.info(f"   {feat}: {imp:.4f}")
        
        # Select top features
        if max_features:
            selected_features = [f for f, _ in feature_importance[:max_features]]
        else:
            # Select features with importance > threshold
            threshold = np.mean(importance) * 0.5
            selected_features = [f for f, imp in feature_importance if imp > threshold]
            
            # Ensure at least 3 features
            if len(selected_features) < 3:
                selected_features = [f for f, _ in feature_importance[:min(5, len(features))]]
        
        logger.info(f"✅ Selected {len(selected_features)} features: {selected_features}")
        
        self.feature_columns = selected_features
        return selected_features
    
    def auto_detect(
        self, 
        df: pd.DataFrame,
        max_features: Optional[int] = None
    ) -> Tuple[str, List[str]]:
        """
        Automatically detect both target and features
        
        Returns:
            (target_column, feature_columns)
        """
        logger.info("🔍 Starting intelligent auto-detection...")
        
        target = self.detect_target_column(df)
        features = self.detect_feature_columns(df, target, max_features)
        
        logger.info(f"✨ Auto-detection complete!")
        logger.info(f"   Target: {target}")
        logger.info(f"   Features: {len(features)} columns")
        
        return target, features
    
    def get_model_recommendations(self, df: pd.DataFrame, target_column: str) -> List[str]:
        """
        Recommend best models based on data characteristics
        
        Returns:
            List of recommended model names
        """
        recommendations = []
        
        # Check if classification or regression
        unique_values = df[target_column].nunique()
        is_classification = unique_values <= 20
        
        if is_classification:
            # Classification models
            if unique_values <= 2:
                # Binary classification
                recommendations = [
                    'logistic_regression',
                    'random_forest',
                    'gradient_boosting',
                    'svm'
                ]
            else:
                # Multi-class classification
                recommendations = [
                    'random_forest',
                    'gradient_boosting',
                    'decision_tree',
                    'logistic_regression'
                ]
        else:
            # Regression models
            recommendations = [
                'random_forest',
                'gradient_boosting',
                'linear_regression',
                'decision_tree'
            ]
        
        logger.info(f"🤖 Recommended models: {recommendations}")
        return recommendations
