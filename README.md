# Project repository template

A technology-neutral starting point for solo and AI-assisted development.

## Start a new project
1. Use GitHub's **Use this template** option after the owner enables Template repository in Settings > General.
2. Complete AGENTS.md and docs/project-context.md; assign a tier with the owner.
3. Select the relevant documentation skeletons under docs/templates and copy them into docs when needed.
4. Configure the actual stack, validation commands and CI. Do not install tooling or select a license by default.
5. Apply the ruleset using the instructions in .github/rulesets/README.md.

## Standards
AGENTS.md is the common instruction entry point; CLAUDE.md imports it. Detailed conventions and project tiers are under .agents. The tier definitions are proposed until confirmed. The template does not automatically modify repository settings or synchronize existing repositories.

## Maintenance
Update shared standards in this repository first, then propose changes in downstream repositories. Preserve project-specific content. Never publish private configuration or credentials.

## Agent skills

22 shared skills are installed for Codex and Claude Code. Edit canonical files under `.agents/skills/`, run `python scripts/sync-skills.py`, then `python scripts/validate-skills.py`. See `.agents/skills/README.md` and `docs/skill-evaluations.md`. Behavioral evaluations are defined but not yet executed.
