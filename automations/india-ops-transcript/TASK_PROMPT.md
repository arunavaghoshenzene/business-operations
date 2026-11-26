# Daily India Operations Meeting – transcript to SharePoint

Scheduled cloud task prompt. Schedule: Mon–Fri 11:47 IST (main run) and 13:13 IST (catch-up run).
Connector needed: Microsoft 365, signed in as an account that can read this meeting's transcript.

---

You are archiving today's Teams transcript for the "Daily India Operations Meeting" to SharePoint. Work only with the Microsoft 365 connector tools. Never send any email.

1. **Today's date (IST).** Determine today's date in Asia/Kolkata. If it is Saturday or Sunday, stop.

2. **Target name.** `Daily India Operations Meeting_<D><Mon>.docx`, where `<D>` is the day of month without leading zero and `<Mon>` is the 3-letter English month (e.g. `Daily India Operations Meeting_26Nov.docx`, `Daily India Operations Meeting_1Dec.docx`).

3. **Already done?** Read the folder `file:///b!x7LTaBfq9kWRGXMPzLB82Gm5kgA5iAVMmFYCmvmidSYB4Y-Izn3MQaRwPQdwMP1Z/01KPUZ4E25YR2NNVWQJZEZNXMVP6TJ7YDZ` with `read_resource`. If a file with the target name exists, stop: nothing to do.

4. **Find the meeting.** `outlook_calendar_search` with query `Daily India Operations Meeting`, from today 00:00 to tomorrow 00:00 IST. If there is no event or it is cancelled, stop. Read the event with `read_resource` and take its `meetingTranscriptUrl` verbatim.

5. **Get the transcript.** `read_resource` on that `meetingTranscriptUrl` (page through all pages if paginated). If there is no transcript yet, stop quietly; the catch-up run will retry. If access is denied, stop and report the error.

6. **Build the Word file.** Write the script below to `build_docx.py`. Write `input.json` with:
   - `title`: `Daily India Operations Meeting - <YYYYMMDD>_<HHMMSS> - Meeting Transcript` using the transcript's start time in IST (fall back to the meeting's actual start time).
   - `date`: transcript start in UTC formatted like `November 26, 2026, 4:40AM`.
   - `duration`: like `42m 8s` (from the transcript metadata, or the last entry's offset).
   - `started_by`: the person who started transcription, if known, else null.
   - `entries`: every utterance in order, `{"speaker": name, "ts": "M:SS" or "H:MM:SS" offset from transcript start, "text": spoken text}`. Merge consecutive lines from the same speaker into one entry. Keep the wording exactly as transcribed.

   Run `python3 build_docx.py input.json out.docx`, then `base64 -w0 out.docx > out.b64` and note the byte size of `out.docx`.

7. **Upload.** `sharepoint_upload_file` with driveId `b!x7LTaBfq9kWRGXMPzLB82Gm5kgA5iAVMmFYCmvmidSYB4Y-Izn3MQaRwPQdwMP1Z`, parentItemId `01KPUZ4E25YR2NNVWQJZEZNXMVP6TJ7YDZ`, filename = target name, `contentBase64` = contents of `out.b64` exactly, `expectedBytes` = byte size of out.docx, conflictBehavior `fail`. If the upload is rejected for a bad base64, regenerate and retry once.

8. **Report** one line: uploaded file name and webUrl, or why it stopped.

```python
<contents of build_docx.py>
```
