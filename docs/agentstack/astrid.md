# AstridOS

**Run AI agents and the tools they use without having to trust them.**

AI agents fail in ways a better prompt cannot fix. A jailbreak, a poisoned tool, or a plain bug, and the agent reaches for access you never meant to give it. Astrid contains that by construction: every agent, and every tool it calls, runs as a sandboxed WebAssembly capsule with only the permissions you granted and the resource budget you set. A compromised agent still cannot read a file, reach a network, or spawn a process outside its grant, and it cannot burn unbounded CPU or memory. Every action it takes flows through a tamper-evident audit chain, so you can prove exactly what ran and why.

Astrid is a user-space microkernel written in Rust. The kernel is a dumb event router: it routes messages, enforces permissions, and owns the sandbox, with no agent logic of its own. Everything an agent can do is a capsule you compose, isolated from the kernel and from every other capsule.

## The model

- **The kernel is dumb.** It routes IPC events, enforces capabilities, and owns the WebAssembly sandbox. It holds no business logic. All intelligence lives in capsules.
- **Capsules are WASM processes.** Each targets `wasm32-unknown-unknown`, declares its interface and the host resources it needs in a manifest, and reaches the rest of the system only over a typed IPC bus. No ambient authority, no raw syscalls.
- **Permissions only ever narrow.** A sub-agent can be granted a smaller slice of access than its parent, never a larger one. Grants are signed capability tokens scoped per principal, so they cannot be forged or escalated.
- **Everything is audited.** Host calls and IPC flow through a BLAKE3-linked audit chain, so the record of what an agent did is tamper-evident, not advisory.
- **Defense in depth, fail secure.** Input classification, capability checks, sandboxing, approval gates, and audit logging stack in front of every action. When a layer is unsure, it denies.
