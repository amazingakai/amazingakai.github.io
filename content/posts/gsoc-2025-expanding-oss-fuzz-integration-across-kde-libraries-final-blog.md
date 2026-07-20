+++
title = 'GSoC 2025: Expanding OSS-Fuzz Integration Across KDE Libraries (Final Update)'
date = '2025-08-30T20:00:00+05:30'
tags = ['GSoC', 'KDE', 'OSS-Fuzz']
+++

Hello everyone, this is going to be the final blog post of my GSoC 2025 project. In this post, I will summarize the progress made during the project and discuss the future plans for expanding OSS-Fuzz integration across KDE libraries.

### Quick Recap Of Progress

So far, I had integrated several KDE libraries into OSS-Fuzz, including KMime, KIO-Extras/thumbnail, and KFileMetaData (submitted for integration).

I have also moved existing projects from OSS-Fuzz repository to KDE repositories.

## Progress After Midterm

After midterm, in the first half I focused on integrating new thumbnailers into OSS-Fuzz. I had already integrated KIO-Extras/thumbnail, and I continued with KDEGraphics-Thumbnailers, KDESDK-Thumbnailers, and FFMpeg-Thumbs.

After that, I mostly worked on improving the existing integration, i.e, testing the fuzzers and fixing any issues, moving to CMake based setup instead of manual compilation of the fuzzers and adding documentation for local testing of the fuzzers.

The CMake setup allowed for easier maintenance however, it wasn't as simple as it may seem. Since OSS-Fuzz recommends using static builds, many of the libraries didn't link to their transitive dependencies correctly for static builds. This required changes to those libraries (.pc files, .cmake files, etc) for proper static linking.

The existing setup also lacked documentation for local testing of the fuzzers. I have added documentation for almost all of the fuzzers. This will be helpful for developers to integrate new fuzzers (such as new thumbnailers or KFileMetaData extractors).

## Future Plans

With the initial setup of thumbnailers and KFileMetaData, it is easy to integrate new thumbnailers and KFileMetaData extractors. Currently there are a few more thumbnailers that could be integrated into OSS-Fuzz, I plan to work on integrating them soon as well, the list is here:

- [Calligra Thumbnailer](https://invent.kde.org/office/calligra/-/tree/master/extras/thumbnail)
- [Itinerary Thumbnailer](https://invent.kde.org/pim/itinerary/-/tree/master/src/thumbnailer)
- [Qui Thumbnailer](https://invent.kde.org/sdk/kde-dev-utils/-/blob/master/kuiviewer/quicreator.cpp)
- [MLT Thumbnailer](https://invent.kde.org/multimedia/kdenlive/-/tree/master/thumbnailer)
- [WebArchive Thumbnailer](https://invent.kde.org/network/konqueror/-/tree/master/plugins/webarchiver/thumbnailer)
- [Pala Thumbnailer](https://invent.kde.org/games/palapeli/-/tree/master/mime)
- [Font Thumbnailer](https://invent.kde.org/plasma/plasma-workspace/-/tree/master/kcms/kfontinst/thumbnail)

### Links

- Intro Blog post: [amazingakai.github.io/posts/gsoc-2025-expanding-oss-fuzz-integration-across-kde-libraries](/posts/gsoc-2025-expanding-oss-fuzz-integration-across-kde-libraries)
- Midterm Blog post: [amazingakai.github.io/posts/gsoc-2025-expanding-oss-fuzz-integration-across-kde-libraries-midterm-blog](/posts/gsoc-2025-expanding-oss-fuzz-integration-across-kde-libraries-midterm-blog)

---

### Thank You

I would like to thank my mentor, Albert Astals Cid, and the KDE community for their guidance throughout this project. Their feedback was helpful in successfully expanding OSS-Fuzz integration across KDE libraries.
