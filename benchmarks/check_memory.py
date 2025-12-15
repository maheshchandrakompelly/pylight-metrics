import time
import tracemalloc
import threading
from pylight_metrics.aggregator import LockFreeMetricsAggregator, MetricType

# --- CONFIG ---
ITERATIONS = 5
OPS_PER_ITERATION = 100_000

def run_memory_test():
    print(f"🧠 MEMORY TEST: Running {ITERATIONS} cycles of {OPS_PER_ITERATION} ops")
    print("-" * 60)
    
    agg = LockFreeMetricsAggregator()
    # Reset singleton ensures clean state
    LockFreeMetricsAggregator._instance = None
    agg = LockFreeMetricsAggregator()

    tracemalloc.start()
    
    initial_snapshot = tracemalloc.take_snapshot()
    
    for i in range(ITERATIONS):
        print(f"Cycle {i+1}: Writing metrics...", end="", flush=True)
        
        # 1. Fill Memory (Simulate Traffic)
        for _ in range(OPS_PER_ITERATION):
            agg.add_metric("test_metric", 1.0, MetricType.COUNTER)
            agg.add_metric("test_timer", 0.5, MetricType.TIMER)
            
        current, peak = tracemalloc.get_traced_memory()
        print(f" Done. [Peak: {peak / 1024 / 1024:.2f} MB]")
        
        # 2. Flush (Should release memory)
        print("        Flushing...", end="", flush=True)
        agg.flush()
        
        # Force Python Garbage Collection just to be fair
        import gc
        gc.collect()
        
        current_after, _ = tracemalloc.get_traced_memory()
        print(f" Cleaned. [Current: {current_after / 1024 / 1024:.2f} MB]")

    print("-" * 60)
    final_snapshot = tracemalloc.take_snapshot()
    
    # Compare Start vs End
    stats = final_snapshot.compare_to(initial_snapshot, 'lineno')
    print("Top Memory Hogs (Should be small):")
    for stat in stats[:3]:
        print(stat)

    tracemalloc.stop()

if __name__ == "__main__":
    run_memory_test()
