#!/usr/bin/env python3

import asyncio
from bittensor.core.metagraph import async_metagraph

async def analyze_metagraph():
    # Create async metagraph
    print("Creating async metagraph...")
    metagraph = await async_metagraph(netuid=1, network="finney", lite=False)
    
    # Perform analysis
    stakes = metagraph.S
    print(f"Total stake: {stakes.sum().item():.2f}")
    
    # Sync to latest block
    print("Syncing to latest block...")
    await metagraph.sync()
    print(f"Synced to block: {metagraph.block.item()}")

async def use_factory():
    print("Using factory function...")
    metagraph = await async_metagraph(netuid=1, sync=True)
    print(f"Factory metagraph has {metagraph.n.item()} neurons")

async def main():
    print("=== Async Metagraph Analysis ===")
    await analyze_metagraph()
    print("\n=== Factory Function Example ===")
    await use_factory()

if __name__ == "__main__":
    # Run async analysis
    asyncio.run(main()) 