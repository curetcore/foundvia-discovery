# Performance evidence

Record URL, device class, network/profile settings, date, data source, and whether the result is field or laboratory data. Google's good Core Web Vitals thresholds are LCP ≤2.5s, INP ≤200ms, and CLS ≤0.1 at the 75th percentile, evaluated separately for mobile and desktop. A single Lighthouse run does not establish that field result.

Trace the actual bottleneck before changing code:

| Symptom | Evidence to inspect | Possible intervention | Verify |
|---|---|---|---|
| Slow LCP | Element, request start, server latency, image transfer | Reduce the measured delay; avoid lazy-loading the actual LCP image | Same controlled profile plus subsequent field data |
| Slow interaction | Main-thread trace and event handler work | Reduce synchronous work; split tasks or use a worker where suitable | Profile the same interaction |
| Layout movement | Shift sources and reserved dimensions | Reserve image/embed space and stabilize dynamic regions | Repeat the affected flow |

React transitions do not make arbitrary synchronous CPU work run off the main thread. Check the installed Next.js version before choosing image loading/preload APIs. Do not preload every image or disable useful scripts solely to raise a score.

Source: [Web Vitals](https://web.dev/articles/vitals).
