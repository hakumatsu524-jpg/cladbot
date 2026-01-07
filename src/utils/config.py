"""
Configuration management
"""
import os
import yaml
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Load configuration from file and environment"""
    
    # Load from YAML
    config_path = os.getenv('CONFIG_PATH', 'config/config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Override with environment variables
    config['anthropic_api_key'] = os.getenv('ANTHROPIC_API_KEY')
    config['solana_rpc_url'] = os.getenv('SOLANA_RPC_URL')
    config['wallet_private_key'] = os.getenv('WALLET_PRIVATE_KEY')
    config['pumpfun_api_key'] = os.getenv('PUMPFUN_API_KEY')
    
    return config
