import asyncio
from collections import deque
import time

from tqdm import tqdm

class AsyncRateLimiter:
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.monotonic()

            # Remove expired timestamps
            while self.calls and self.calls[0] <= now - self.period:
                self.calls.popleft()

            if len(self.calls) >= self.max_calls:
                sleep_time = self.calls[0] + self.period - now
                await asyncio.sleep(sleep_time)

                # Clean again after sleep
                now = time.monotonic()
                while self.calls and self.calls[0] <= now - self.period:
                    self.calls.popleft()

            self.calls.append(time.monotonic())

class RateLimitedLauncher:
    def __init__(self, max_calls_per_sec: int = 2):
        self.rate_limiter = AsyncRateLimiter(
            max_calls=max_calls_per_sec,
            period=1.0
        )

    async def _run_one(self, worker_func, item, progress, useContext, enhance, directContext):
        await self.rate_limiter.acquire()   # ⬅ rate limit enforced here
        result = await worker_func(item, useContext, enhance, directContext)
        progress.update(1)
        return result

    async def run(self, items, worker_func, useContext=False, enhance=False, directContext=True):
        progress = tqdm(total=len(items))

        tasks = [
            asyncio.create_task(
                self._run_one(worker_func, item, progress, useContext, enhance, directContext)
            )
            for item in items
        ]

        results = await asyncio.gather(*tasks)
        progress.close()
        return results
