# AGENTS.md — airpyrt-tools/

## Purpose

Python 3 port of `airpyrt-tools` (the `acp` module) implementing the legacy Apple ACP protocol for AirPort/Time Capsule devices. Originated as upstream `x56/airpyrt-tools` (Python 2.7); this tree has been ported to Python 3.8+ with an added pytest suite.

## Ownership

- Origin: https://github.com/x56/airpyrt-tools (separate git repo at this path; local commits diverge from upstream).
- This is a **local fork**. `TimeCapsuleSMB` still consumes the upstream Py2 tree via `make airpyrt` (clones into `TimeCapsuleSMB/.deps/airpyrt-tools`); it does **not** yet consume this Py3 port.
- `BuildAirpyrtTools.sh` at the workspace root builds an sdist/wheel from this tree.

## Local Contracts

- Python 3.8+ with `pycryptodome` (drop-in for legacy `pycrypto`). `setup.py` version 2.0, packages `["acp", "acp.clibs"]`, entry point `acp=acp.cli:main`.
- Editable install from this dir: `.venv/bin/pip install -e .`. Run: `.venv/bin/python -m acp`.
- Dedicated venv lives at `.venv/` (gitignored).
- All source/test files use **TAB indentation**; preserve it in edits.
- The port preserves original behavior; only Py2→Py3 incompatibilities were fixed, plus one pre-existing bug: `ACPClientSession.enable_encryption` referenced a bare `encryption_context` (NameError) and now uses `self.encryption_context`.
- **Security**: the old ACP protocol transmits the admin password in a trivially recoverable format. Treat the tool as unsafe, especially for remote administration. Keep AirPort remote admin disabled.

## Work Guidance

- `acp/property.py` lines ~9–551 are the `_acp_properties` data table (~90 entries as 4-tuples). Use targeted edits there, never whole-file rewrites.
- `zlib.adler32`/`crc32` return UNSIGNED in Py3 (signed in Py2). `acp/message.py` stores checksums in signed `!i` struct fields via a `_to_i32()` helper; `acp/basebinary.py` uses unsigned `>I` with `& 0xFFFFFFFF`. Match each module's convention.
- `ACPEncryption` uses AES-CTR; the counter advances per call, so encrypt-then-decrypt must use **two fresh instances** with the same key/iv, not one instance.
- The SRP path (`acp/client.py::authenticate_AppleSRP`, `acp/clibs/AppleSRP.py`) loads the macOS `AppleSRP.framework` lazily and is unfinished/untested.
- Known pre-existing LSP noise (runtime-safe, not regressions): `acp/session.py` initializes `self.sock = None`; `acp/cli.py:80` calls `.ljust` on a value that can be `None` only for invalid property names.

## Verification

- `cd airpyrt-tools && .venv/bin/python -m pytest` — 73 tests, all must pass.
- Suite lives under `tests/`: `test_keystream`, `test_misc`, `test_cflbinary`, `test_message`, `test_property`, `test_encryption`, `test_basebinary`, `test_cli`.

## Child DOX Index

(none)

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **airpyrt-tools** (255 symbols, 532 relationships, 22 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> Index stale? Run `node .gitnexus/run.cjs analyze` from the project root — it auto-selects an available runner. No `.gitnexus/run.cjs` yet? `npx gitnexus analyze` (npm 11 crash → `npm i -g gitnexus`; #1939).

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows. For regression review, compare against the default branch: `detect_changes({scope: "compare", base_ref: "main"})`.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `rename` which understands the call graph.
- NEVER commit changes without running `detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/airpyrt-tools/context` | Codebase overview, check index freshness |
| `gitnexus://repo/airpyrt-tools/clusters` | All functional areas |
| `gitnexus://repo/airpyrt-tools/processes` | All execution flows |
| `gitnexus://repo/airpyrt-tools/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
