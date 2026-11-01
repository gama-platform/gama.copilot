# GitHub Copilot for GAMA

Independent packaging and small GAMA UI adaptations for the **unmodified**
[GitHub Copilot for Eclipse](https://github.com/microsoft/copilot-for-eclipse).
This is not a fork of Copilot and is not affiliated with or endorsed by GitHub or Microsoft.
GAMA itself builds and runs without this optional integration.

**Update site:** `https://gama-platform.org/gama.copilot/`

## Installation and compatibility

Use the Copilot installation command in GAMA, restart, and sign in with GitHub.
Alternatively, in **Help > Install New Software...**, add the update site above and select
**GitHub Copilot for GAMA** (`gama.feature.copilot.feature.group`). Keep the
[Eclipse 2026-03 repository](https://download.eclipse.org/releases/2026-03/) available
for platform dependencies. Do not add the upstream moving Copilot update site.
A Copilot entitlement and network access to GitHub's services are required.

The baseline is **Eclipse 2026-03 (4.39), Java 21+**. Supported GAMA platforms:
Linux GTK x86_64, Windows x86_64, macOS Cocoa x86_64 and aarch64 (Apple Silicon).
The upstream feature also declares Linux aarch64; that is not a supported GAMA target here.
The installed feature retains the upstream native-agent platform filters.

For preference seeding, GAMA must expose the `gama.ui.application.startup` extension
point introduced with this repository extraction in November 2026. Its `<startup class="..."/>`
contributions implement `java.lang.Runnable` and run synchronously on the UI thread
before workspace selection and workbench startup. The integration has **no GAMA Java API
dependency**. Older GAMA builds that already seed these preferences retain their old
startup behavior; they do not call the new contribution. Other older builds do not gain
pre-workbench seeding merely by installing this feature.

The adapter seeds `com.microsoft.copilot.eclipse.ui` configuration preferences
`copilotQuickStartVersion=1` and `autoShowWhatsNew=false` **only when absent**.
It preserves user choices, propagates persistence failures to the GAMA startup logger,
and does not activate the upstream UI or duplicate its menus/chat. Its own disabled activity
hides the upstream status-bar contribution/menu. Generic GAML editor hooks remain in GAMA.
UI behavior is verified manually in GAMA.

## Locked dependencies

| Component | Pin / role |
|---|---|
| Copilot for Eclipse | Release **0.21.0**, p2 **0.21.0.202608060743** |
| Upstream distribution | GitHub release ZIP, SHA-256 `29e7b7f018a4c8bc4bf8d83d606448dc06606547c8e8fe6318510eff78aad5bb` |
| Copilot language server / native agents | **1.527.0**, supplied unchanged inside upstream bundles |
| Eclipse | **2026-03** release repository; JavaSE-21 minimum |
| Build | Tycho **5.0.2**, Maven **3.9.x** (CI: 3.9.16), JDK **21+** (CI: 25), Python **3.11+** |

[`upstream.lock.json`](upstream.lock.json) records the release URL, digest, source and Eclipse
baseline. The wrapper feature includes the **exact** upstream feature version. Its upstream
core, UI, jobs, terminal API, branding and filtered native agents are packaged together with
the mandatory Eclipse dependency closure by Tycho. Optional upstream integrations are not
silently promoted to required dependencies. The site does not redirect installers to the
mutable Azure upstream repository, and retains the original upstream feature's installation terms.

The Eclipse baseline is a named release repository, not a byte-for-byte lock of all Eclipse
artifacts. Copilot artifacts are digest-locked; the platform closure is resolved against that
baseline and retained in each published build. See [third-party terms](THIRD_PARTY.md) before redistribution.

## Source and build

Clone this repository and import its three projects into Eclipse using **Existing Projects
into Workspace**. It has its own parent POM, not GAMA's:

| Project | Purpose |
|---|---|
| `gama.ui.copilot` | Preference startup Runnable and status-bar activity |
| `gama.feature.copilot` | Stable installer contract and exact upstream pin |
| `gama.p2site.copilot` | Dependency-complete p2 repository and publication assembler |

Normal build, using the retained public site for the pinned upstream feature:

```sh
mvn -B -DskipTests package
```

For the first publication, offline preparation, or an upstream version upgrade, download and
verify the immutable release archive before invoking Tycho:

```sh
python3 scripts/prepare-upstream.py
mvn -B "-Dcopilot.upstream.repository=file:$(pwd)/.build/upstream" -DskipTests package
```

The script fails on digest or feature-pin mismatches. Output is
`gama.p2site.copilot/target/repository/`. No credentials or publishing actions are used by Maven.
For headless resolution, use the Equinox p2 director with that repository, Eclipse 2026-03,
and `-installIU gama.feature.copilot.feature.group`, setting `-p2.os`, `-p2.ws` and
`-p2.arch` for the target platform. A successful headless installation is not a UI acceptance test.

An external reactor may include this **whole root aggregator**, preserving its parent and module
layout. The default `copilot.upstream.repository` is an HTTPS p2 site, independent of the outer
reactor's working directory; no local `.build` directory is required after initial publication.
This explicitly opted-in source build is separate from ordinary GAMA builds. If the external
reactor merges p2 repositories, resolve this property's default value from this root POM.

To update upstream, review its release/native-agent notices, change the lock and the exact
`<includes>` version together, rebuild, and resolve all four platforms before publication.
Never replace or patch upstream JARs. File upstream functionality changes upstream.

## Independent publication

`.github/workflows/publish-copilot.yaml` runs for relevant module/build/lock/license changes
on `main`, validates pull requests without deployment, and supports **Run workflow**.
It verifies the upstream ZIP, builds the site, retains immutable repositories on `copilot-site`,
and deploys GitHub Pages. Pages must use **GitHub Actions** as its source.
The organization domain provides the stable URL above.

Each build's metadata is published under `releases/<run-id>-<attempt>/`. The root is a composite
repository listing all retained releases; metadata maps artifacts to a shared root-level pool.
Unchanged native agents are stored once across builds, with conflicting artifact bytes rejected.
Old metadata and artifact URLs are never overwritten or pruned automatically.
Each release retains its lock, license notices and source-commit provenance.
Keep the `copilot-site` branch. Native agents are large: monitor GitHub Pages' site/storage limits
as releases accumulate and migrate the retained site to suitable static storage before exceeding
those limits, preserving the stable URL and old paths.

## Issues and licenses

Report integration, installation, dependency and update-site issues
[here](https://github.com/gama-platform/gama.copilot/issues).
Report Copilot chat/completion/authentication bugs to
[microsoft/copilot-for-eclipse](https://github.com/microsoft/copilot-for-eclipse/issues);
report generic GAMA/GAML editor problems to [GAMA](https://github.com/gama-platform/gama/issues).
Include GAMA, Java, OS/architecture and installed feature versions, without tokens or private prompts.
See [CHANGELOG.md](CHANGELOG.md) for integration changes.

GAMA integration code is GPL-3.0; upstream binaries retain their own licenses.
See [LICENSE](LICENSE) and [THIRD_PARTY.md](THIRD_PARTY.md).
Copilot's service access, billing, privacy and trademarks are not granted by this repository's license.
