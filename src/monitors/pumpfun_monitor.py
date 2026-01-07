"""
Monitor pump.fun for new token launches and updates
"""
import asyncio
from typing import AsyncIterator, Dict, Any
import aiohttp

class PumpFunMonitor:
    """Monitors pump.fun for trading opportunities"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_url = config.get('pumpfun_api_url', 'https://api.pump.fun')
        self.check_interval = config.get('check_interval_seconds', 10)
        self.seen_tokens = set()
        
    async def watch_new_tokens(self) -> AsyncIterator[Dict[str, Any]]:
        """
        Continuously watch for new tokens on pump.fun
        
        Yields:
            Token data for newly discovered tokens
        """
        while True:
            try:
                tokens = await self._fetch_recent_tokens()
                
                for token in tokens:
                    if token['address'] not in self.seen_tokens:
                        self.seen_tokens.add(token['address'])
                        yield token
                        
            except Exception as e:
                print(f"Error fetching tokens: {e}")
                
            await asyncio.sleep(self.check_interval)
    
    async def _fetch_recent_tokens(self) -> list[Dict[str, Any]]:
        """Fetch recent tokens from pump.fun API"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}/tokens/recent") as response:
                if response.status == 200:
                    return await response.json()
                return []
    
    async def get_token_details(self, token_address: str) -> Dict[str, Any]:
        """Get detailed information about a specific token"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/tokens/{token_address}"
            ) as response:
                if response.status == 200:
                    return await response.json()
                return {}
