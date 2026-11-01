# Third-party software and service terms

## GAMA integration

`gama.ui.copilot`, the wrapper feature and build/publication code are GPL-3.0.
The full license is in [LICENSE](LICENSE). GPL does not relicense separate third-party artifacts
aggregated in the p2 repository.

## Unmodified Copilot for Eclipse

Source and release: <https://github.com/microsoft/copilot-for-eclipse/tree/0.21.0>.
The release is MIT-licensed, copyright Microsoft Corporation.
The MIT notice is retained in [licenses/copilot-eclipse-MIT.txt](licenses/copilot-eclipse-MIT.txt).
Its upstream branding/feature and service terms remain unchanged in the mirrored JARs.
No upstream source is forked or rebuilt here.

The pinned release uses `@github/copilot-language-server` **1.527.0** and matching platform
packages. These packages declare the MIT license, separately from the service subscription.
The language server MIT notice is retained in
[licenses/copilot-language-server-MIT.txt](licenses/copilot-language-server-MIT.txt).
Native binaries, runtime components and bundled third-party notices remain part of the unmodified
agent JARs. Their notices must accompany redistribution; do not strip files from those JARs.
This permission to redistribute software does not provide Copilot service access or a trademark license.

Provenance:

- [Upstream MIT license at 0.21.0](https://github.com/microsoft/copilot-for-eclipse/blob/0.21.0/LICENSE)
- [Exact agent dependency declarations](https://github.com/microsoft/copilot-for-eclipse/blob/0.21.0/com.microsoft.copilot.eclipse.core/copilot-agent/package.json)
- [Language server package metadata](https://registry.npmjs.org/@github/copilot-language-server/1.527.0)

The upstream feature presents GitHub Copilot's terms during installation, including
[product-specific terms](https://github.com/customer-terms/github-copilot-product-specific-terms),
acceptable-use requirements and data collection provisions. Users need their own entitlement.
Review GitHub/Microsoft privacy and telemetry settings before sending private source or prompts.

## Eclipse and other dependencies

The p2 build resolves the mandatory closure from Eclipse 2026-03. Eclipse Platform components
are generally EPL-2.0; bundled libraries may use Apache, BSD, MIT or other licenses.
Every included feature/bundle retains its own original license, notices and signatures.
The resulting `content.jar` records feature license metadata; JAR `about.html`, `about_files`,
`META-INF` and other notices remain intact. Source offerings remain available through each
component's upstream project/release. Do not describe the whole update site as GPL-only or MIT-only.

Re-review licenses and source availability when updating the lock or baseline. The exact upstream
ZIP is verified before packaging; installation never relies on the moving upstream update site.
