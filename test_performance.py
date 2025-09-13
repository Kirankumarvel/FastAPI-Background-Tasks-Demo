import asyncio
import time
import httpx
import statistics

async def test_endpoint(url, data, num_requests=10):
    """Test endpoint performance"""
    times = []
    
    async with httpx.AsyncClient() as client:
        for i in range(num_requests):
            start_time = time.time()
            response = await client.post(url, json=data)
            end_time = time.time()
            
            if response.status_code == 200:
                times.append(end_time - start_time)
            else:
                print(f"Request {i+1} failed: {response.status_code}")
    
    return times

async def main():
    print("🚀 Performance Testing: Sync vs Async Background Tasks\n")
    
    # Test sync endpoint (blocks until complete)
    print("Testing 10 sequential requests to /sync-task/")
    sync_times = await test_endpoint(
        "http://localhost:8000/sync-task/",
        {"task_name": "test", "duration": 3.0},
        10
    )
    
    sync_total = sum(sync_times)
    sync_avg = statistics.mean(sync_times)
    print(f"Total time: {sync_total:.2f} seconds")
    print(f"Average time per request: {sync_avg:.2f} seconds")
    print()
    
    # Test async endpoint (returns immediately)
    print("Testing 10 concurrent requests to /async-task/")
    start_time = time.time()
    
    async with httpx.AsyncClient() as client:
        tasks = [
            client.post(
                "http://localhost:8000/async-task/",
                json={"task_name": f"test{i}", "duration": 3.0}
            )
            for i in range(10)
        ]
        
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
    
    async_total = end_time - start_time
    async_avg = async_total / 10
    
    print(f"Total time: {async_total:.2f} seconds")
    print(f"Average time per request: {async_avg:.2f} seconds")
    print()
    
    # Calculate improvement
    improvement = sync_total / async_total
    print(f"Performance improvement: {improvement:.1f}x faster!")
    print()
    
    # Test user creation with background tasks
    print("Testing user creation with background email...")
    user_times = await test_endpoint(
        "http://localhost:8000/users/",
        {"email": "test@example.com", "username": "testuser"},
        5
    )
    
    user_avg = statistics.mean(user_times)
    print(f"Average user creation time: {user_avg:.2f} seconds")
    print("(Note: Email is sent in background after response)")

if __name__ == "__main__":
    asyncio.run(main())