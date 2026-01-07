"""
CladBot - Claude-powered trading agent for pump.fun tokens
"""
import asyncio
import logging
from src.agents.claude_agent import ClaudeAgent
from src.monitors.pumpfun_monitor import PumpFunMonitor
from src.traders.token_trader import TokenTrader
from src.utils.config import load_config
from src.utils.logger import setup_logger

async def main():
    """Main entry point for CladBot"""
    
    # Setup logging
    logger = setup_logger()
    logger.info("🤖 Starting CladBot...")
    
    # Load configuration
    config = load_config()
    
    # Initialize components
    claude_agent = ClaudeAgent(config)
    pumpfun_monitor = PumpFunMonitor(config)
    token_trader = TokenTrader(config)
    
    # Start monitoring and trading loop
    try:
        logger.info("✅ CladBot initialized successfully")
        logger.info("👀 Monitoring pump.fun for trading opportunities...")
        
        async for token_data in pumpfun_monitor.watch_new_tokens():
            # Analyze token with Claude
            analysis = await claude_agent.analyze_token(token_data)
            
            # Execute trade if conditions met
            if analysis.should_trade:
                await token_trader.execute_trade(token_data, analysis)
                
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down CladBot...")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
