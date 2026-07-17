# Unicity AOS

**A modular operating system for AI agents. Build from sealed parts, swap them later, and keep every capability under control.**

Unicity AOS is the operating system for agents you can compose and operate as your own. It brings together the Community Edition CLI, HTTP API, distributions, first-party capsules, provider and model experience, and Unicity Audit on the Unicity blockchain. Each capability has an explicit boundary, so the system can grow without becoming a single opaque agent application.

Unicity AOS is built on Astrid Runtime: a user-space microkernel that routes events, enforces capabilities, and owns the sandbox, with no agent logic of its own. Everything an agent can do is a capsule you compose, isolated from the kernel and from every other capsule.

## The model

- **Build from sealed parts.** Models, tools, memory, skills, and frontends are independently composable capsules with declared interfaces and authority.
- **Replace what changes.** Swap a provider, tool, memory system, or user interface without forking the operating system.
- **Keep authority explicit.** Capabilities are scoped to the work at hand; helpers receive only the access they need.
- **Keep sensitive work accountable.** Unicity Audit anchors the actions that matter on the Unicity blockchain; it is separate from Astrid Runtime's local enforcement records.

## Where to go next

- Read the [AOS Community Edition README](../aos/README.md) for the source, distributions, capsules, CLI, and HTTP API.
- See [AOS Community Edition on GitHub](https://github.com/unicity-aos/aos-ce).
