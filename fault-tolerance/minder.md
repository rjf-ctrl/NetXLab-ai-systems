# MINDER
- Modern LLMs like GPT-4 contain hundreds of billions to trillions of parameters. Such models require distributed training across many GPUs and machines.
- *Distributed training* depends heavily on synchronization between machines.If one machine slows down, all other machines may have to wait.
- Faults happen frequently in large GPU clusters due to system complexity.Common fault sources include GPU failures, ECC memory errors, network issues, storage delays, and software bugs.
- Manual debugging is slow because many teams must inspect logs and hardware separately.Training interruptions can cause major financial and time losses. Traditional fault detection methods using fixed thresholds are unreliable.
- Monitoring metrics vary based on workload, model type, and cluster scale. No single metric consistently identifies all fault types.
  
Minder assumes healthy machines should show similar runtime behavior. Faulty machines show unusual behavior compared to peer machines.
**Minder Principles**:
- Similarity: machine vs peer machines, not machine vs fixed threshold
- Continuity: real faults persist over time, transient spikes/noise ignored
- Per-metric modeling: separate model for each metric, GPU / CPU / network / storage independently analyzed
- Metric prioritization: most fault-sensitive metrics checked first, faster detection
  
**Minder Working**
- collect runtime telemetry from all nodes
- denoise monitoring data
- compare machine behavior across cluster
- compute dissimilarity scores
- track duration of abnormality
- persistent divergence ⇒ faulty machine
- runtime detection without stopping training
  
**eg:** *PCIe Downgrading Case*
PCIe bandwidth dropped from 6.4Gbps → 4Gbps   
NIC buffers filled → communication bottleneck created  
caused PFC/ECN/CNP congestion surge in network   
cluster-wide NIC throughput dropped from 6.5Gbps → 4.9Gbps   
reduced GPU tensor core utilization  
entire 128-machine training slowed for 40 minutes  
shows how small local hardware faults cascade into distributed performance collapse

- Hardware faults are most common; ECC errors dominate
- CUDA, GPU, NVLink, PCIe, NIC faults also frequent
- Different faults affect different metrics differently
- No single metric can reliably detect all fault types
- CPU/GPU drops often indicate faulty node
- Network faults cause PFC/throughput anomalies
- Disk metrics less useful for fault detection
  
**Challenges**
- faults can happen in any hardware/software component
- normal metric behavior depends on workload/task
- same fault can appear through different metrics
- same metric anomaly can indicate different faults
- monitoring data contains noise and jitters
- Key Insight
- multi-metric detection required
- per-metric models better than one combined model

**Machine-level Similarity**
Healthy cluster → similar behavior across machines  
balanced DP/PP/TP workloads → similar GPU/CPU/network patterns  
faulty node breaks symmetry → becomes outlier/diverges from peers  

**Why Not Supervised Learning**

same metric value may be normal in one task, abnormal in another  
problem is machine localization, not just anomaly classification  
hence → unsupervised peer comparison  

**Machine-level Continuity**

jitters/noise → short-lived spikes  
real faults → persist over time  
continuity check filters false positives

**Individual Denoising Models**

different faults affect different metrics differently  
one combined model could get confused  
separate VAE-based model per metric → cleaner telemetry + better detection  

**Prioritized Metric Sequence**

some metrics more fault-sensitive  
check high-sensitivity metrics first  
faster faulty machine localization  


