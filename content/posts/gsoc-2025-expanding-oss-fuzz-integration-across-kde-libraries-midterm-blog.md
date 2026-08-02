+++
title = 'GSoC 2025: Expanding OSS-Fuzz Integration Across KDE Libraries (Midterm Update)'
date = '2025-07-23T20:00:00+05:30'
tags = ['GSoC', 'KDE', 'OSS-Fuzz']
+++

Hello everyone! Midterm evaluations are here, and I wanted to share an update on my GSoC project. Here's what I've accomplished so far:

### Progress So Far

#### Migration of Existing Fuzz Targets

The first step was migrating the existing build scripts and fuzz targets from the OSS-Fuzz repository into the respective KDE repositories. Maintaining them within the OSS-Fuzz repo added a bit of friction when making changes. Having them in KDE repos makes it easier to maintain and update them.

#### KArchive Fuzzer

Then I worked on **KArchive** fuzzer doing mainly two changes: First was to split the fuzzer into separate targets for each archive format (like zip, tar, 7z, etc.) to improve coverage. Second was to add libFuzzer dictionary files to guide the fuzzing process better. Here is an image showing the coverage after these changes:

![KArchive Fuzzer](/images/gsoc-2025-expanding-oss-fuzz-integration-across-kde-libraries-midterm-blog/gsoc-2025-oss-fuzz-karchive-fuzzer.webp)

This coverage was tested using a local corpus and it is pretty solid for just fuzzing the "reading" part. The coverage will increase on OSS-Fuzz by time as the corpus keeps growing. Splitting the fuzzer into multiple targets allows the fuzzer to focus on specific archive formats, which keeps the corpus size smaller and more efficient.

#### KMime Fuzzer

After that, I focused on **KMime**. I created a fuzz target for it, which focused on the just the MIME parsing functionality. The parsing part of KMime is critical as it handles untrusted input, such as, from emails (in KMail).

![KMime Fuzzer](/images/gsoc-2025-expanding-oss-fuzz-integration-across-kde-libraries-midterm-blog/gsoc-2025-oss-fuzz-kmime-fuzzer.webp)

For KMime, I also added a libFuzzer-style dictionary file to help guide the fuzzing process. This helps the fuzzer generate more meaningful inputs, which can improve coverage and help the fuzzer reach deeper code paths.

#### KDE Thumbnailers Fuzzer

After KMime, I moved on to **KDE Thumbnailers**. I created a fuzzer for the thumbnailers that are used in KDE applications to generate previews of files. This is important as it handles untrusted input from various file formats, such as images, documents, etc. KDE has a lot of thumbnailers, I started with the thumbnailers in **KIO-Extras** repository, which includes thumbnailers for various file formats like images, videos, documents, etc.

**KDE Thumbnailers** were tricky to fuzz because they aren't standalone. They depend on KIO and KIOGui, which are pretty heavy and pull in a bunch of dependencies not required for thumbnailing. Building the full KIO stack inside OSS-Fuzz would have made the build process slow and complicated.

To avoid that, I wrote a custom build script that compiles just the thumbnailer source files and their direct dependencies. That keeps the fuzzers lightweight and focused only on the thumbnailing functionality.

![KDE Thumbnailers Fuzzer](/images/gsoc-2025-expanding-oss-fuzz-integration-across-kde-libraries-midterm-blog/gsoc-2025-oss-fuzz-kde-thumbnailers-fuzzer.webp)

For these thumbnailers, I also created a dictionary file for each thumbnailer separately for the same reason as KMime.

#### KFileMetaData Fuzzer

At last, I worked on **KFileMetaData**. This library is used to extract metadata from files, such as images, videos, documents, etc. Same as KDE Thumbnailers, it handles untrusted input from various file formats, so fuzzing it is important to ensure it can handle malformed or unexpected data gracefully.

Initially, I made a single fuzzer that used Qt plugin system to load metadata extractors and ran the extractors based on content mimetype. However, this required using dynamic libraries which is not great for OSS-Fuzz integration. So I split the fuzzer into multiple targets, one for each extractor, and compiled them statically. This way, each fuzzer is focused on a specific extractor and doesn't depend on dynamic linking.

![KFileMetaData Fuzzer](/images/gsoc-2025-expanding-oss-fuzz-integration-across-kde-libraries-midterm-blog/gsoc-2025-oss-fuzz-kfilemetadata-fuzzer.webp)

The thumbnailers and kfilemetadata currently have the highest coverage among all the fuzzers I've created so far, which is great! The coverage will improve and reach closer to 100% for them as the corpus grows on OSS-Fuzz.

### What's Next

There are still many more libraries that could benefit from OSS-Fuzz integration. Here are some that I plan to work on next:

#### More Thumbnailers

KDE maintains a large number of thumbnailer plugins, and I intend to integrate as many of them as possible. The next ones on my list (provided by Albert Astals Cid) include:

- [Calligra Thumbnailer](https://invent.kde.org/office/calligra/-/tree/master/extras/thumbnail)
- [Itinerary Thumbnailer](https://invent.kde.org/pim/itinerary/-/tree/master/src/thumbnailer)
- [Qui Thumbnailer](https://invent.kde.org/sdk/kde-dev-utils/-/blob/master/kuiviewer/quicreator.cpp)
- [KDE Graphics Thumbnailers](https://invent.kde.org/graphics/kdegraphics-thumbnailers)
- [MLT Thumbnailer](https://invent.kde.org/multimedia/kdenlive/-/tree/master/thumbnailer)
- [KDE SDK Thumbnailers](https://invent.kde.org/sdk/kdesdk-thumbnailers)
- [WebArchive Thumbnailer](https://invent.kde.org/network/konqueror/-/tree/master/plugins/webarchiver/thumbnailer)
- [Pala Thumbnailer](https://invent.kde.org/games/palapeli/-/tree/master/mime)
- [Font Thumbnailer](https://invent.kde.org/plasma/plasma-workspace/-/tree/master/kcms/kfontinst/thumbnail)

#### Okular Generators & QMobipocket

[QMobipocket](https://invent.kde.org/graphics/kdegraphics-mobipocket/) is a library used by Okular for reading `.mobi` files. It parses Mobipocket documents and could benefit from fuzzing to identify edge cases and potential vulnerabilities.

Okular also includes several [generators](https://invent.kde.org/graphics/okular/-/tree/master/generators) responsible for rendering various document formats. While most rely on third-party libraries, a few include custom code that has not yet been fuzzed. These components may be susceptible to bugs triggered by malformed files.

Fuzzing these generators is a bit tricky, since building the full Okular application and all its dependencies would slow down the build process and make its maintenance harder. To address this, I plan to build only the relevant generator source files and their minimal dependencies similar to the approach I used for KDE thumbnailers.

#### KContacts (VCard Parser)

[KContacts](https://invent.kde.org/frameworks/kcontacts) is a KDE framework for handling contact data. It includes a VCard parser that reads `.vcf` files. Although the format is relatively simple, it supports multiple character encodings and codecs, making it an interesting candidate for fuzz testing.

### Links

- Intro Blog post: [amazingakai.github.io/posts/gsoc-2025-expanding-oss-fuzz-integration-across-kde-libraries]({{< ref "gsoc-2025-expanding-oss-fuzz-integration-across-kde-libraries.md" >}})

That's it for now. If you're working on/know a KDE library that touches untrusted input and could benefit from fuzzing, please let me know! You can reach me on [Matrix](https://matrix.to/#/@azharmomin:kde.org) or [Email](mailto:azhar.momin@kdemail.net).
