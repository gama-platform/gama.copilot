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
[Microsoft's Copilot repository](https://azuredownloads-g3ahgwb5b8bkbxhd.b01.azurefd.net/github-copilot/)
and [Eclipse 2026-03 repository](https://download.eclipse.org/releases/2026-03/) available
for dependencies. The GAMA site advertises both references; enable **Contact all update sites
during install to find required software** in the Eclipse installer.
A Copilot entitlement and network access to GitHub's services are required.

The baseline is **Eclipse 2026-03 (4.39), Java 21+**. Supported GAMA platforms:
Linux GTK x86_64, Windows x86_64, macOS Cocoa x86_64 and aarch64 (Apple Silicon).
The upstream feature also declares Linux aarch64; that is not a supported GAMA target here.
The installed feature retains the upstream native-agent platform filters.
For this GAMA version, keep the platform on **2026-03**, not `latest` or a newer release
repository. If a future Copilot release needs a newer Eclipse, resolution must fail rather
than upgrade the platform baseline. Disable newer Eclipse repositories for manual installation.

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

## Dependencies and updates

| Component | Compatibility / role |
|---|---|
| Copilot for Eclipse | **[0.21.0, 1.0.0)**; initially validated with **0.21.0.202608060743** |
| Copilot language server / native agents | Managed and delivered by Microsoft's feature, not mirrored here |
| Eclipse | **2026-03** release repository; JavaSE-21 minimum |
| Eclipse Terminal | `org.eclipse.terminal.feature` **[1.0.200, 2.0.0)** from Eclipse 2026-03; required by the wrapper because Copilot checks for its bundles only at runtime |
| Build | Tycho **5.0.2**, Maven **3.9.x** (CI: 3.9.16), JDK **21+** (CI: 25), Python **3.11+** |

This is a **thin site**: it distributes only `gama.ui.copilot` and `gama.feature.copilot`.
The wrapper requires, rather than includes, Microsoft's upstream feature. Copilot core, UI,
language servers and native agents are downloaded directly from Microsoft; Eclipse dependencies
come from Eclipse. No upstream binaries or platform closure are copied into the GAMA site.

The compatible range permits upstream 0.x releases without rebuilding the wrapper for each
agent update. This is a declared compatibility window, not a claim that every future release
has been tested: upstream must also resolve against the installed Eclipse/Java environment.
Eclipse's normal **Check for Updates** mechanism updates installed Copilot components;
this integration does not silently update agents.

Microsoft's site is mutable. Older releases can disappear, so old GAMA wrapper releases do
not guarantee reproducible offline installs. A future breaking upstream release may require a
new adapter/range or Eclipse baseline. See [third-party terms](THIRD_PARTY.md).

## Source and build

Clone this repository and import its three projects into Eclipse using **Existing Projects
into Workspace**. It has its own parent POM, not GAMA's:

| Project | Purpose |
|---|---|
| `gama.ui.copilot` | Preference startup Runnable and status-bar activity |
| `gama.feature.copilot` | Stable installer contract and compatible upstream requirement |
| `gama.p2site.copilot` | Thin p2 repository and retained-release publisher |

Build against Microsoft's public p2 site and Eclipse 2026-03:

```sh
mvn -B -DskipTests package
```

Output is `gama.p2site.copilot/target/repository/`. No archive preparation, credentials or
publishing actions are used by Maven. For headless resolution, use the Equinox p2 director
with that repository, Microsoft's Copilot repository, Eclipse 2026-03,
and `-installIU gama.feature.copilot.feature.group`, setting `-p2.os`, `-p2.ws` and
`-p2.arch` for the target platform. A successful headless installation is not a UI acceptance test.

An external reactor may include this **whole root aggregator**, preserving its parent and module
layout. The default `copilot.upstream.repository` is an HTTPS p2 site, independent of the outer
reactor's working directory; no local `.build` directory or initial publication is required.
This explicitly opted-in source build is separate from ordinary GAMA builds. If the external
reactor merges p2 repositories, resolve this property's default value from this root POM.

Before changing the compatibility range or Eclipse baseline, review upstream changes, rebuild,
and resolve all four supported platforms. Do not copy or patch upstream JARs here.
File upstream functionality changes upstream.

## Independent publication

`.github/workflows/publish-copilot.yaml` runs for relevant module/build/license changes
on `main`, validates pull requests without deployment, and supports **Run workflow**.
It builds the site, verifies that only the two GAMA artifacts are present,
retains immutable repositories on `copilot-thin-site`,
and deploys GitHub Pages. Pages must use **GitHub Actions** as its source.
The organization domain provides the stable URL above.

Each small GAMA build is published under `releases/<run-id>-<attempt>/`. The root is a composite
repository listing all retained thin releases and the external dependency repository references.
Old GAMA artifacts are not overwritten or pruned automatically.
Each release retains its license notices and source-commit provenance.
Keep the `copilot-thin-site` branch. It starts independently of the earlier mirrored
`copilot-site` publication so no old agent pool is included in new Pages deployments.

## Issues and licenses

Report integration, installation, dependency and update-site issues
[here](https://github.com/gama-platform/gama.copilot/issues).
Report Copilot chat/completion/authentication bugs to
[microsoft/copilot-for-eclipse](https://github.com/microsoft/copilot-for-eclipse/issues);
report generic GAMA/GAML editor problems to [GAMA](https://github.com/gama-platform/gama/issues).
Include GAMA, Java, OS/architecture and installed feature versions, without tokens or private prompts.
See [CHANGELOG.md](CHANGELOG.md) for integration changes.

GAMA integration code is GPL-3.0; externally supplied dependencies retain their own licenses.
See [LICENSE](LICENSE) and [THIRD_PARTY.md](THIRD_PARTY.md).
Copilot's service access, billing, privacy and trademarks are not granted by this repository's license.
