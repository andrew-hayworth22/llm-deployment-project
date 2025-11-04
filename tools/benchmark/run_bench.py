import asyncio, aiohttp, time, statistics as stats, json, random

# save as bench.py
import asyncio, aiohttp, time, statistics as stats, json, random

PROMPTS = [
  "Explain transformers to a 10-year-old in 3 sentences.",
  "Summarize this text: The quick brown fox jumps over the lazy dog.",
  "List 5 pros and cons of microservices.",
]

N_REQ = 200
CONCURRENCY = 16
TARGET = "vllm"  # "vllm" or "tgi"

async def hit_vllm(session, prompt):
    t0 = time.perf_counter()
    async with session.post("http://localhost:8000/v1/chat/completions", json={
        "model":"facebook/opt-1.3b",
        "messages":[{"role":"user","content":prompt}],
        "max_tokens":128, "stream":True
    }) as r:
        first = None
        async for line in r.content:
            if line.startswith(b"data: "):
                if first is None:
                    first = time.perf_counter()
        t1 = time.perf_counter()
        return (first - t0 if first else None, t1 - t0)

async def hit_tgi(session, prompt):
    t0 = time.perf_counter()
    async with session.post("http://localhost:8080/generate", json={
        "inputs": prompt, "parameters": {"max_new_tokens":128}, "stream": True
    }) as r:
        first = None
        async for chunk in r.content.iter_any():
            if first is None:
                first = time.perf_counter()
        t1 = time.perf_counter()
        return (first - t0 if first else None, t1 - t0)

async def main():
    lat_ttft, lat_total = [], []
    async with aiohttp.ClientSession() as session:
        sem = asyncio.Semaphore(CONCURRENCY)
        async def one():
            prompt = random.choice(PROMPTS)
            async with sem:
                if TARGET=="vllm":
                    ttft, total = await hit_vllm(session, prompt)
                else:
                    ttft, total = await hit_tgi(session, prompt)
                lat_ttft.append(ttft); lat_total.append(total)

        await asyncio.gather(*[one() for _ in range(N_REQ)])
    def s(x): return dict(p50=stats.median(x), p95=stats.quantiles(x, n=20)[18], p99=stats.quantiles(x, n=100)[98], avg=sum(x)/len(x))
    print(json.dumps({"TTFT": s([t for t in lat_ttft if t]), "TotalLatency": s(lat_total)}, indent=2))

if __name__=="__main__":
    asyncio.run(main())