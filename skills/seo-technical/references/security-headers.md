# Security headers are security controls

Do not label missing HSTS, CSP, or Permissions-Policy as proven search-ranking failures. Review them as security concerns within the user's scope.

HSTS requires a working HTTPS policy across the intended host/subdomains; understand its persistence before enabling it. Design CSP around actual resource and script needs, including nonces/hashes where appropriate. Do not copy a restrictive header list that breaks the app or an overly broad policy that creates false assurance.

Confirm headers at the actual response layer: CDN, reverse proxy, framework, and route overrides may differ. Start with a reviewed candidate and inspect important flows after changes. Treat deployment and live verification separately.

Sources: [MDN HSTS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security), [MDN CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP).
