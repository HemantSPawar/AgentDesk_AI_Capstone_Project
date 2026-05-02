# Chapter 11 - Product-Ready Polish

## What This Chapter Teaches

How to improve runtime reliability with response schema validation and safer fallbacks.

Prerequisite: complete one-time setup in `chapter_02_project_setup`.

## Which Files To Open

- `agentdesk_ai/schema.py`
- `agentdesk_ai/agent.py`
- `app.py`

## What Command To Run

```bash
python app.py
```

## What Student Should Observe

- Stable JSON structure.
- Cleaner fallback behavior when model output is malformed.

## Common Mistakes

- Skipping schema validation and trusting raw model text.
- Returning non-JSON response on errors.

## Connection To Next Chapter

Next chapter packages the capstone into a portfolio-ready teaching artifact.
