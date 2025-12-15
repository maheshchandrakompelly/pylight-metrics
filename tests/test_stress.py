import unittest
import threading
from pylight_metrics.aggregator import LockFreeMetricsAggregator, MetricType

class TestConcurrency(unittest.TestCase):
    def setUp(self):
        """
        Clean setup for every test.
        We just reset the Singleton instance.
        """
        LockFreeMetricsAggregator._instance = None
        self.agg = LockFreeMetricsAggregator()

    def test_high_concurrency_counting(self):
        """
        The Ultimate Test:
        Launch 50 threads. Each thread adds 100 metrics.
        Total should be exactly 5000.
        """
        THREADS = 50
        UPDATES_PER_THREAD = 100
        EXPECTED_TOTAL = THREADS * UPDATES_PER_THREAD

        # Define the worker function
        def worker():
            for _ in range(UPDATES_PER_THREAD):
                self.agg.add_metric("stress.test", 1, metric_type=MetricType.COUNTER)

        threads = []
        
        # Launch Threads
        for _ in range(THREADS):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        # Wait for all threads to finish
        for t in threads:
            t.join()

        # CRITICAL: We must flush to calculate the final stats from shards
        stats = self.agg.flush()

        # Debug Print
        if "stress.test" in stats:
            actual_count = stats["stress.test"].count
            # print(f"✅ Stress Test Success! Expected: {EXPECTED_TOTAL}, Actual: {actual_count}")
        else:
            print("❌ Failed: Metric still missing.")
            actual_count = 0

        # Assertions
        self.assertIn("stress.test", stats, "Metric stress.test was not recorded!")
        self.assertEqual(actual_count, EXPECTED_TOTAL, 
                         f"Race condition detected! Expected {EXPECTED_TOTAL}, Got {actual_count}")

if __name__ == '__main__':
    unittest.main()
