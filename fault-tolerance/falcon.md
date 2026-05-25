# FALCON
- Core distinction: **fail-stop vs fail-slow**
- fail-stop → crash/halt immediately
- fail-slow → machine still works but becomes slower
- Existing systems mostly handle fail-stop failures
- fail-slows harder because training continues but throughput drops

- Causes of fail-slows:
  - CPU contention
  - GPU thermal throttling
  - network congestion
  - degraded communication links

- Distributed training synchronizes every iteration
- one slow worker/link → entire cluster waits

- Production study:
  - 10,000+ GPUs
  - 4000+ nodes
  - fail-slows extremely common

- Computation fail-slows:
  - less frequent
  - ~10 min average duration

- Communication fail-slows:
  - more frequent
  - ~24 min average duration

- 16/27 large jobs experienced fail-slows
- average training slowdown: **1.34×**

---

# Why Detection is Hard

- hybrid parallelism (DP/TP/PP) complicates slowdown propagation
- slowdown source difficult to localize
- current practice:
  - manual debugging
  - checkpoint/restart

---

# FALCON-DETECT

- runtime straggler detection system
- detects slow GPUs and communication links

Detection flow:
1. monitor iteration time per worker
2. BOCD detects sustained slowdown/change-point
3. lightweight profiling narrows suspicious groups
4. brief benchmarks pinpoint exact slow GPU/link

- framework-agnostic
- non-intrusive
- avoids full-cluster validation

---

# FALCON-MITIGATE

- avoids immediate checkpoint/restart
- fail-slows often temporary → restart is overkill

Mitigation strategies:
- S1 → do nothing
- S2 → redistribute microbatches
- S3 → adjust parallel topology/routing
- S4 → checkpoint & restart

---

# Key Insight

- mitigation cost increases from S1 → S4
- fail-slow duration unknown beforehand
- modeled like ski-rental problem

Strategy:
- start with cheap mitigation
- escalate only if slowdown persists


# FALCON 

- LLM training requires thousands of GPUs on HPC clusters
- distributed training → frequent synchronization
- one slow/faulty component slows entire job

# Parallelism

## TP
- split computation across GPUs
- high synchronization cost
- mostly intra-node

## DP
- multiple model replicas
- synchronize gradients each iteration

## PP
- split layers across GPUs
- pipelined execution
- lower communication overhead

## Hybrid Parallelism
- combines TP + DP + PP
- enables trillion-parameter training

---

# Key Insight

- hybrid parallelism makes straggler localization difficult
- slowdown can propagate through:
  - compute
  - communication
  - synchronization

---

# Core Motivation

- fail-slows are:
  - common
  - hard to detect
  - hard to mitigate
- motivates FALCON