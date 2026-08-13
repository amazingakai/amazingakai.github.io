+++
title = 'Building Import-Driven Instrumentation for otelc'
date = '2026-08-12T12:00:00+05:30'
tags = ['LFX', 'OpenTelemetry', 'Go', 'Observability', 'Open Source']
featured = true
summary = "How I got involved with OpenTelemetry Go Compile Instrumentation through LFX Mentorship, and the work I did on import-driven instrumentation selection."
+++

In [my last post](/posts/my-lfx-mentorship-so-far-and-what-id-tell-future-mentees), I wrote about how I got into OpenTelemetry Go Compile
Instrumentation and applied to LFX Mentorship. This one is about the
actual work, what I built, the bugs I ran into, and how I fixed them.

## Why otelc specifically?

I'm interested in both low-level tooling and observability, and otelc
sits right at the intersection of the two. That's really what pulled me
toward this project instead of OpenTelemetry in general.

## What is otelc, briefly?

otelc instruments Go code at compile time. Instead of requiring developers to
manually instrument their code, otelc rewrites the program during compilation
so that instrumentation is inserted automatically. The rest of this post assumes
a little bit of that context, so here's the short version before I get into
what I actually worked on.

## What I worked on

### Import-driven instrumentation selection

otelc ships with a built-in set of instrumentations, each made up of
modules and rule files. But there was no good way to bring in third-party
instrumentations easily, and no way to disable a built-in instrumentation
at compile time (you could only toggle them at runtime).

This came up in a SIG meeting, and was tracked in
[this issue](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation/issues/567).
Orchestrion, Datadog's own compile-time instrumentation tool for Go,
already had a solution: an `orchestrion.tool.go` file that developers
could use to declare instrumentation explicitly. We used that as a
starting point and built something similar for otelc.

The mechanism works like this: otelc looks for a file (`otel.instrumentation.go`,
or `otelc.tool.go` as an alias) containing a list of blank imports. This
file isn't included in the actual build (it's marked with a `tools`
build tag, following the standard `tools.go` convention), but Go still
tracks its imports in `go.mod`. otelc reads this file before building,
loads the imported packages using `golang.org/x/tools/go/packages`, and scans
each package's directory for rule files (`otelc.yaml`, `*.otelc.yaml`)
or another `otel.instrumentation.go`, allowing instrumentation packages
to bundle together other instrumentation packages. Those rule files
define how to instrument that package.

Here's roughly what one of these files looks like in practice:

```go
//go:build tools

package tools

import (
    _ "go.opentelemetry.io/otelc/instrumentation/net/http/client"
    _ "..."
)
```

![OpenTelemetry Go Compile Instrumentation Import-Driven Instrumentation Flow](/images/building-import-driven-instrumentation-for-otelc/otelc-import-driven-instrumentation-flow-light.webp)
![OpenTelemetry Go Compile Instrumentation Import-Driven Instrumentation Flow](/images/building-import-driven-instrumentation-for-otelc/otelc-import-driven-instrumentation-flow-dark.webp)

The naming itself was already decided in a UX design document from before
I joined the project, so that part was settled. I'd originally written this
as a single PR, but it ended up being around 5,000 lines, which was far
too large to review properly. Reviewers asked me to split it into smaller
PRs, so I did. During that process, one review comment asked for an integration
test covering a recursive instrumentation path, where one `otel.instrumentation.go`
file references another. Writing that test surfaced a real bug: otelc was only
looking for hook code files inside its own embedded bundle, not in packages loaded
from external import paths. If that comment hadn't come up, this bug might
have gone unnoticed for a while. I fixed it by updating otelc to load hook code
through `golang.org/x/tools/go/packages` as well. The implementation landed across a couple of
PRs: the hook loading fix in [#617](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation/pull/617),
followed by the core import-driven instrumentation support in
[#612](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation/pull/612).

### The initInstrumentation deadlock

Every instrumentation in otelc followed the same rough pattern: lazily
set up the OTel SDK (if it wasn't already running) and start runtime
metrics, guarded by a `sync.Once`.

This caused a deadlock. Here's what happened: when
a user's code called `grpc.NewClient`, the gRPC instrumentation hook would
call `initInstrumentation`, which runs inside a `sync.Once.Do`. If the
user had their OTLP exporter configured to use gRPC, the SDK setup inside
that same `Once.Do` would itself call `grpc.NewClient`, which tried to
call `initInstrumentation` again, re-entering the same `Once.Do` block
that hadn't finished running yet. That's a deadlock.

![OpenTelemetry Go Compile Instrumentation initInstrumentation Deadlock Sequence](/images/building-import-driven-instrumentation-for-otelc/otelc-initinstrumentation-deadlock-sequence-light.webp)
![OpenTelemetry Go Compile Instrumentation initInstrumentation Deadlock Sequence](/images/building-import-driven-instrumentation-for-otelc/otelc-initinstrumentation-deadlock-sequence-dark.webp)

My first fix was simpler than it should have been: check the value of
`OTEL_EXPORTER_OTLP_ENDPOINT` and skip instrumentation for any
`grpc.NewClient` call pointed at that endpoint. That worked for the
obvious case, but it broke down as soon as the two values didn't match
exactly, since the values could point at the same collector without
matching as strings at all:

```text
endpoint = "http://collector-localhost:4317"
target   = "localhost:4317"
```

This kept happening because I was relying on dumb string comparison to
detect whether the two calls pointed at the same target. Instead of
trying to make that comparison smarter, I took a different approach.

The fix was to stop having every instrumentation independently lazy-init
the SDK. Instead, I moved that startup logic out into a single injected
rule that runs once in the user's main package, before any instrumentation
hook runs. Every hook can now assume the SDK is already set up by the time
it runs, so there's no endpoint comparison to get wrong in the first
place. It also meant third-party rules don't need to follow the old init pattern at all,
they can simply assume the SDK is already available, which fit nicely with the
import-driven instrumentation work happening around the same time. Users who
want to bring their own tracer or meter provider can also remove this rule and wire
up their own. The implementation landed in [#625](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation/pull/625).

### otelc pin and auto-pinning

The second thing I worked on was the `otelc pin` command, which generates
an `otel.instrumentation.go` file based on a user's dependency graph,
inspired by Orchestrion's own `pin` command. Orchestrion's version points
to a single package that bundles every integration together. I changed
this so `otelc pin` looks at the user's actual dependencies and infers
which instrumentations are relevant, rather than pulling in everything.

`otelc pin` also keeps the generated file clean by automatically removing
imports that don't resolve to any rule files (or other
`otel.instrumentation.go` files). The result is an explicit list of the
instrumentations that are actually relevant to the project.

Auto-pinning was also mentioned in the original issue, but initially I
wasn't convinced it was necessary. If a project didn't have an
`otel.instrumentation.go` file, otelc could simply fall back to its default
instrumentations. Generating a temporary file just to represent that default
set seemed like an unnecessary extra step.

While testing otelc against a project using an older version of gRPC, I ran into
another problem. I already had a fix open for that problem, but auto-pinning
addressed its underlying cause in a much cleaner way.

At the time, otelc's build process matched instrumentation rules first,
then added the matched instrumentation modules to `go.mod` and ran
`go mod tidy`. That dependency resolution could bump the project's gRPC
version. The instrumentation rules had already been selected against the
old version, though, so otelc could end up building against a dependency
graph different from the one it had used to decide which rules to apply
which resulted in the build failing.

My original fix was to run the setup process in multiple passes until the
dependency graph stopped changing. It worked, but auto-pinning turned out to
solve the same problem much more cleanly.

`otelc go build` now generates a temporary `otel.instrumentation.go` early
when the user hasn't provided one. Dependencies are resolved and added to
`go.mod` as part of that pinning phase, before rule matching happens. By
the time otelc selects instrumentation rules, it's looking at the dependency
versions that will actually be used for the build. The setup phase that
follows no longer needs to modify the dependency graph, so the selected
rules stay valid.

![OpenTelemetry Go Compile Instrumentation Auto-Pinning Before/After](/images/building-import-driven-instrumentation-for-otelc/otelc-autopinning-before-after-light.webp)
![OpenTelemetry Go Compile Instrumentation Auto-Pinning Before/After](/images/building-import-driven-instrumentation-for-otelc/otelc-autopinning-before-after-dark.webp)

This also gives us a cleaner path toward
[registry-backed integration search](#whats-next). If otelc eventually
discovers compatible instrumentations from the [OpenTelemetry Ecosystem Explorer](https://github.com/open-telemetry/opentelemetry-ecosystem-explorer)
registry, the same pinning step can resolve those integrations and their
dependencies before rule matching, rather than requiring the rest of the build
pipeline to care where an instrumentation came from. I talk more about that idea
in the registry-backed integration section below.

One rough edge that's still open is that `otelc pin` currently adds
`replace` directives pointing to local paths in `go.mod`, which makes
checking the generated file into version control awkward. Decoupling
instrumentations from the tool itself, also described below, should fix
that. The initial implementation landed in [#655](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation/pull/655).

## What's next

A few things I'm looking at for the rest of the mentorship:

1. **Decoupling instrumentations from otelc's embedded bundle.** Right
   now, instrumentation packages are embedded directly into the otelc
   binary. That means adding a new instrumentation requires a new release
   of the tool, even if it's otherwise fully compatible. Decoupling this
   would also let us build a proper dependency graph between
   instrumentations (for example, automatically pulling in a runtime/GLS
   instrumentation whenever the OTel SDK instrumentation is used), and
   would let users check reproducible `otel.instrumentation.go` files
   into their own repos without local path replaces.

2. **Registry-backed integration search.** Instead of only looking at the
   embedded bundle, otelc could look up compatible instrumentations
   through the [OpenTelemetry Ecosystem Explorer](https://github.com/open-telemetry/opentelemetry-ecosystem-explorer)
   registry, which would let third-party instrumentations get picked up
   automatically once published there. This is currently being
   researched, see
   [this issue](https://github.com/open-telemetry/opentelemetry-ecosystem-explorer/issues/916)
   for the open questions around how Go compile-time instrumentations
   should be represented there and how otelc would consume that data.

3. **Supporting `.otel.yml` files.** Similar in spirit to
   `otel.instrumentation.go`, but without tracking dependencies in
   `go.mod`. Useful for customizing instrumentations without wanting them
   tracked in version control, though it won't produce fully reproducible
   builds.

## Acknowledgements

The work described here went through a lot of review. Thanks to
[Kemal Akkoyun](https://github.com/kakkoyun) for raising the original
issue that led to import-driven instrumentation selection, and to both
[Kemal](https://github.com/kakkoyun) and
[Dario Castañé](https://github.com/darccio) for reviewing the PRs linked
throughout this post, including the review comment that led me to the
recursive-instrumentation bug. Thanks also to everyone else in the
OpenTelemetry Go Compile Instrumentation community who reviewed and
discussed this work along the way.
