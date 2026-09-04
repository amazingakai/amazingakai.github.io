+++
title = 'My LFX Mentorship at OpenTelemetry Has Come to an End'
date = '2026-09-04T00:00:00+05:30'
tags = ['LFX', 'OpenTelemetry', 'Open Source', 'Mentorship']
featured = true
summary = "Looking back on my LFX Mentorship at OpenTelemetry Go Compile Instrumentation, what shipped, what I gained, and what's next."
+++

My LFX Mentorship at OpenTelemetry Go Compile Instrumentation (otelc) has
ended. I've already written about
[how I got here and why I applied](/posts/my-lfx-mentorship-so-far-and-what-id-tell-future-mentees/)
and about [the technical work](/posts/building-import-driven-instrumentation-for-otelc/),
so this one's just a short summary and reflection.

## What shipped

The biggest piece of work was import-driven instrumentation selection,
covered in [my last post](/posts/building-import-driven-instrumentation-for-otelc/).

The other piece, registry-backed integration search through the
[OpenTelemetry Ecosystem Explorer](https://github.com/open-telemetry/opentelemetry-ecosystem-explorer),
is still in progress. We're also migrating otelc's instrumentations into
a separate contrib repo, which should make this kind of work easier to
build on. I'll write about these in a future post.

## What I gained

Getting better at communication was one of the reasons I applied. I was
always fine talking async over GitHub, comments, reviews, PR
descriptions, but I didn't have much confidence in live SIG meetings or
calls. Weekly SIG meetings and regular syncs with my mentors fixed that.

I'm also a lot more interested in observability than when I started. I
want to keep exploring the OpenTelemetry ecosystem, mainly around Rust
and eBPF. I'm graduating in about a year, and this mentorship is a big
part of why I'm now seriously looking at observability as a career
direction.

The project got a lot of traction during my mentorship, we submitted
two project proposals for the next LFX term, so alongside my own
contributions I reviewed many PRs. Reading other people's approaches and
review discussions taught me things faster than writing my own code
ever did.

## What's next

I'm mentoring a project myself next term, co-mentoring with
[Xabier Martinez](https://github.com/txabman42). I'm also planning to
stay in touch with my mentors and everyone else I've gotten to know
through this.

## Thank you

Thanks to my mentors, and to the OpenTelemetry and CNCF community, for
everything over the past few months. ❤️
