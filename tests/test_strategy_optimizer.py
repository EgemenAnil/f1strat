"""
Test Strategy Optimizer
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.strategy_optimizer import StrategyOptimizer


class TestStrategyOptimizer:
    """Test strategy optimizer functionality."""
    
    @pytest.fixture
    def optimizer(self):
        """Create optimizer instance."""
        return StrategyOptimizer(track_name='Bahrain', total_laps=57)
    
    def test_optimizer_init(self, optimizer):
        """Test optimizer initialization."""
        assert optimizer.track_name == 'Bahrain'
        assert optimizer.total_laps == 57
        assert optimizer.strategies is not None
    
    def test_generate_strategies(self, optimizer):
        """Test strategy generation."""
        strategies = optimizer.generate_strategies()
        
        assert len(strategies) > 0
        assert len(strategies) <= 100  # Max strategies
        
        # Check strategy structure
        for strategy in strategies[:5]:
            assert hasattr(strategy, 'name')
            assert hasattr(strategy, 'compounds')
            assert hasattr(strategy, 'pit_laps')
    
    def test_strategy_validity(self, optimizer):
        """Test that generated strategies are valid."""
        strategies = optimizer.generate_strategies()
        
        for strategy in strategies:
            # Pit laps should be within race bounds
            for pit_lap in strategy.pit_laps:
                assert 1 <= pit_lap <= optimizer.total_laps
            
            # Should have compounds
            assert len(strategy.compounds) > 0
    
    def test_different_tracks(self):
        """Test optimizer works with different tracks."""
        tracks = ['Monaco', 'Monza', 'Spa', 'Silverstone']
        
        for track in tracks:
            opt = StrategyOptimizer(track_name=track, total_laps=50)
            strategies = opt.generate_strategies()
            assert len(strategies) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
