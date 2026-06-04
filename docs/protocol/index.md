# Unicity Protocol

Unicity is a settlement layer for machine-speed commerce. Assets are self-contained bearer objects that carry their own proof of validity and move directly between parties, rather than rows in a global database that validators take turns updating.

## Architecture

The protocol is organized in three layers:

- __L1 — Proof of Work.__ The base chain.
- __L2 — BFT finality and aggregation.__ Byzantine fault-tolerant finality on top of L1, plus the aggregator that batches transaction commitments into a sparse Merkle tree.
- __L3 — Token layer.__ Off-chain tokens whose validity is proven against the aggregator. A Unicity proof is a non-inclusion proof: it demonstrates a commitment has not been spent.

For the formal treatment of each layer, see the [research papers](research-papers.md). For the developer-facing token API, see the [State Transition SDK (JS)](../stsdk/README.md).

## Where to go next

- Read the [Whitepaper](research-papers.md) for the high-level design.
- Read the [Yellowpaper](research-papers.md) for the formal protocol specification.
- Build with the [State Transition SDK (JS)](../stsdk/README.md) to move tokens.
