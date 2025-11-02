"""
Advanced ML models for F1 race prediction.
Uses XGBoost and Neural Networks for lap time prediction.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader


class LapTimeDataset(Dataset):
    """PyTorch dataset for lap time prediction."""
    
    def __init__(self, X: np.ndarray, y: np.ndarray):
        """Initialize dataset."""
        self.X = torch.FloatTensor(X)
        self.y = torch.FloatTensor(y)
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


class LapTimeNN(nn.Module):
    """Neural Network for lap time prediction."""
    
    def __init__(self, input_dim: int, hidden_dims: List[int] = [256, 128, 64]):
        """
        Initialize neural network.
        
        Args:
            input_dim: Number of input features
            hidden_dims: List of hidden layer dimensions
        """
        super(LapTimeNN, self).__init__()
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.2)
            ])
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, 1))
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)


class F1RacePredictor:
    """Advanced F1 race prediction model."""
    
    def __init__(self, model_type: str = 'xgboost'):
        """
        Initialize predictor.
        
        Args:
            model_type: 'xgboost', 'neural_network', or 'ensemble'
        """
        self.model_type = model_type
        self.scaler = StandardScaler()
        self.model = None
        self.feature_names = None
        self.feature_importance = None
        
        # Model hyperparameters
        self.xgb_params = {
            'objective': 'reg:squarederror',
            'max_depth': 8,
            'learning_rate': 0.05,
            'n_estimators': 500,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'min_child_weight': 3,
            'gamma': 0.1,
            'reg_alpha': 0.1,
            'reg_lambda': 1.0,
            'random_state': 42
        }
        
        self.nn_params = {
            'hidden_dims': [256, 128, 64],
            'learning_rate': 0.001,
            'batch_size': 64,
            'epochs': 100,
            'early_stopping_patience': 10
        }
    
    def prepare_features(self, df: pd.DataFrame, 
                        target_col: str = 'LapTimeSeconds') -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Prepare features for training.
        
        Args:
            df: Input DataFrame
            target_col: Target column name
        
        Returns:
            Tuple of (X, y, feature_names)
        """
        # Select features
        exclude_cols = [
            target_col, 'Time', 'Driver', 'Team', 'LapTime', 
            'IsPersonalBest', 'Sector1Time', 'Sector2Time', 'Sector3Time',
            'IsAccurate', 'PitOutTime', 'PitInTime'
        ]
        
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        # Handle categorical variables
        X = df[feature_cols].copy()
        
        # Convert any remaining object columns
        for col in X.columns:
            if X[col].dtype == 'object':
                X[col] = pd.Categorical(X[col]).codes
        
        # Fill NaN values
        X = X.fillna(X.mean())
        
        # Get target
        y = df[target_col].values
        
        return X.values, y, feature_cols
    
    def train_xgboost(self, X_train: np.ndarray, y_train: np.ndarray,
                     X_val: np.ndarray, y_val: np.ndarray) -> xgb.XGBRegressor:
        """
        Train XGBoost model.
        
        Args:
            X_train: Training features
            y_train: Training targets
            X_val: Validation features
            y_val: Validation targets
        
        Returns:
            Trained XGBoost model
        """
        print("Training XGBoost model...")
        
        model = xgb.XGBRegressor(**self.xgb_params)
        
        model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            verbose=False
        )
        
        # Store feature importance
        self.feature_importance = model.feature_importances_
        
        return model
    
    def train_neural_network(self, X_train: np.ndarray, y_train: np.ndarray,
                           X_val: np.ndarray, y_val: np.ndarray) -> LapTimeNN:
        """
        Train neural network model.
        
        Args:
            X_train: Training features
            y_train: Training targets
            X_val: Validation features
            y_val: Validation targets
        
        Returns:
            Trained neural network
        """
        print("Training Neural Network...")
        
        # Create datasets
        train_dataset = LapTimeDataset(X_train, y_train)
        val_dataset = LapTimeDataset(X_val, y_val)
        
        train_loader = DataLoader(
            train_dataset, 
            batch_size=self.nn_params['batch_size'],
            shuffle=True
        )
        val_loader = DataLoader(
            val_dataset,
            batch_size=self.nn_params['batch_size'],
            shuffle=False
        )
        
        # Initialize model
        model = LapTimeNN(
            input_dim=X_train.shape[1],
            hidden_dims=self.nn_params['hidden_dims']
        )
        
        # Loss and optimizer
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=self.nn_params['learning_rate'])
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=5
        )
        
        # Training loop
        best_val_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(self.nn_params['epochs']):
            # Training
            model.train()
            train_loss = 0
            for batch_X, batch_y in train_loader:
                optimizer.zero_grad()
                predictions = model(batch_X).squeeze()
                loss = criterion(predictions, batch_y)
                loss.backward()
                optimizer.step()
                train_loss += loss.item()
            
            # Validation
            model.eval()
            val_loss = 0
            with torch.no_grad():
                for batch_X, batch_y in val_loader:
                    predictions = model(batch_X).squeeze()
                    loss = criterion(predictions, batch_y)
                    val_loss += loss.item()
            
            avg_val_loss = val_loss / len(val_loader)
            scheduler.step(avg_val_loss)
            
            # Early stopping
            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                patience_counter = 0
                best_model_state = model.state_dict().copy()
            else:
                patience_counter += 1
            
            if patience_counter >= self.nn_params['early_stopping_patience']:
                print(f"Early stopping at epoch {epoch+1}")
                break
            
            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch+1}: Train Loss = {train_loss/len(train_loader):.4f}, "
                      f"Val Loss = {avg_val_loss:.4f}")
        
        # Load best model
        model.load_state_dict(best_model_state)
        
        return model
    
    def train(self, df: pd.DataFrame, target_col: str = 'LapTimeSeconds',
             test_size: float = 0.2) -> Dict[str, float]:
        """
        Train the model.
        
        Args:
            df: Training data
            target_col: Target column name
            test_size: Test set size
        
        Returns:
            Dictionary with training metrics
        """
        # Prepare features
        X, y, feature_names = self.prepare_features(df, target_col)
        self.feature_names = feature_names
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model based on type
        if self.model_type == 'xgboost':
            self.model = self.train_xgboost(
                X_train_scaled, y_train,
                X_test_scaled, y_test
            )
        elif self.model_type == 'neural_network':
            self.model = self.train_neural_network(
                X_train_scaled, y_train,
                X_test_scaled, y_test
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        # Evaluate
        metrics = self.evaluate(X_test_scaled, y_test)
        
        return metrics
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            X: Input features
        
        Returns:
            Predictions
        """
        X_scaled = self.scaler.transform(X)
        
        if self.model_type == 'xgboost':
            return self.model.predict(X_scaled)
        elif self.model_type == 'neural_network':
            self.model.eval()
            with torch.no_grad():
                X_tensor = torch.FloatTensor(X_scaled)
                predictions = self.model(X_tensor).squeeze().numpy()
            return predictions
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            X: Input features
            y: True targets
        
        Returns:
            Dictionary with metrics
        """
        predictions = self.predict(X)
        
        metrics = {
            'mae': mean_absolute_error(y, predictions),
            'rmse': np.sqrt(mean_squared_error(y, predictions)),
            'r2': r2_score(y, predictions),
            'mape': np.mean(np.abs((y - predictions) / y)) * 100
        }
        
        print("\nModel Performance:")
        print(f"  MAE:  {metrics['mae']:.3f} seconds")
        print(f"  RMSE: {metrics['rmse']:.3f} seconds")
        print(f"  R²:   {metrics['r2']:.4f}")
        print(f"  MAPE: {metrics['mape']:.2f}%")
        
        return metrics
    
    def get_feature_importance(self, top_n: int = 20) -> pd.DataFrame:
        """
        Get feature importance.
        
        Args:
            top_n: Number of top features to return
        
        Returns:
            DataFrame with feature importance
        """
        if self.model_type != 'xgboost':
            print("Feature importance only available for XGBoost models")
            return None
        
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.feature_importance
        }).sort_values('importance', ascending=False)
        
        return importance_df.head(top_n)
    
    def save(self, filepath: str):
        """Save model to disk."""
        save_dict = {
            'model_type': self.model_type,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'feature_importance': self.feature_importance
        }
        
        if self.model_type == 'xgboost':
            save_dict['model'] = self.model
        elif self.model_type == 'neural_network':
            save_dict['model_state'] = self.model.state_dict()
            save_dict['nn_params'] = self.nn_params
        
        joblib.dump(save_dict, filepath)
        print(f"Model saved to {filepath}")
    
    def load(self, filepath: str):
        """Load model from disk."""
        save_dict = joblib.load(filepath)
        
        self.model_type = save_dict['model_type']
        self.scaler = save_dict['scaler']
        self.feature_names = save_dict['feature_names']
        self.feature_importance = save_dict.get('feature_importance')
        
        if self.model_type == 'xgboost':
            self.model = save_dict['model']
        elif self.model_type == 'neural_network':
            self.nn_params = save_dict['nn_params']
            input_dim = len(self.feature_names)
            self.model = LapTimeNN(input_dim, self.nn_params['hidden_dims'])
            self.model.load_state_dict(save_dict['model_state'])
            self.model.eval()
        
        print(f"Model loaded from {filepath}")


if __name__ == "__main__":
    print("F1 Race Predictor - Test Mode")
    print("This module requires training data to demonstrate.")
