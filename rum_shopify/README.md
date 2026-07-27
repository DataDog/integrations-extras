# Shopify Integration

## Overview

Instrument your Shopify store with Datadog Real User Monitoring using the Datadog RUM Shopify bundle. One bundle covers both surfaces of a Shopify store:

- **Storefront pages** (`/`, `/products/*`, `/collections/*`, etc.) — added via a Theme Liquid snippet. Full RUM feature set: views, resources, long tasks, user interactions, errors, and Session Replay.
- **Checkout pages** (`/checkouts/*`, `/checkout`) — added via a Custom Pixel. Shopify deprecated `checkout.liquid` in August 2024, so checkout pages cannot be reached by theme edits at all; a [Web Pixel][5] running in a sandboxed iframe is the only mechanism that can observe them.

Use both deployment paths together for full-funnel coverage.

## Setup

### Prerequisites

Before you begin, gather the following Datadog RUM values:

- A Datadog RUM Application ID
- A Datadog RUM Client Token
- A Datadog site, such as `datadoghq.com`

You can get those values in Datadog under **Digital Experience > Real User Monitoring > Manage Applications > Set Up Manually**.

You'll also need:

- Admin access to your Shopify store (**Settings** and **Online Store > Themes**).
- For the Custom Pixel path: access to **Settings > Customer events** in Shopify Admin.

### Installation and Configuration

#### Theme Liquid Setup

Use this path to cover storefront pages (product, collection, cart, home).

##### Steps

1. In Shopify Admin, go to **Online Store > Themes**.
2. On your live theme, click the **⋮** menu, then **Edit code**.
3. Open `layout/theme.liquid`.
4. Paste the following snippet right before the closing `</head>` tag, replacing the placeholder values with your Datadog RUM configuration:

   ```html
   <script>
     (function (h, o, u, n, d) {
       h = h[d] = h[d] || { q: [], onReady: function (c) { h.q.push(c) } }
       d = o.createElement(u); d.async = 1; d.src = n
       d.crossOrigin = 'anonymous'
       n = o.getElementsByTagName(u)[0]; n.parentNode.insertBefore(d, n)
     })(
       window,
       document,
       'script',
       'https://www.datadoghq-browser-agent.com/{{< region-param key="dd_datacenter_lowercase" code="true" >}}/v7/datadog-rum-shopify.js',
       'DD_RUM'
     );

     DD_RUM.onReady(function () {
       DD_RUM.init({
         applicationId: '<YOUR_DATADOG_APPLICATION_ID>',
         clientToken: '<YOUR_DATADOG_CLIENT_TOKEN>',
         site: '{{< region-param key="dd_site" code="true" >}}',
         service: '<YOUR_SERVICE_NAME>',
         env: '<YOUR_ENV_NAME>',
         version: '1.0.0',
         sessionSampleRate: 100,
         sessionReplaySampleRate: 100,
         trackUserInteractions: true,
         trackResources: true,
         trackLongTasks: true,
         defaultPrivacyLevel: 'mask-user-input',
       })
       DD_RUM.startSessionReplayRecording()
     })
   </script>
   ```

5. Save the file.

##### Out-of-the-box functionality

`DD_RUM.init()` here behaves exactly like the regular [`@datadog/browser-rum`][6] package. You get:

- Automatic view tracking as visitors navigate storefront pages.
- Web Vitals, resource timing, long tasks, and automatic click tracking.
- Session Replay recording.
- Runtime error tracking (`window.onerror`, `unhandledrejection`).

##### Limitations

- **No checkout coverage.** Checkout, Thank You / Order Status, and Customer Account pages are fully controlled by Shopify and cannot be reached by any Liquid edit. Use the [Custom Pixel Setup](#custom-pixel-setup) below for that funnel.
- Theme code changes require re-editing `theme.liquid` on every theme update or theme switch — there's no install-once mechanism on this path.

#### Custom Pixel Setup

Use this path to cover checkout pages (`/checkouts/*`, `/checkout`). It runs inside a Shopify **Custom Pixel**, a sandboxed `<iframe sandbox="allow-scripts allow-forms">` that Shopify injects to observe checkout events — the only place JavaScript can run on checkout pages at all.

##### Steps

1. In Shopify Admin, go to **Settings > Customer events**.
2. Click **Add custom pixel**, give it a name, and open its code editor.
3. Paste the following snippet, replacing the placeholder values with your Datadog RUM configuration:

   ```javascript
   (function (h, o, u, n, d) {
     h = h[d] = h[d] || { q: [], onReady: function (c) { h.q.push(c) } }
     d = o.createElement(u); d.src = n
     d.crossOrigin = 'anonymous'
     n = o.getElementsByTagName(u)[0]; n.parentNode.insertBefore(d, n)
   })(
     window,
     document,
     'script',
     'https://www.datadoghq-browser-agent.com/{{< region-param key="dd_datacenter_lowercase" code="true" >}}/v7/datadog-rum-shopify.js',
     'DD_RUM'
   )

   DD_RUM.onReady(function () {
     DD_RUM.init({
       applicationId: '<YOUR_DATADOG_APPLICATION_ID>',
       clientToken: '<YOUR_DATADOG_CLIENT_TOKEN>',
       site: '{{< region-param key="dd_site" code="true" >}}',
       service: '<YOUR_SERVICE_NAME>',
       env: '<YOUR_ENV_NAME>',
       version: '1.0.0',
       sessionSampleRate: 100,
       shopifyAnalytics: analytics, // the Custom Pixel's `analytics` global — see note below
     })
   })
   ```

4. Save the pixel, then set its required consent category under **Settings** for the pixel (e.g. Analytics) to match your store's privacy configuration — the bundle does not add its own consent gate; it defers entirely to whatever the merchant declares in Shopify's Pixel Manager.

**Note on `shopifyAnalytics`:** `analytics` is a bare global that only exists inside a Custom Pixel's code editor scope — pass it straight through as shown.

##### Out-of-the-box functionality

Once `shopifyAnalytics` is set, the bundle automatically:

- Starts a RUM view on each checkout step (bound to Shopify's `page_viewed` standard event).
- Converts Shopify's `clicked` DOM event into a RUM click action, with correct position data.
- Converts Shopify's `ui_extension_errored` event (a checkout UI extension crashing) into a RUM error, tagged with the failing extension's name, target, and type.
- Continues the storefront session: the sandbox shares the top frame's cookie jar, so if a visitor already has a `_dd_s` session cookie from the Theme Liquid snippet, checkout events land in that same session.
- Is a no-op in effect on storefront pages: Shopify fires the pixel's `page_viewed` event on every page, not just checkout, but the bundle only calls `startView` for checkout-path URLs — so no duplicate session or duplicate view is created alongside the Theme Liquid instance.

##### Instrumenting extra Shopify events

The snippet above only wires up the three events the bundle binds automatically. Shopify's [standard events][7] cover the full checkout funnel — `checkout_started`, `checkout_contact_info_submitted`, `checkout_shipping_info_submitted`, `payment_info_submitted`, `checkout_completed`, `alert_displayed` and more. Subscribe to any of them yourself, using `DD_RUM.onReady()` to queue calls made before the SDK has finished loading:

```javascript
analytics.subscribe('checkout_completed', (event) => {
  const checkout = event.data.checkout
  DD_RUM.onReady(() =>
    DD_RUM.addAction('checkout_completed', {
      orderId: checkout?.order?.id,
      totalPrice: checkout?.totalPrice,
    })
  )
})

analytics.subscribe('checkout_contact_info_submitted', (event) => {
  const checkout = event.data.checkout
  DD_RUM.onReady(() => {
    if (checkout?.email) {
      DD_RUM.setUser({ email: checkout.email }) // capture the guest email here
    }
    DD_RUM.addAction('checkout_contact_info_submitted', { checkoutToken: checkout?.token })
  })
})
```

You can also emit and subscribe to [custom events][8] the same way.

##### Limitations

- **No Session Replay or Profiling.** The sandbox iframe has no real checkout DOM — recording or profiling it would capture nothing meaningful. Both are force-disabled regardless of what you pass to `init()`.
- **No Web Vitals, resource timing, or runtime JS errors.** `PerformanceObserver`, `fetch`/`XMLHttpRequest` instrumentation, and `window.onerror`/`unhandledrejection` all observe the sandbox iframe itself, not the checkout page's main thread — that boundary can't be crossed from a Custom Pixel.
- **Click actions are partial.** Only Shopify's basic `clicked` DOM event is available (no automatic DOM click listener, since there's no real DOM to listen on):
  - Emitted for inputs, links, and buttons — not for empty space or plain text.
  - Not emitted for payment card fields (card number, expiration, CVC, name on card) or the "Sign in" link.
  - Not emitted for a second click on a field that's already focused.
- **Advanced DOM Events are unavailable.** Shopify restricts that API to apps approved for it in the Partner Dashboard — a bar that doesn't apply to (and can't be met by) a Custom Pixel.
- **Checkout-path detection is regex-based**, matching `/checkouts?/` with an optional two-letter locale prefix (e.g. `/en/checkout`). A store with a non-standard checkout URL structure won't currently have an override flag to adjust it.

### Validate the Installation

#### Storefront (Theme Liquid)

1. Open your storefront in a new browser session with developer tools open.
2. Confirm `datadog-rum-shopify.js` loads successfully (Network tab) and `window.DD_RUM` is defined (Console tab).
3. Navigate between a few storefront pages (home, a product, the cart).
4. In Datadog, open **Digital Experience > RUM Explorer**, filter by your configured `service` and `env`.
5. Confirm view events appear for each page you visited, and that a Session Replay recording is available for the session.

#### Checkout (Custom Pixel)

1. Place a test order (or go far enough into checkout to trigger `checkout_started`) on a storefront that has the Custom Pixel configured.
2. In the RUM Explorer, filter by the same `service`/`env` and look for views whose URL is under `/checkouts/`.
3. Confirm the view URL matches the real checkout URL (not a sandbox/iframe address) — this validates the `page_viewed`-driven `startView` binding is working.
4. Click a few checkout fields/buttons during the test run, then confirm corresponding click actions appear on the view.
5. If you added extra event subscriptions (see [Instrumenting extra Shopify events](#instrumenting-extra-shopify-events)), confirm their custom actions or user attributes (e.g. `checkout_completed`, the identified email from `setUser`) show up on the same view/session.
6. If nothing appears: check the pixel's consent category under **Settings > Customer events** — in opt-in (GDPR-style) regions, Shopify won't load the sandbox at all until the visitor consents, so no events fire until then.

## Troubleshooting

Need help? Contact [Datadog Support][3].

[1]: https://shopify.dev/docs/api/web-pixels-api
[2]: https://docs.datadoghq.com/help/
[3]: https://docs.datadoghq.com/help/
[4]: https://docs.datadoghq.com/getting_started/site/#access-the-datadog-site
[5]: https://shopify.dev/docs/api/web-pixels-api
[6]: https://github.com/DataDog/browser-sdk/blob/main/packages/rum/README.md
[7]: https://shopify.dev/docs/api/web-pixels-api/standard-events
[8]: https://shopify.dev/docs/api/web-pixels-api/emitting-data
