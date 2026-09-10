# Release readiness — 0.2.0 research preview

**Assessment:** READY WITH CONDITIONS — local 0.2.0 prep is committed and tagged; **GitHub push blocked** (`gh` token for `lessthanzero` invalid). Re-auth, then create remotes / push / release.

## Done in this execution

- Version bumped to **0.2.0** across ancient-text-lab, linear-a, phaistos-disk
- NOTICE files + license fields; third-party media/census untracked
- PII/homelab scrub (paths, LAN/Tailscale IPs, Forgejo sync stubs); remote tokens stripped; local forgejo-token file wiped on `pc`
- Claim hygiene: homology CONFIRMED removed; hymn/God demoted; README rewrite (phaistos)
- SCIENTIFIC_LIMITATIONS, CHANGELOG, INDEPENDENT_REVIEW (phaistos); outreach drafts in `docs/OUTREACH_DRAFTS.md`
- CI workflows added for linear-a and phaistos-disk
- Tests: ATL 60, LA 141, PD 131 — all passing locally (macOS)
- Local tags `v0.2.0` created (not pushed)

## Blocked on you

- [ ] `gh auth refresh -h github.com` (token invalid)
- [ ] Create public GitHub remotes under your account/org
- [ ] `git push -u origin main` (or `master`) + `git push origin v0.2.0` on each repo
- [ ] Prefill outreach emails with live URLs (do not auto-send)
- [ ] Reddit / LinkedIn only after URLs work
- [ ] Optional: capture workbench GIF from cleared assets; Fedora pytest cross-check

## Explicitly not done

- No 1.0.0 tag
- No public GitHub push
- No ATL ← sibling package integration
- No auto-sent email / social posts
