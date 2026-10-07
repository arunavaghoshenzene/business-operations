# Sends the People & Learning deck to Soumya Guria via the Outlook desktop app (Outlook must be open).
# Put this script in the same folder as the .pptx (e.g. Downloads), then: right-click > Run with PowerShell.
$deck = Join-Path $PSScriptRoot "People_and_Learning_Overview_Audit_Sep2026_with_photos.pptx"
if (-not (Test-Path $deck)) { $deck = "$env:USERPROFILE\Downloads\People_and_Learning_Overview_Audit_Sep2026_with_photos.pptx" }
if (-not (Test-Path $deck)) { Write-Host "Deck not found: $deck"; Read-Host "Press Enter to exit"; exit 1 }

$outlook = New-Object -ComObject Outlook.Application
$mail = $outlook.CreateItem(0)
$mail.To = "soumya.guria@enzene.com"
$mail.Subject = "People & Learning Overview - Audit Deck (Sep 2026) with event photos"
$mail.Body = @"
Hi Soumya,

Please find attached the updated People & Learning overview deck for the audit team (Sep 2026). It now includes photo slides from Dandiya Night 2025, Potluck & Reflections 2025 and the Annual Awards Night 2026.

Regards,
Arunava
"@
$mail.Attachments.Add($deck) | Out-Null
$mail.Send()
Write-Host "Email sent to Soumya Guria."
Read-Host "Press Enter to close"
