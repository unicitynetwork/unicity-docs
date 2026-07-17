# Unicity Protocol

Unicity is a settlement network for machine-speed commerce. Assets are self-contained bearer objects that carry their own proof of validity and move directly between parties, rather than rows in a global database that validators take turns updating.

## How it works

A Unicity proof is a non-inclusion proof: it demonstrates that a commitment has not been spent. Transaction commitments are batched by the aggregator into a sparse Merkle tree, and a token's validity is proven against that tree. Because ownership is proven rather than looked up in a shared ledger, assets can change hands directly between parties without a global state update on every transfer.

For the formal treatment, see the [research papers](research-papers.md). For the developer-facing token API, see the [State Transition SDK (JS)](../stsdk/README.md).

## Where to go next

- Read the [Whitepaper](research-papers.md) for the high-level design.
- Read the [Yellowpaper](research-papers.md) for the formal protocol specification.
- Build with the [State Transition SDK (JS)](../stsdk/README.md) to move tokens.
