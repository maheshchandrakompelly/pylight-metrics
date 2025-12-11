# Pylight Metrics

**Zero-Contention, High-Performance Observability for Python.**

`pylight-metrics` is a thread-safe metrics aggregator designed for high-throughput applications. Unlike standard libraries that introduce lock contention, this library uses **Thread Local Storage (TLS)** to buffer metrics.

## Installation

```bash
pip install pylight-metrics
