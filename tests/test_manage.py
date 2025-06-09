from unittest.mock import patch, MagicMock
import pytest
import os
from flow_3d.manage import main

@pytest.fixture
def portfolio_path(tmp_path):
    return tmp_path / "test_workspace"

@patch('flow_3d.Portfolio')  # Order matters - innermost decorator is executed first
@patch('argparse.ArgumentParser')
def test_workspace_init_creates_folder(mock_argparser, portfolio_path):
    # Setup mock parser
    mock_parser = MagicMock()
    mock_argparser.return_value = mock_parser
    mock_args = MagicMock()
    mock_args.method = "workspace_init"
    mock_args.portfolio_path = str(portfolio_path)
    mock_args.verbose = False
    mock_parser.parse_known_args.return_value = (mock_args, [])
    
    # Execute main
    main()
    
    # Verify the directory was created
    assert os.path.exists(portfolio_path)
    assert os.path.isdir(portfolio_path)
    
    # Optional: Verify specific files/folders were created inside
    workspace_dir = os.path.join(portfolio_path, os.listdir(portfolio_path)[0])  # Get first subdirectory
    assert os.path.exists(workspace_dir)
    assert os.path.isfile(os.path.join(workspace_dir, 'manage.py'))
