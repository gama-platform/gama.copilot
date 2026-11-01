# Changelog

## 2026-11-01 - Standalone integration

- Extract optional Copilot packaging from GAMA into `gama-platform/gama.copilot`,
  retaining the `gama.feature.copilot` feature ID.
- Add an independent Tycho build and dependency-complete p2 site with retained releases
  behind `https://gama-platform.org/gama.copilot/`.
- Pin unmodified Copilot for Eclipse 0.21.0 (`0.21.0.202608060743`) and its release ZIP
  digest against the Eclipse 2026-03 / Java 21 baseline.
- Support Linux GTK x86_64, Windows x86_64, and both macOS architectures.
- Move preference seeding and status-bar activity bindings into `gama.ui.copilot`.
  Preference seeding uses GAMA's new pre-workbench Runnable startup extension,
  preserving existing user preferences without starting upstream UI early.
- Add path-filtered builds, pull-request validation and manually dispatchable GitHub Pages
  publication, explicit third-party notices, and repository-specific issue routing.
- Keep generic GAML editor hooks and core installation commands in GAMA, without making
  this optional integration part of ordinary GAMA builds.
