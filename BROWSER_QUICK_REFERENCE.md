# 🚀 Browser Actions Quick Reference

## All Available Browser Actions

| Action | Purpose | Example | Usage |
|--------|---------|---------|-------|
| `browser_search` | Search web | `"Python tutorials"` | Find info online |
| `browser_visit` | Visit URL | URL + task | See page elements |
| `browser_analyze` | Analyze page | Just URL | Map structure |
| `browser_click` | Click element | Button text | Interact with page |
| `browser_fill_form` | Submit form | Field data | Complete forms |
| `browser_extract` | Get info | URL + topic | Gather data |

---

## Action Details & Examples

### browser_search
**What it does:** Search Google
```json
{
  "action": "browser_search",
  "value": "best python books"
}
```

### browser_visit
**What it does:** Visit page, show buttons/links/content
```json
{
  "action": "browser_visit",
  "value": {
    "url": "https://example.com",
    "task": "show what's available"
  }
}
```

### browser_analyze
**What it does:** Deep analysis of page structure
```json
{
  "action": "browser_analyze",
  "value": "https://example.com"
}
```

**Returns:**
- All buttons with IDs
- All links with URLs
- All forms with fields
- Page features
- Content preview

### browser_click
**What it does:** Click a button or link
```json
{
  "action": "browser_click",
  "value": {
    "url": "https://example.com",
    "selector": "Sign Up"
  }
}
```

### browser_fill_form
**What it does:** Fill and submit a form
```json
{
  "action": "browser_fill_form",
  "value": {
    "url": "https://example.com/contact",
    "data": "{\"email\": \"you@example.com\", \"name\": \"Your Name\", \"message\": \"Hello\"}"
  }
}
```

### browser_extract
**What it does:** Extract specific information
```json
{
  "action": "browser_extract",
  "value": {
    "url": "https://example.com/pricing",
    "info": "all pricing options"
  }
}
```

---

## Common Patterns

### Pattern 1: Find Info
```
browser_visit → Find link → browser_click → browser_extract
```

### Pattern 2: Sign Up
```
browser_analyze → browser_click (Sign Up) → browser_fill_form
```

### Pattern 3: Search & Collect
```
browser_search → browser_visit → browser_click (results) → browser_extract
```

### Pattern 4: Navigate Deep
```
browser_visit → browser_click → browser_click → browser_extract
```

---

## Response Format

All browser actions return:
- ✅ Content/info extracted
- ✅ Links available
- ✅ Elements found
- ✅ Status messages

---

## Usage Tips

1️⃣ **Start with browser_analyze** - Understand page first
2️⃣ **Use browser_visit** - See clickable elements
3️⃣ **Click with browser_click** - Get to what you need
4️⃣ **Extract with browser_extract** - Get final data

---

## Real Examples

### "Find GitHub's pricing"
```
1. browser_visit github.com
2. browser_click "Pricing" link
3. browser_extract pricing info
```

### "Sign up for newsletter"
```
1. browser_visit example.com
2. browser_click "Subscribe" button
3. browser_fill_form {email: "you@example.com"}
```

### "Get store hours"
```
1. browser_search "store hours"
2. browser_visit store website
3. browser_extract "hours of operation"
```

### "Check product availability"
```
1. browser_visit amazon.com
2. browser_click "Search"
3. browser_fill_form {q: "product name"}
4. browser_click "product"
5. browser_extract "availability"
```

---

## What Each Action Returns

### browser_search
```
Search results for 'query':
- Result 1
- Result 2
- Result 3
```

### browser_visit
```
Page: Title
URL: https://...

=== BUTTONS ===
[0] Button Text

=== LINKS ===
[0] Link Text

=== PAGE CONTENT ===
[Text preview...]
```

### browser_analyze
```
=== CLICKABLE BUTTONS ===
[BTN 0] Sign Up
[BTN 1] Log In

=== FORMS ===
Form 0:
  - email (text)
  - password (password)

=== FEATURES ===
Has Search: true
Has Login: false
```

### browser_click
```
Clicked element. 
Page content after click:
[Updated page content...]
```

### browser_fill_form
```
Form submitted.
Result page:
[Confirmation or result...]
```

### browser_extract
```
=== PAGE INFORMATION ===
Title: ...
Description: ...

=== HEADINGS ===
- Heading 1
- Heading 2

=== CONTENT ===
[Extracted info...]
```

---

## Error Handling

If something doesn't work:
1. Try `browser_analyze` first
2. Use exact button/link text
3. Check URL is correct
4. Try different selectors
5. Break into smaller steps

---

## Performance Notes

| Operation | Time |
|-----------|------|
| Search | 2-3 sec |
| Visit | 2-3 sec |
| Analyze | 2-4 sec |
| Click | 1-2 sec |
| Form Submit | 2-3 sec |
| Extract | 2-3 sec |

---

## Integration

✅ Works with:
- Desktop automation
- File operations
- System commands
- Python execution
- Screenshots/analysis

---

## Quick Start

```bash
# 1. Start agent
python app.py

# 2. Choose "agent" profile

# 3. Try:
"Search for Python tutorials"

# 4. Or:
"Visit example.com and find the pricing"

# 5. Or:
"Sign me up for beta.example.com"
```

---

## Cheat Sheet

**See what's on page:**
`browser_visit` or `browser_analyze`

**Click something:**
`browser_click`

**Fill & submit form:**
`browser_fill_form`

**Get specific info:**
`browser_extract`

**Search web:**
`browser_search`

---

## Documentation

- `ADVANCED_BROWSER_COMPLETE.md` - Full guide
- `BROWSER_INTERACTION_ADVANCED.md` - Advanced patterns
- `BROWSER_USAGE.md` - Basic usage
- `IMPLEMENTATION_COMPLETE.md` - Technical details

---

## Examples by Goal

| Goal | Actions |
|------|---------|
| Find contact info | visit → click → extract |
| Sign up | analyze → click → fill_form |
| Compare prices | visit → click → analyze → extract |
| Get news | search → visit → extract |
| Check status | visit → analyze → click |

---

**Your AI is ready to browse!** 🌐🚀

Use these actions to complete any web task!
