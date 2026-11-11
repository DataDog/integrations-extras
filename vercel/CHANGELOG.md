# CHANGELOG - Vercel

## 1.1.0 / 2026-11-11

***Changed***:

* The logs pipeline now prepares Vercel Function errors for Error Tracking: logs with a Node.js stack trace, `console.error` output, or a Function crash get `error.kind`, `error.message`, and (when available) `error.stack`, plus the `error` status. The log status changes even when the request returned a non-5xx status code, so `status:error` searches, monitors, and dashboards include these invocations. `vercel.functions.errors`, which counts invocation summary logs with the `error` status, now also counts invocations that returned a non-5xx response but logged a stack trace.

* https://vercel.com/changelog