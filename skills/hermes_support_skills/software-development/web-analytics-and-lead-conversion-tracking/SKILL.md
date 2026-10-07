---
name: web-analytics-and-lead-conversion-tracking
description: "Use when building web analytics, CTA leads, or dashboards."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: software-development
    tags: [analytics, lead-tracking, click-to-chat, whatsapp-leads, executive-dashboard, event-deduplication, telemetry]
    related_skills: [static-site-seo-and-analytics-v4, web-asset-deployment-and-caching, production-environment-operations-v2]
---

# Self-Hosted Web Analytics, CTA Lead Tracking, & Executive Dashboard Operations

A class-level operational guide for engineering, deploying, and maintaining self-hosted web analytics engines, client-side click-to-chat conversion trackers, server-side event de-duplication, and executive command center dashboards.

## When to Use

- When deploying lightweight, self-hosted web analytics (Unique Visitors, Pageviews, Average Read Duration, Bounce Rate, Real-Time Active Users) on shared hosting or VPS environments without third-party tracking bloat (Google Analytics).
- When implementing outbound lead capture for WhatsApp, telephone, or email Call-to-Action (CTA) buttons via asynchronous beacons (`/api/track-lead.php`).
- When diagnosing duplicate event logs or artificial conversion spikes where single button clicks generate 2–4 identical rows in the database.
- When structuring executive analytics dashboards (Clean Light Theme) to optimize executive readability and data hierarchy.
- When analyzing visitor clickstream behavior to differentiate between single-device repeat clicks and multi-user traffic.

## Procedure

1. **Client-Side Telemetry & Event Listener Hygiene:**
   - **Isolate Analytics from UI Logic:** Never bundle tracking event listeners into general UI scripts (`main.js`). Maintain tracking logic strictly inside a dedicated standalone script (`/js/analytics.js`).
   - **Unified Event Delegation:** Attach a single global `click` listener on `document` targeting outbound anchors (`wa.me`, `tel:`, `mailto:`):
     ```javascript
     document.addEventListener('click', function(e) {
         const link = e.target.closest('a');
         if (!link) return;
         const href = link.getAttribute('href') || '';
         if (href.includes('wa.me') || href.includes('whatsapp.com')) {
             const payload = {
                 button_name: link.innerText.trim() || 'WhatsApp CTA',
                 button_location: link.classList.contains('floating-wa') ? 'Floating Button' : 'In-Page CTA',
                 page_url: window.location.href,
                 page_title: document.title,
                 target_url: href
             };
             if (navigator.sendBeacon) {
                 navigator.sendBeacon('/api/track-lead.php', new Blob([JSON.stringify(payload)], { type: 'application/json' }));
             } else if (window.fetch) {
                 fetch('/api/track-lead.php', { method: 'POST', body: JSON.stringify(payload), keepalive: true });
             }
         }
     });
     ```
   - **Avoid Script Concatenation Duplication:** During iterative deployments, ensure historical tracking snippets are not repeatedly appended to `main.js`. Bundling multiple event listeners causes each tap to fire simultaneous requests in the same millisecond.

2. **Server-Side Smart De-duplication (Debounce Filter):**
   - In `/api/track-lead.php`, implement a 2-second timestamp & IP debounce before appending records to storage:
     ```php
     $ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
     if (!empty($_SERVER['HTTP_CF_CONNECTING_IP'])) {
         $ip = $_SERVER['HTTP_CF_CONNECTING_IP'];
     } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
         $ip_list = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
         $ip = trim($ip_list[0]);
     }

     $now = time();
     $now_str = date('Y-m-d H:i:s', $now);

     // Check last logged line for identical IP within 2 seconds
     $is_duplicate = false;
     if (file_exists($log_file)) {
         $fp = fopen($log_file, 'r');
         if ($fp) {
             fseek($fp, max(0, filesize($log_file) - 1024));
             $tail = fread($fp, 1024);
             fclose($fp);
             $lines = array_filter(explode("\n", trim($tail)));
             if (!empty($lines)) {
                 $last_record = json_decode(end($lines), true);
                 if ($last_record && isset($last_record['ip'], $last_record['timestamp'])) {
                     $last_time = strtotime($last_record['timestamp']);
                     if ($last_record['ip'] === $ip && ($now - $last_time) < 2) {
                         $is_duplicate = true;
                     }
                 }
             }
         }
     }

     if ($is_duplicate) {
         echo json_encode(['status' => 'ignored_duplicate']);
         exit;
     }
     ```

3. **Executive Dashboard Section Layout Hierarchy:**
   Structure executive dashboards following a top-to-bottom macro-to-micro hierarchy:
   1. **Header & Real-Time Presence:** Brand name, domain, local timezone clock (WIB / UTC+7), and live online visitor badge.
   2. **Top Row (High-Level KPIs):** 6 core metrics (Unique Visitors, Total Pageviews, Avg Duration, Bounce Rate, Total WhatsApp Leads, Conversion Rate).
   3. **Second Row (Executive Insights & Trends):** Plain-language business summary box paired with 7-day Traffic Trend & Device Breakdown visual charts.
   4. **Third Row (2-Column Comparative Performance):**
      - Left column: *Top Visited Pages & Average Read Duration*.
      - Right column: *Recent Live Visitor Sessions (Real-Time Flow)*.
   5. **Bottom Row (Granular Event Feed):** Full-width *Outbound WhatsApp Leads Tracker* table displaying chronological click records, source URLs, CTA locations, and devices.

4. **Forensic Clickstream & Device Analysis:**
   - When diagnosing user interaction patterns in lead logs:
     - Compare IP addresses, User-Agents, and page URLs across adjacent timestamps.
     - **Multi-Log at Identical Second:** Indicates multiple unbundled client-side event listeners firing concurrently on a single physical tap.
     - **Logs Separated by 5–30 Seconds from Same IP:** Indicates a genuine user behavior where the visitor clicked the CTA, opened WhatsApp Web/App, returned to the browser tab, and clicked the button again.

## Pitfalls

- **Inverted Dashboard Data Hierarchy:** Placing voluminous tabular event logs (e.g. 50+ row raw click logs) above high-level KPIs and pageview duration tables forces executives to scroll past raw data before seeing key business metrics. Always position macro-level summaries and 2-column comparative cards above detailed tabular feeds.
- **Client-Side Event Listener Duplication:** Leaving duplicate `click` listeners across bundled scripts (`main.js` + `analytics.js`) causes a single tap to record 2–4 duplicate rows in the database at the exact same millisecond.
- **Missing Server-Side Timestamp Debounce:** Failing to implement an IP/timestamp debounce in tracking endpoints records artificial conversion spikes from user double-taps or rapid button hammering.
- **Timezone Mismatch in Operational Logs:** Storing or displaying timestamps in UTC on dashboards intended for Indonesian business owners creates confusion; always convert server timestamps to `Asia/Jakarta` (`WIB` / UTC+7) and explicitly label table columns `(WIB)`.
