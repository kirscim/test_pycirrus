import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from source.core.meteorology.data_manager import MeteorologyDataManager
import os

@pytest.fixture
def data_manager():
    """Fixture für den MeteorologyDataManager."""
    return MeteorologyDataManager()

def test_initialization(data_manager):
    """Test der Initialisierung des MeteorologyDataManager."""
    assert data_manager is not None
    assert isinstance(data_manager, MeteorologyDataManager)
    assert hasattr(data_manager, 'config')

def test_get_available_variables(data_manager):
    """Test des Abrufs der verfügbaren meteorologischen Variablen."""
    variables = data_manager.get_available_variables()
    assert isinstance(variables, list)
    assert len(variables) > 0

@patch('source.core.meteorology.data_manager.ERA5')
@patch('source.core.meteorology.data_manager.ERA5ModelLevel')
def test_download_data(mock_era5_model, mock_era5, data_manager):
    """Test des Downloads von Meteorologiedaten mit gemockten ERA5-Klassen."""
    # Mock setup
    mock_dataset = Mock()
    mock_era5.return_value.open_metdataset.return_value = mock_dataset
    mock_era5_model.return_value.open_metdataset.return_value = mock_dataset

    # Testzeitraum definieren
    start_date = datetime(2024, 1, 1)
    end_date = start_date + timedelta(days=1)
    
    # Test für pressure level data
    data_manager.config['meteorology']['use_model_level'] = False
    data_manager.download_data(start_date, end_date)
    
    # Überprüfen der ERA5 Parameter
    mock_era5.assert_called_once()
    call_args = mock_era5.call_args[1]
    assert 'variables' in call_args
    assert call_args['variables'] == data_manager.get_available_variables()
    assert call_args['pressure_levels'] == [400, 300, 200, 100]
    assert call_args['product_type'] == "reanalysis"
    
    # Reset mocks für model level test
    mock_era5.reset_mock()
    mock_era5_model.reset_mock()
    
    # Test für model level data
    data_manager.config['meteorology']['use_model_level'] = True
    data_manager.download_data(start_date, end_date)
    
    # Überprüfen der ERA5ModelLevel Parameter
    mock_era5_model.assert_called_once()
    call_args = mock_era5_model.call_args[1]
    assert 'variables' in call_args
    assert call_args['variables'] == data_manager.get_available_variables()
    assert call_args['product_type'] == "reanalysis"

@patch('source.core.meteorology.data_manager.pycontrails')
def test_get_data_for_date(mock_pycontrails, data_manager):
    """Test des Abrufs von Meteorologiedaten für ein bestimmtes Datum."""
    # Mock setup
    mock_dataset = Mock()
    mock_dataset.time = [1]
    mock_dataset.latitude = [1]
    mock_dataset.longitude = [1]
    mock_pycontrails.open_dataset.return_value = mock_dataset
    
    # Testdatum definieren
    date = datetime(2024, 1, 1)
    
    # Daten abrufen
    data = data_manager.get_data_for_date(date)
    
    # Überprüfungen
    assert data is not None
    assert hasattr(data, 'time')
    assert hasattr(data, 'latitude')
    assert hasattr(data, 'longitude')
    assert len(data.time) > 0
    assert len(data.latitude) > 0
    assert len(data.longitude) > 0

def test_invalid_date_range(data_manager):
    """Test mit ungültigem Datumsbereich."""
    # Ungültiger Datumsbereich (Ende vor Anfang)
    start_date = datetime(2024, 1, 2)
    end_date = datetime(2024, 1, 1)
    
    with pytest.raises(ValueError):
        data_manager.download_data(start_date, end_date)