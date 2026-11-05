# Third-party software and service terms

## GAMA integration

`gama.ui.copilot`, the wrapper feature and build/publication code are GPL-3.0.
The full license is in [LICENSE](LICENSE). This thin p2 repository distributes only GAMA's
adapter and wrapper feature. GPL does not relicense externally installed dependencies.

## Unmodified Copilot for Eclipse

Initially validated release: <https://github.com/microsoft/copilot-for-eclipse/tree/0.21.0>.
This release is MIT-licensed, copyright Microsoft Corporation.
Microsoft's update site supplies its feature, branding, agents and associated terms directly.
No upstream source is forked, rebuilt or redistributed here.

The initially validated release uses `@github/copilot-language-server` **1.527.0** and matching platform
packages. These packages declare the MIT license, separately from the service subscription.
These details document the initially validated dependency; they do not assert that future
upstream versions have identical licensing. Native binaries, runtime components and bundled
third-party notices are supplied by Microsoft. Review the terms of the version being installed.
Software licensing does not provide Copilot service access or a trademark license.

Provenance:

- [Upstream MIT license at 0.21.0](https://github.com/microsoft/copilot-for-eclipse/blob/0.21.0/LICENSE)
- [Exact agent dependency declarations](https://github.com/microsoft/copilot-for-eclipse/blob/0.21.0/com.microsoft.copilot.eclipse.core/copilot-agent/package.json)
- [Language server package metadata](https://registry.npmjs.org/@github/copilot-language-server/1.527.0)

The upstream feature presents GitHub Copilot's terms during installation, including
[product-specific terms](https://github.com/customer-terms/github-copilot-product-specific-terms),
acceptable-use requirements and data collection provisions. Users need their own entitlement.
Review GitHub/Microsoft privacy and telemetry settings before sending private source or prompts.

## Eclipse and other dependencies

The build and installation resolve platform dependencies from Eclipse 2026-03, without
mirroring them into the GAMA site. Eclipse Platform components
are generally EPL-2.0; bundled libraries may use Apache, BSD, MIT or other licenses.
Each external feature/bundle has its own license, notices and signatures, supplied by its publisher.
Source offerings remain available through each component's upstream project/release.

Re-review licenses when updating the compatibility range or baseline. Installation deliberately
depends on Microsoft's moving update site and Eclipse's release site, rather than retained
copies of their binaries.
