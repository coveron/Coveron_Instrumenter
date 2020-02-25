---
title: Codeconut Instrumentation Data (CID) - Specification
permalink: /docs/cid_format/
---

## Introduction

The Codeconut Instrumentation Data Format provides the information necessary to link the runtime output to the according source code file.

The file consists of a gzip-compressed JSON object, whose structure and content details are explained in a later section.

The link between source code and runtime metrics is established by providing a dictionary that links every unique marker's ID integrated into the final source code with 1 or more elements (statements, decisions and conditions) in the uninstrumented source code and specifies the type of the marker (more info found in the documentation for the [Codeconut Runtime Information specification]({{site.baseurl}}{% link _docs/cri_format.md %})).
