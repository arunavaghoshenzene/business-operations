# Handoff: Daily India Operations Meeting transcript → SharePoint

## What the user asked (prompts so far)
1. "I want a cloud based automation that runs even when my laptop is off. The automation should download the transcript after the meeting is done (meeting happens only on weekdays) and upload it to the SharePoint folder `Business Operations/42/FY27/Daily Meeting - India Operations` (site BusinessOperationsHub-BusinessOperations). While uploading rename the transcript word file as per the nomenclature in the screenshot." Screenshots showed the existing files `Daily India Operations Meeting_23Nov.docx`, `_24Nov.docx` and `_25Nov.docx`.
2. "The download button for the transcript works when I login via the ID business.operations@enzene.com."
3. Agreed to rebuilding the Word file from the transcript text in the same layout ("ok go ahead").
4. "can we do in power automate"
5. "I know business operations has access to download. So, can you set up the power automate using your in-browser. I will login to business operations ID in your in-browser window."
6. "connect to z drive business operations folder and run it"
7. "make zip of the prompts done till now. i will move this chat to some folder"

## What was found
- **Meeting:** "Daily India Operations Meeting", weekdays 10:10–11:00 IST. The organizer is Amol Laddha; business.operations@enzene.com and arunava.ghosh@enzene.com are attendees. It is a Teams meeting with Meeting ID 462 903 127 721 1.
- **Teams join URL:** `https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZDY1MGFjNTMtNzQ5NC00NTQ5LWIyODAtMjNhMjlhMWRiMzcw%40thread.v2/0?context=%7b%22Tid%22%3a%221192226a-0d8a-498d-be00-7d83129b2fdb%22%2c%22Oid%22%3a%2258eb6eca-3adb-4407-b8a9-85ff97a2a533%22%7d`
- **SharePoint folder:**
  - driveId `b!x7LTaBfq9kWRGXMPzLB82Gm5kgA5iAVMmFYCmvmidSYB4Y-Izn3MQaRwPQdwMP1Z`
  - folder item id `01KPUZ4E25YR2NNVWQJZEZNXMVP6TJ7YDZ`
  - URL `https://enzene.sharepoint.com/sites/BusinessOperationsHub-BusinessOperations/Shared Documents/Business Operations/42/FY27/Daily Meeting - India Operations`
- **File name pattern:** `Daily India Operations Meeting_<D><Mon>.docx`, for example `_26Nov`. Single-digit days are written without a leading zero (`_1Dec`); this is unconfirmed.
- **Blocker:** with the arunava.ghosh account, the Claude Microsoft 365 connector gets Microsoft Graph error 403 / 3003, "User does not have access to lookup meeting". Microsoft only lets the organizer (or app-only access granted by an application access policy) read transcripts through Graph. The Teams UI download works for business.operations, but it is not certain that Graph will allow that account.
- Graph returns the transcript as text (VTT), not the original .docx, so the Word file is rebuilt in the Teams layout. See `build_docx.py` and `sample.docx`.

## Options
- **A (recommended).** IT registers an app with OnlineMeetingTranscript.Read.All and OnlineMeetings.Read.All (application permissions, admin consent) plus a Teams application access policy covering the organizer, Amol Laddha. The automation then runs in Power Automate (Premium HTTP action) or as a Claude scheduled task.
- **B.** A Power Automate flow owned by business.operations@enzene.com. Test first whether Graph returns the transcript for that account.
- **C.** A flow owned by the organizer (Amol).

## Power Automate flow outline
1. Recurrence: Mon–Fri at 11:45 India Standard Time, with a second run at 13:15.
2. Office 365 Outlook – Get calendar view of events for today; filter on subject "Daily India Operations Meeting"; take the event's Teams join URL.
3. HTTP (Graph): `GET /users/{organizerId}/onlineMeetings?$filter=JoinWebUrl eq '<joinUrl>'` → meeting id.
4. HTTP (Graph): `GET .../onlineMeetings/{id}/transcripts` → pick the transcript created today.
5. HTTP (Graph): `GET .../transcripts/{tid}/content?$format=text/vtt`.
6. Parse the VTT into entries of speaker, timestamp and text.
7. Word Online (Business) – Populate a Microsoft Word template (title, date, duration, repeating section of entries).
8. SharePoint – Check whether the file exists; if not, Create file `Daily India Operations Meeting_<D><Mon>.docx` in the folder above.

## Rules
- Never send any email to anyone outside @enzene.com. The automation sends no email at all.
- Never overwrite an existing file in the folder.

## Files in this bundle
- `TASK_PROMPT.md`: the step-by-step prompt for a Claude scheduled cloud task. It uses the Claude Microsoft 365 connector.
- `build_docx.py`: builds a Teams-layout .docx from transcript entries. It uses only the Python standard library.
- `sample.docx`: a layout sample.
