# LGD 徽章验真器 / LGD Badge Verifier

Verify a badge certificate: recompute fingerprint (anti-tamper) + evidence hash format + registry cross-check (serial exists & not revoked).

**Pain point**: Issuance without verification is forgeable: the loop lacked reverse checking and the trust chain broke.

Part of the **LGD moat loop**: Passport (registered) → Evidence chain (evidenced) → Gate (gated) → **Badge (issued/verified)**.

Zero-dependency (stdlib only). See `scripts/` for CLI usage (`--help`).

© MedXpert × SynomosAI · LGD-Powered
