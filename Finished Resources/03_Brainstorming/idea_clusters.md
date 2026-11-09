# Root Cause Diagnosis & Solution Idea Clusters

## 1. Five Whys Decomposition
1. **Why is throughput lagging?** Micro-stoppages at staging accumulation point.
2. **Why do stoppages occur?** Variance between primary press cycle and secondary transfer.
3. **Why does variance cause idle time?** Lack of buffer decoupling between stages.
4. **Why is buffering rigid?** Monolithic fixed-conveyor architecture without dynamic re-routing.
5. **Root Cause**: Rigid synchronous coupling between disparate machine cycles without telemetry-driven pacing.
