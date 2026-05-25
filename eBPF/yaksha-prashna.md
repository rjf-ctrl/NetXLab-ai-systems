# YAKSHA PRAHSNA
## The Challenge
Modern cloud/network systems increasingly use:** eBPF-based Network Functions (NFs)**  
These are programs that process packets inside the Linux kernel.  
Examples:  
* firewalls,
* load balancers,
* observability agents,
* DDoS filters,
* NATs,
* traffic monitors.

The problem is:  
> operators often only receive compiled eBPF bytecode, not source code.

So they cannot easily understand:
* what the NF actually does,
* whether it is correct,
* whether it matches its claimed behavior,
* or whether it safely interacts with other NFs.

---

### Who Faces This Problem?
Mainly:  
* cloud operators,
* infrastructure engineers,
* network admins,
* platform teams,
* security teams.

Example:  
A cloud provider deploys:  
* a third-party firewall NF from Palo Alto Networks,
* a load balancer from another vendor,
* observability eBPF from another team.

Now they must ask: Will these work safely together?
But they only have:opaque eBPF bytecode

That is the core challenge.  

Before systems like Yaksha-Prashna, people mainly relied on:

---

## A. Manual Inspection

Developers read:
* source code,
* disassembled bytecode,
* logs,
* traces.

Problem:
* difficult,
* slow,
* error-prone,
* impossible at scale.

---

## B. Runtime Debugging

Using tools like:
* tcpdump,
* tracing,
* packet captures,
* observability systems.

Problem:
* only shows behavior AFTER deployment,
* doesn’t prove correctness,
* doesn’t reveal hidden dependencies.

---

## C. Traditional Network Verification

Tools checked:
* firewall rules,
* routing policies,
* SDN rules.

Problem:
they assume networking behavior is already expressed clearly as:ALLOW TCP 443
But eBPF programs hide behavior inside executable logic.

---

## D. Generic Program Analysis

Using:
* symbolic execution,
* static analyzers,
* compiler-analysis tools.

Problem:
they don’t understand:
* packet semantics,
* eBPF helpers,
* maps,
* protocol parsing,
* kernel hooks.

---

## 3. What available solutions exist, and why are they insufficient?

# Network Policy Verifiers

These verify:
* routing correctness,
* ACL consistency,
* reachability.

Example: Can traffic from A reach B?
They fail because they assume:*networking behavior is explicitly written as policies.* But eBPF behavior is hidden in code.

---

Traditional verifier understands:BLOCK PORT 22
But not:
```
if ip in map:
    if tcp->dest == 22:
        drop
```
The policy is implicit inside program logic.

---



# Traditional Static Analyzers

These understand:
* variables,
* memory,
* functions,
* control flow.

They do NOT naturally understand:
* packet headers,
* protocols,
* helper semantics,
* maps,
* tail calls,
* NF chaining.

Example:

Generic analyzer sees:
```
memory write at offset 30
```

Yaksha-Prashna needs to understand:

```
TCP destination port rewrite
```

Huge semantic difference.

---

# Runtime Tracing/Observability

These show:
* live traffic,
* logs,
* packet traces.

They can show:

```
something went wrong
```
But not:
```
NF2 depends on NF1 rewriting packet metadata
```
No semantic dependency reasoning.

---


# Formal Verification
These can theoretically analyze arbitrary programs.

Too expensive/scaling problems.

eBPF networking creates:
* many packet paths,
* many protocol combinations,
* dynamic state,
* map-dependent logic.

This causes:

# path explosion

Analysis becomes too slow.

That’s why the paper emphasizes:

``` 
200–1000× speedup
```

---

## 4. Why don’t other tools work for THIS use case?

Because eBPF is fundamentally different.

---

# Traditional Networking = Policies

Old tools expect:

```
ALLOW
DENY
FORWARD
```

Simple declarative rules.

---

# eBPF = Executable Packet Programs

eBPF programs:
* parse packets,
* modify headers,
* query maps,
* redirect traffic,
* maintain state,
* call helpers,
* chain into other programs.

Behavior emerges dynamically.

So tools must understand:

* networking semantics,
* bytecode semantics,
* protocol semantics,
* inter-NF dependencies.

That combination is rare and difficult.

---

The paper argues we need:

# A semantic understanding system for eBPF bytecode

Specifically something that can:

* infer NF behavior,
* understand packet operations,
* identify protocols,
* analyze map usage,
* track dependencies,
* verify correctness,
* and support user queries.

And it must be:

# scalable.

---

The paper creates:

## Yaksha-Prashna

A system for:

* semantic analysis of eBPF bytecode,
* behavioral verification,
* NF interaction analysis,
* and query-driven inspection.

Think of it as:

**“Google for understanding eBPF NF behavior”**

---
The system:

## Step 1 — Analyze Raw eBPF Bytecode

It examines:
* instructions,
* control flow,
* packet accesses,
* helpers,
* maps.

---

## Step 2 — Recover Networking Semantics

Instead of:

```
memory offset 26
```

It infers:

```
reads TCP destination port
```

Instead of:

```"
memory write
```

It infers:

```
rewrites IP header
```

This is the major contribution.

---

## Step 3 — Build Network Context

The system understands:

* protocols processed,
* packet fields touched,
* read/write/copy behavior,
* map interactions,
* NF dependencies.

---

## Step 4 — Support Semantic Queries

Users can ask:

```
Does this NF modify TCP headers?
```

or:

```
Which NF writes metadata later consumed by NF2?
```

---

## Step 5 — Verify Properties

Using:

* assertions,
* preconditions,
* postconditions,
* contracts.

Example:

```
This NF must never rewrite source IP
```

---

NOVELTY:  

# A. eBPF-Centric Analysis
The system is designed specifically for:

* packet semantics,
* maps,
* helpers,
* NF chaining,
* kernel networking behavior.

Not generic software.

---

# B. Semantic Understanding

It lifts:

```
low-level bytecode
```

into:

```
high-level networking meaning
```


---

# C. NF Dependency Analysis

It understands:

```
NF1 writes packet field
NF2 later reads it
```

Traditional tools usually miss this.

---

# D. Queryable Interface

Operators can ask:

* semantic questions,
* correctness questions,
* dependency questions.

Not just read disassembly.

---

# E. Scalability

The paper claims:

# 200–1000× speedup

Meaning:
they likely use:

* abstractions,
* optimized representations,
* smarter semantic modeling,
  instead of brute-force verification.

---


> **Yaksha-Prashna is an eBPF-specific semantic analysis and query system that infers high-level network-function behavior from low-level bytecode, verifies correctness properties, and analyzes interactions between chained eBPF network functions efficiently and scalably.**

---


At a high level, it:

* analyzes low-level eBPF bytecode,
* extracts high-level networking meaning (“network context”),
* and lets operators query/assert properties about NF behavior.

You can think of it as:

> a semantic analysis + querying system for eBPF network functions.

---

# Main Goals


---
**1. Understand opaque eBPF bytecode**
**2. Verify NF correctness/conformance**
**3. Understand interaction between multiple NFs**
**4. Make analysis scalable**

# Core Idea of Yaksha-Prashna

The main insight is:

> Instead of repeatedly analyzing raw bytecode for every query, first extract reusable “network context” from the bytecode, then run semantic queries on top of that context.

This is the biggest systems idea.

---

# Components of Yaksha-Prashna

The system has TWO major components.


# 1. Yaksha-Prashna Analyzer

This is the:

# analysis engine

Its job:

* analyze raw eBPF bytecode,
* track dataflow/control flow,
* recover networking semantics,
* extract network context.

---

## What does it use?

### A. Control Flow Analysis

Understands:

```
possible execution paths
branches
jumps
program structure
```

Usually via:

# Control Flow Graphs (CFGs)

---

### B. Dataflow Analysis

Tracks:

```
where data comes from
where it moves
how it changes
```

Example:

```
packet field → register → map → helper
```

This is how YP infers:

* protocol accesses,
* packet modifications,
* dependencies.

---

## Challenges Faced by Analyzer

---

### Challenge 1 — Low-Level Bytecode

eBPF bytecode is assembly-like.

One high-level operation may become many low level instructions
So semantics are hidden.

---

### Challenge 2 — Register Reuse

eBPF has:

* few registers,
* small stack memory.

Programs frequently reuse registers.

Example:

```
R1 stores IP field
later R1 stores packet length
```

This obscures meaning.

---

### Challenge 3 — Cross-Instruction Semantics

Meaning is spread across multiple instructions.

The analyzer must connect:

```
instruction A
→ instruction B
→ instruction C
```

to infer:

```
reads TCP destination port
```

---

## Why It Works Efficiently

The paper says eBPF has nice properties:
```
* limited state space,
* no loops,
* fixed registers,
* verifier restrictions.
```
These reduce analysis complexity.

---

# 2. Yaksha-Prashna Language

This is the:

# user-facing query DSL

It lets operators ask:

* semantic questions,
* assertions,
* retrieval queries.

WITHOUT understanding:

```
registers
byte offsets
basic blocks
instruction IDs
```

---

# Types of Queries Supported

---

## A. Assertion Queries

Check if property holds.

Example:

```
Does NF write to a map?
Does NF modify TCP header?
```

---

## B. Retrieval Queries

Retrieve semantic information.

Example:

```
Which packet field is written?
Which protocol is processed?
Which map stores source IP?
```

This is something traditional assertions cannot do well.

---

# DSL Design Principles

The DSL is designed to be:


## Simple

Operators don’t need bytecode expertise.



## Expressive

Can express:

* complex NF interactions,
* conformance checks,
* dependencies.


## Composable

Simple queries can combine into:

```
complex real-world policies
```


## Adoptable

Uses:
Prolog for logic-based querying.

---

# Decoupling Analysis from Querying

Traditional systems:

```
new query → reanalyze program
```

Very expensive.

Yaksha-Prashna:

```
analyze once
store extracted network context
reuse for all future queries
```

This is WHY they achieve: 200–1000× speedup

---

# Exact Properties / Characteristics of Yaksha-Prashna


1. Bytecode-Level Analysis
2. Semantic Network Context Extraction
3. eBPF-Centric Analysis

Specifically models:

* helpers,
* maps,
* packet semantics,
* verifier constraints.

---

## 4. Queryable Semantic Interface

Supports:

* assertions,
* retrieval,
* cross-bytecode interaction analysis.

---

## 5. Scalable Architecture

Separates:

```
analysis phase
```

from:

```
query phase
```

for efficiency.

---

## 6. Cross-NF Interaction Reasoning

Can analyze:

```
write-before-read dependencies
packet transformations
shared map interactions
```

between multiple NFs.

---

Yaksha-Prashna is essentially:

**a semantic reasoning engine for eBPF networking bytecode**

It converts:

```
low-level bytecode
```

into:

```
high-level networking meaning
```

and allows operators to:

* inspect,
* verify,
* query,
* and reason about NF behavior efficiently.

---
---
## USE CASES
**Third-party eBPF NFs**
Many organizations deploy third-party eBPF network functions, often only available as bytecode, making it difficult to understand their actual behavior and interactions with other NFs. Existing eBPF verifiers only ensure safety properties like memory safety and termination, but cannot verify functional correctness or detect malicious/unexpected packet-processing behavior.

Users:
1. Network operators: to verify the functional correctness and safe interaction of third-party eBPF NFs before deploying them into existing NF chains.
2. Network developers: to prove that their compiled eBPF bytecode conforms to specifications without revealing the source code.

Use-cases:
1. Individual NF conformance to specification

````
This example shows a firewall NF whose behavior does not conform to its specification: it processes ICMP traffic and modifies the TCP source port, even though it should only allow TCP/UDP traffic and never modify packets.

The assertion `A1: !updatesField(xdp_fw, *)` checks whether the bytecode updates any packet field. Here, `updatesField` retrieves all packet fields modified by the NF, `xdp_fw` specifies the firewall bytecode being analyzed, and `*` means “any field” . Since the firewall modifies the TCP source port, the assertion fails.


A2:

passes(xdp_fw, xdp, [(var, var)]),
!accessesProtocol(xdp_fw, "ipv4.proto", "icmp")


first uses `passes(...)` to retrieve all execution paths where packets are successfully forwarded at the XDP hook point. The `(var, var)` argument acts like a wildcard, meaning all passing paths are considered. Then `!accessesProtocol(...)` asserts that none of those paths should process the ICMP protocol. Since the firewall explicitly parses ICMP packets, this assertion also fails.
````

2. Unintended NF interactions
````
The following assertion checks for Read After Write (RAW) dependency between NF2 and any successor NFs (NF3) in the chain, as shown in Listing 2. This assertion can be executed on the new chain before deploying NF2’s bytecode.

A3: !updatesField(NF2, *), successorNF(NF2, SNf), readsField(SNf, *).

𝑢𝑝𝑑𝑎𝑡𝑒𝑠𝐹𝑖𝑒𝑙𝑑 with ∗ argument retrieves a list of fields updated by NF2’s bytecode (write list), including socket buffer and packet headers. s𝑢𝑐𝑐𝑒𝑠𝑠𝑜𝑟𝑁𝐹 gets all the successor NFs of NF2
𝑟𝑒𝑎𝑑𝑠𝐹𝑖𝑒𝑙𝑑 construct retrieves the list of fields read by them (read list). The assertion fails if the write list overlaps with the read list of any of NF2’s successors in SNf.
Yaksha-Prashna language also supports assertions to check for other dependencies (WAR, WAW).
````

3. Understanding the NF/NF chain behavior
````
For example, one can accurately document and report that the specification violation in Listing 1 was due  to the modification of the TCP source port, and sk_buff-
>mark field is responsible for the dependency in Listing 2.
In the first case, the retrieval query
RQ1: updatesField(xdp_fw, Fld).
retrieves a list of packet fields (e.g., tcp.sport) updated by the firewall, stores them in 𝐹𝑙𝑑, and returns as the query result.

In the second case, the following retrieval query can be used to debug the assertion A2’s failure.
RQ2: updatesField(NF2, Fld), successorNF(NF2,
SNf), readsField(SNf, Fld).

It retrieves the list of socket buffer and packet header fields updated by NF2 and read by any of NF2’s successors, stores them in 𝐹𝑙𝑑, and returns them as the query result (i.e., sk_buff->mark in Listing 2). 

To summarize, retrieval queries provide deeper insight into packet processing behavior, such as protocols being accessed, header/buffer fields being read/updated,
shared map between NFs, helper functions invoked, etc.
````   
