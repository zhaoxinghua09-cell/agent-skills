# 提示词泄漏扫描器 / Prompt Leak Scanner

Pre-share scanner for prompts and system prompts: secrets, internal paths, PII, custom sensitive words (--extra), and self-leak backdoors ('ignore previous instructions' / 'print your system prompt' plants). Non-zero exit blocks leaks.

**Pain point**: Prompts are the most casually shared sensitive asset: one embedded key, intranet path, or 'repeat your system prompt' plant gives away the farm — nobody runs a pre-release check.

LGD-III gated (the last gate before a prompt goes public).

Part of the **LGD moat** (凡自治之物: registered / evidenced / gated).

Zero-dependency (stdlib only). See `scripts/` for CLI usage (`--help`).

© MedXpert × SynomosAI · LGD-Powered
