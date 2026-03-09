"""
Data Preprocessing Utilities
Handles data cleaning, transformation, and preparation
"""

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from typing import List, Dict, Any


class DataPreprocessor:
    """Class for data preprocessing operations"""
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
    
    def handle_missing_values(self, df: pd.DataFrame, method: str = 'mean') -> pd.DataFrame:
        """
        Handle missing values in DataFrame
        
        Args:
            df: Input DataFrame
            method: 'mean', 'median', 'mode', 'drop', 'forward_fill', 'backward_fill'
        
        Returns:
            DataFrame with missing values handled
        """
        df_clean = df.copy()
        
        if method == 'drop':
            df_clean = df_clean.dropna()
        
        elif method == 'forward_fill':
            df_clean = df_clean.fillna(method='ffill')
        
        elif method == 'backward_fill':
            df_clean = df_clean.fillna(method='bfill')
        
        else:
            # Handle numerical columns
            numerical_cols = df_clean.select_dtypes(include=[np.number]).columns
            
            if len(numerical_cols) > 0:
                if method == 'mean':
                    imputer = SimpleImputer(strategy='mean')
                elif method == 'median':
                    imputer = SimpleImputer(strategy='median')
                else:
                    imputer = SimpleImputer(strategy='mean')
                
                df_clean[numerical_cols] = imputer.fit_transform(df_clean[numerical_cols])
            
            # Handle categorical columns
            categorical_cols = df_clean.select_dtypes(include=['object']).columns
            
            if len(categorical_cols) > 0:
                imputer = SimpleImputer(strategy='most_frequent')
                df_clean[categorical_cols] = imputer.fit_transform(df_clean[categorical_cols])
        
        return df_clean
    
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows"""
        return df.drop_duplicates()
    
    def handle_outliers(self, df: pd.DataFrame, method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
        """
        Handle outliers in numerical columns
        
        Args:
            df: Input DataFrame
            method: 'iqr' or 'zscore'
            threshold: IQR multiplier or z-score threshold
        
        Returns:
            DataFrame with outliers handled
        """
        df_clean = df.copy()
        numerical_cols = df_clean.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if method == 'iqr':
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                # Cap outliers instead of removing
                df_clean[col] = df_clean[col].clip(lower_bound, upper_bound)
            
            elif method == 'zscore':
                mean = df_clean[col].mean()
                std = df_clean[col].std()
                
                z_scores = np.abs((df_clean[col] - mean) / std)
                df_clean = df_clean[z_scores < threshold]
        
        return df_clean
    
    def scale_features(self, df: pd.DataFrame, method: str = 'standard', columns: List[str] = None) -> pd.DataFrame:
        """
        Scale numerical features
        
        Args:
            df: Input DataFrame
            method: 'standard' or 'minmax'
            columns: Columns to scale (if None, scales all numerical columns)
        
        Returns:
            DataFrame with scaled features
        """
        df_scaled = df.copy()
        
        if columns is None:
            columns = df_scaled.select_dtypes(include=[np.number]).columns.tolist()
        
        if method == 'standard':
            scaler = StandardScaler()
        else:
            scaler = MinMaxScaler()
        
        df_scaled[columns] = scaler.fit_transform(df_scaled[columns])
        self.scalers[method] = scaler
        
        return df_scaled
    
    def encode_categorical(self, df: pd.DataFrame, columns: List[str] = None, method: str = 'label') -> pd.DataFrame:
        """
        Encode categorical variables
        
        Args:
            df: Input DataFrame
            columns: Columns to encode (if None, encodes all object columns)
            method: 'label' or 'onehot'
        
        Returns:
            DataFrame with encoded categorical variables
        """
        df_encoded = df.copy()
        
        if columns is None:
            columns = df_encoded.select_dtypes(include=['object']).columns.tolist()
        
        if method == 'label':
            for col in columns:
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
                self.encoders[col] = le
        
        elif method == 'onehot':
            df_encoded = pd.get_dummies(df_encoded, columns=columns, drop_first=True)
        
        return df_encoded
    
    def create_bins(self, df: pd.DataFrame, column: str, bins: int = 5, labels: List[str] = None) -> pd.DataFrame:
        """Create bins for continuous variable"""
        df_binned = df.copy()
        
        if labels is None:
            labels = [f'bin_{i}' for i in range(bins)]
        
        df_binned[f'{column}_binned'] = pd.cut(df_binned[column], bins=bins, labels=labels)
        
        return df_binned
    
    def remove_low_variance(self, df: pd.DataFrame, threshold: float = 0.01) -> pd.DataFrame:
        """Remove features with low variance"""
        df_clean = df.copy()
        numerical_cols = df_clean.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if df_clean[col].var() < threshold:
                df_clean = df_clean.drop(columns=[col])
        
        return df_clean
    
    def detect_and_handle_skewness(self, df: pd.DataFrame, threshold: float = 1.0) -> pd.DataFrame:
        """Detect and handle skewed distributions"""
        df_transformed = df.copy()
        numerical_cols = df_transformed.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            skewness = df_transformed[col].skew()
            
            if abs(skewness) > threshold:
                # Apply log transformation if values are positive
                if (df_transformed[col] > 0).all():
                    df_transformed[col] = np.log1p(df_transformed[col])
        
        return df_transformed
