# Staging Menu Map — v16.60

**Site:** `rom.tjomtek.co.za`  
**Recorded:** 23 November 2026

## Resolved menus

| App | Module | Sidebar | Items |
|---|---|---|---|
| `rgn_lab` | LABS | LABS | Lab Booking, Lab COA, Lab Commodity, Lab Parameter |
| `weighbridge` | Weighbridge | Weighbridge | Dashboard, Weighbridge, Reports, Transporter Fleet List, Settings |
| `rgn_timecards` | RGN Time Cards | RGN Time Cards | RGN Time Employee, Time Cards Settings, Employee Directory Report |
| `rgn_timecards` | Time Cards | Time Cards | Time Card Employee Map, Employee Directory Report, Time Settings |
| `sars_tax_returns` | SARS Tax Returns | SARS Tax Returns | IRP6, IT14SD, Dividends Tax, Customs VAT, Settings |
| `flight_booking` | Flight Booking | Flight Booking | Flight Bookings, Flight Request, Flight Folio And Defect |

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
