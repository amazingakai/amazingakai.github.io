+++
title = 'My Path to LFX Mentorship, and Some Advice for Future Mentees'
date = '2026-07-24T00:00:00+00:00'
tags = ['LFX', 'OpenTelemetry', 'Open Source', 'Mentorship']
featured = true
summary = "How a slow Discord bot led me to OpenTelemetry, why I applied to LFX Mentorship, and some advice for anyone thinking about applying themselves."
banner = '/images/my-lfx-mentorship-so-far-and-what-id-tell-future-mentees/opentelemetry-go-compile-instrumentation-hero.webp'
+++

![OpenTelemetry Go Compile Instrumentation Hero](/images/my-lfx-mentorship-so-far-and-what-id-tell-future-mentees/opentelemetry-go-compile-instrumentation-hero.webp)

## How I got here

I was building a Discord minigame as a side project in Python. It grew
bigger than I expected, and it started slowing down, partly due to code
I could've written better. Eventually I decided to rewrite it in Go,
mostly to see how much its concurrency model would help.

Separately, I realized that whatever language I ended up in, I wanted
real visibility into what the bot was actually doing, not just something
that told me when it crashed. So I tried instrumenting things manually,
and ran into two problems almost immediately. First, I didn't really know
what to instrument. Second, even following the docs, there was so much
boilerplate involved that I nearly gave up on the whole idea.

That's what pushed me toward auto-instrumentation, mostly as a way to
avoid the boilerplate. At the time, though, I was more interested in
learning how to instrument things properly than in auto-instrumentation
itself, that appreciation came later.

While looking into zero-code instrumentation solutions, I came across
[this old blog post](https://www.cncf.io/blog/2025/02/27/alibaba-datadog-and-quesma-join-forces-on-go-compile-time-instrumentation/)
announcing the new [OpenTelemetry Go Compile Instrumentation](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation)
project. One of the most appealing reasons for me to contribute was that there
was scope for adding new instrumentations, a learning chance for me
since I didn't know much about observability yet. The compiler-level
part also mattered to me, I already liked that kind of low-level work. On top of that, I'd separately been looking
for a CNCF project to contribute to. I introduced myself in the
project's Slack, asked some questions, and my first real contribution
was auto-instrumentation for `k8s.io/client-go`, though there were a
couple of smaller ones before that.

## Before this: GSoC @ KDE

This wasn't my first mentorship. In 2025, I was a GSoC mentee at KDE,
working on integrating KDE libraries into OSS-Fuzz under the guidance
of [Albert Astals Cid](https://invent.kde.org/aacid). At the time, I was
a total newbie to open source. That period taught me the ropes, both
technically and in terms of how contributing to a real project actually
works. I've written about that in more detail separately
([link]({{< ref "gsoc-2025-expanding-oss-fuzz-integration-across-kde-libraries.md" >}})),
and it's worth mentioning here because it's a big part of why I felt
ready to jump into OTel later.

## Why Mentorship again?

Two reasons, really.

The first was that I wanted to get better at communicating. LFX comes
with weekly SIG meetings and regular meetings with my mentors,
[Kemal Akkoyun](https://github.com/kakkoyun) and
[Dario Castañé](https://github.com/darccio). Having to regularly explain
what I've been working on to people who know the project well has been
good practice, especially since it isn't something that comes naturally
to me.

The second was that I wanted to go deeper into observability and
OpenTelemetry specifically, and get better at Go along the way. We're
still in the middle of the mentorship, but so far it's been exactly what
I was hoping for.

## Advice for future mentees

A few things that I think mattered, based on my own experience going
through this.

**Contributing is more than opening PRs.** Looking back at what actually
helped my application, joining community discussions, opening issues
when I found something worth raising, reviewing other people's PRs, and
sharing ideas even when I wasn't sure they'd go anywhere all mattered
just as much as the code I wrote. Mentors and maintainers see all of
that, not just your commit history.

Reviewing other people's PRs ended up helping me far more than I
expected. Reading different approaches, following review discussions,
and seeing why maintainers asked for certain changes taught me things I
wouldn't have learned nearly as quickly by only writing my own code.

Consistency also matters more than volume. You don't need dozens of PRs
to stand out. Showing up regularly, staying involved in discussions,
attending meetings when you can, and gradually becoming part of the
community leaves a much stronger impression than trying to maximize your
contribution count over a few weeks.

**Be genuine about why you're there.** From what I've seen, it's fairly
easy for mentors and maintainers to tell the difference between someone
who's actually excited about a project and someone who's mainly
interested in the resume line. You can want both, a career boost and
genuine interest at the same time, but if the interest isn't real, it
tends to show once the work gets less glamorous.

**Don't disappear if you're not selected.** LFX mentorship slots are
limited, not getting selected doesn't say anything about your ability.
If you were seriously contributing during the application period, you
already learned something real, keep using it. That doesn't stop
mattering just because one specific mentorship round didn't go your way.
You can keep contributing to the project on your own, and there's always
a next round.

**Don't hesitate to ask.** Whether it's a basic question about the
codebase, something you think might be obvious, or just wanting to
double check you're on the right track, ask. I did this myself when I
first joined the project's Slack, and no one made me feel bad about it.
Most maintainers would rather answer a simple question early than review
a PR that went in the wrong direction because you guessed instead of
asking.

**On using AI tools.** I do use AI tools regularly, but where and how
varies. For code, I use it sometimes, mostly for parts I already
understand well, where I'm confident I could write it myself but don't
need to grind through it by hand to learn something new. Where I use it
a lot more is research and understanding things, I reach for an LLM over
Google search these days because it explains things faster than digging
through search results and docs myself.

Wherever I use it, I double check everything it gives me. I review
answers against the actual source, and I review AI-assisted code
multiple times before submitting it.

Reviewers are volunteering their time, so submitting unreviewed
AI-generated code doesn't just leave a bad impression, it's
disrespectful. Make sure you're following whatever AI usage guidelines
the project you're contributing to has. Also question AI-generated code
critically: ask why something was done a certain way, whether it's
actually needed, read through the surrounding code, and check if
there's a simpler solution.

More generally, whether code comes from AI, Stack Overflow, or another
contributor, you're the one submitting it. Make sure you understand it
well enough to explain every part of it during review.

## Closing thoughts

This mentorship also convinced me I want to be on the other side of it.
I'll be mentoring a project myself in the next LFX term, co-mentoring
with [Xabier Martinez](https://github.com/txabman42). You can check out
the project [here](https://mentorship.lfx.linuxfoundation.org/project/3db981bf-404b-4c8e-96f8-b0433688e8cf).
I'm looking forward to it, partly because I want to try being the kind
of mentor Kemal, Dario, and Albert have been for me. I'll write more
about the mentorship itself once it wraps up, and separately about the
actual technical work I did on otelc.

## Acknowledgements

Thanks to my mentors, [Kemal Akkoyun](https://github.com/kakkoyun) and
[Dario Castañé](https://github.com/darccio), for their guidance so far
during the mentorship. I'd also like to thank
[Xabier Martinez](https://github.com/txabman42), who was one of the first
maintainers I interacted with on the project, along with everyone else in
the OpenTelemetry Go Compile Instrumentation community for the reviews,
discussions, and feedback along the way.
