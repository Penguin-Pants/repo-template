# Synchronization ownership (initial contract)

Only exact paths listed in `.agents/ownership.json` are candidates for recurring synchronization. Unlisted paths are project-owned. Root AGENTS.md, CLAUDE.md, project context and gitignore are project-owned. Existing files require a verified baseline before any replacement. Local divergence blocks an update. Removed paths are reported, never deleted. The workflow listed in the manifest is a candidate only; workflow security validation and sandbox approval are required before deployment. This initial contract does not enroll repositories or authorize production synchronization.

The root entry point loads `.agents/shared/instructions.md`. The manifest itself and shared evaluation definitions are managed. The shared skill validator and generator operate only on registered pairs and leave all custom skills alone. Executable shared files require controller security approval before propagation.

## Automatic dispatch

`.github/workflows/dispatch-sync.yml` runs only in this repository on pushes to main that touch managed path prefixes. It dispatches the private controller with `SYNC_DISPATCH_TOKEN` (Actions write on repo-bootstrap only). It is not a managed file, so it never propagates. Repositories generated from this template skip it through a repository guard. The controller always reconciles against the latest trusted main revision. It never writes to this repository, so synchronization cannot trigger itself. There is no periodic synchronization.
