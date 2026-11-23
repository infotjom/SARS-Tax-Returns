# Staging Menu Map — v16.60

**Site:** `rom.tjomtek.co.za`  
**Recorded:** 23 November 2026

## Resolved menus — after custom-app cleanup

| App | Module | Sidebar | Items |
|---|---|---|---|
| `rgn_lab` | LABS | LABS | 4: Lab Booking, Lab COA, Lab Commodity, Lab Parameter |
| `weighbridge` | Weighbridge | Weighbridge | 5: Dashboard, Weighbridge, Reports, Transporter Fleet List, Settings |
| `rgn_timecards` | Time Cards | Time Cards | 6: Time Card Employee Map, Employee Directory, Time Settings, RGN Time Employee, Time Cards Settings, Employee Directory Report |
| `flight_booking` | Flight Booking | Flight Booking | 3: Flight Bookings, Flight Request, Flight Folio And Defect |
| `sars_tax_returns` | SARS Tax Returns | SARS Tax Returns | 5: IRP6, IT14SD, Dividends Tax, Customs VAT, Settings |

The duplicate **RGN Time Cards** module no longer resolves; its items are consolidated into **Time Cards**.

Verified with `frappe.desk.doctype.sidebar.sidebar.get_sidebar(module)`.

## What was repaired

- Set the correct **app** on custom Sidebars:
  - LABS → `rgn_lab`
  - Time Cards / RGN Time Cards → `rgn_timecards`
  - WeighBridge → `weighbridge`
  - Wiki → `wiki`
  - Raven → `raven`
- Created the missing **Flight Booking Workspace** and **Flight Booking Sidebar**.
- Created **Custom Sidebar** overrides for:
  - Weighbridge
  - SARS Tax Returns
  - Flight Booking
- Fixed Desktop Icon app mappings and removed the stale `SA VAT Returns` icon.
- Set custom Workspaces to `public` so all desk users can see them.

## v16.60 navigation note

Frappe v16.60 uses the new `Sidebar` model. The old `Workspace Sidebar` records are **archived by Frappe** and can no longer be edited or newly created. Existing old-desk Workspaces and routes remain available; new apps are wired through `Sidebar` + `Custom Sidebar`.

## Checks

- Login: `200`
- Ping: `200`
- Public site: `200`
- All six menus resolve to the expected item counts.
- No SARS test transactions were created.

## Duplicate LABS cleanup — 23 November 2026

Cause: the v16.60 upgrade retained the archived `Workspace Sidebar` **LABS** alongside the new `Sidebar` **LABS**. Both were visible.

Fixed:

- Deleted the legacy `Workspace Sidebar` **LABS**.
- Kept the v16.60 `Sidebar` **LABS** (`rgn_lab`).
- Set `Workspace` **LABS** module to `LABS` so it no longer creates a second module entry.
- Hid the legacy `Desktop Icon` **LABS** because its `Workspace Sidebar` target no longer exists. The workspace route `/app/labs` remains.
- Other custom apps may still have legacy Workspace Sidebar rows; clean them the same way if they show duplicate desk entries.


## Custom legacy cleanup — 23 November 2026

Applied to custom apps only (`rgn_lab`, `weighbridge`, `rgn_timecards`, `flight_booking`):

- Removed legacy `Workspace Sidebar` rows: **WeighBridge**, **Time Cards**, **RGN Time Cards**.
- Removed duplicate new-UI `Sidebar` rows: **WeighBridge (Custom)**, **RGN Time Cards**.
- Kept one canonical `Sidebar` per module:
  - LABS
  - Weighbridge
  - Time Cards (six items, including RGN Time Employee)
  - Flight Booking
- Aligned Workspaces to the same module names:
  - LABS → LABS
  - WeighBridge → Weighbridge
  - Time Cards → Time Cards
  - Flight Booking → Flight Booking
- Hid the legacy Desktop Icons for LABS, WeighBridge and Time Cards; the new UI uses `Sidebar`, not the archived launcher.
- Old `Workspace` routes remain available at `/app/<workspace>`.
- Verified `get_sidebar()` after cleanup:
  - LABS: 4
  - Weighbridge: 5
  - Time Cards: 6
  - Flight Booking: 3
  - SARS Tax Returns: 5
  - RGN Time Cards: not present
- Login and ping remain **200**.
