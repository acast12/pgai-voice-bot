# Bug Report

## Bug 1 — Doctor name transcription inconsistency
**Severity:** Low (transcription artifact, not agent bug)
**Note:** Twilio STT struggles with uncommon proper nouns. 
The agent likely pronounces the name correctly but Twilio 
transcribes it differently each time. Would need Deepgram 
or similar for better proper noun handling.