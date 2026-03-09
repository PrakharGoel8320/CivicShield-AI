"""
Feature Engineering Utilities
Creates new features and transforms existing ones
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from datetime import datetime
from typing import List


class FeatureEngineer:
    """Class for feature engineering operations"""
    
    def create_date_features(self, df: pd.DataFrame, date_column: str) -> pd.DataFrame:
        """
        Extract features from date column
        
        Args:
            df: Input DataFrame
            date_column: Name of date column
        
        Returns:
            DataFrame with additional date features
        """
        df_features = df.copy()
        
        # Convert to datetime
        df_features[date_column] = pd.to_datetime(df_features[date_column], errors='coerce')
        
        # Extract features
        df_features[f'{date_column}_year'] = df_features[date_column].dt.year
        df_features[f'{date_column}_month'] = df_features[date_column].dt.month
        df_features[f'{date_column}_day'] = df_features[date_column].dt.day
        df_features[f'{date_column}_dayofweek'] = df_features[date_column].dt.dayofweek
        df_features[f'{date_column}_quarter'] = df_features[date_column].dt.quarter
        df_features[f'{date_column}_week'] = df_features[date_column].dt.isocalendar().week
        df_features[f'{date_column}_is_weekend'] = df_features[date_column].dt.dayofweek.isin([5, 6]).astype(int)
        
        return df_features
    
    def create_polynomial_features(self, df: pd.DataFrame, columns: List[str], degree: int = 2) -> pd.DataFrame:
        """
        Create polynomial features
        
        Args:
            df: Input DataFrame
            columns: Columns to create polynomial features for
            degree: Polynomial degree
        
        Returns:
            DataFrame with polynomial features
        """
        df_poly = df.copy()
        
        poly = PolynomialFeatures(degree=degree, include_bias=False)
        poly_features = poly.fit_transform(df_poly[columns])
        
        # Create feature names
        feature_names = poly.get_feature_names_out(columns)
        
        # Add to DataFrame
        poly_df = pd.DataFrame(poly_features, columns=feature_names, index=df_poly.index)
        
        # Remove original columns to avoid duplication
        df_poly = df_poly.drop(columns=columns)
        df_poly = pd.concat([df_poly, poly_df], axis=1)
        
        return df_poly
    
    def create_interaction_features(self, df: pd.DataFrame, col1: str, col2: str) -> pd.DataFrame:
        """Create interaction feature between two columns"""
        df_interaction = df.copy()
        df_interaction[f'{col1}_x_{col2}'] = df_interaction[col1] * df_interaction[col2]
        
        return df_interaction
    
    def create_aggregation_features(self, df: pd.DataFrame, group_col: str, agg_col: str, agg_funcs: List[str] = ['mean', 'sum', 'std']) -> pd.DataFrame:
        """
        Create aggregation features
        
        Args:
            df: Input DataFrame
            group_col: Column to group by
            agg_col: Column to aggregate
            agg_funcs: Aggregation functions
        
        Returns:
            DataFrame with aggregation features
        """
        df_agg = df.copy()
        
        for func in agg_funcs:
            agg_data = df.groupby(group_col)[agg_col].transform(func)
            df_agg[f'{agg_col}_{func}_by_{group_col}'] = agg_data
        
        return df_agg
    
    def create_ratio_features(self, df: pd.DataFrame, numerator: str, denominator: str) -> pd.DataFrame:
        """Create ratio feature"""
        df_ratio = df.copy()
        df_ratio[f'{numerator}_div_{denominator}'] = df_ratio[numerator] / (df_ratio[denominator] + 1e-10)
        
        return df_ratio
    
    def create_binning_features(self, df: pd.DataFrame, column: str, bins: int = 5) -> pd.DataFrame:
        """Create binned categorical feature from numerical column"""
        df_binned = df.copy()
        df_binned[f'{column}_binned'] = pd.qcut(df_binned[column], q=bins, labels=False, duplicates='drop')
        
        return df_binned
    
    def create_lag_features(self, df: pd.DataFrame, column: str, lags: List[int] = [1, 2, 3]) -> pd.DataFrame:
        """Create lag features for time series"""
        df_lag = df.copy()
        
        for lag in lags:
            df_lag[f'{column}_lag_{lag}'] = df_lag[column].shift(lag)
        
        return df_lag
    
    def create_rolling_features(self, df: pd.DataFrame, column: str, windows: List[int] = [3, 7, 14]) -> pd.DataFrame:
        """Create rolling window features"""
        df_rolling = df.copy()
        
        for window in windows:
            df_rolling[f'{column}_rolling_mean_{window}'] = df_rolling[column].rolling(window=window).mean()
            df_rolling[f'{column}_rolling_std_{window}'] = df_rolling[column].rolling(window=window).std()
        
        return df_rolling
