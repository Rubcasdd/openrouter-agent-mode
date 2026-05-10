# Advanced Browser Interaction Guide

## Overview

Your AI agent can now fully interact with web pages - opening links, clicking buttons, analyzing page structure, filling forms, and extracting information. **No display required!**

## Complete Browser Action Set

### 1. **browser_search** - Search the Web
Search Google and get results instantly.

```json
{
  "action": "browser_search",
  "value": "Python programming tips"
}
```

**Response:**
```
Search results for 'Python programming tips':
- Python Tips and Tricks
- Python Best Practices
- Advanced Python Techniques
...
```

---

### 2. **browser_visit** - Visit URL & See Elements
Visit a page and get all clickable elements, buttons, and links.

```json
{
  "action": "browser_visit",
  "value": {
    "url": "https://example.com",
    "task": "Find product information"
  }
}
```

**Response:**
```
Page: Example.com
URL: https://example.com

=== BUTTONS ===
[0] Sign Up
[1] Learn More
[2] Contact Us

=== LINKS ===
[0] About Us
[1] Documentation
[2] Pricing

=== HEADINGS ===
- Welcome to Example
- Our Services
- Get Started

=== PAGE CONTENT ===
[page text...]

Use 'browser_click' action to click buttons/links by their ID number.
```

---

### 3. **browser_analyze** - Deep Page Analysis
Analyze page structure to find all interactive elements before interacting.

```json
{
  "action": "browser_analyze",
  "value": "https://example.com"
}
```

**Response:**
```
=== PAGE ANALYSIS ===
Title: Example.com
URL: https://example.com
Total Elements: 243

=== CLICKABLE BUTTONS ===
[BTN 0] Sign Up
[BTN 1] Submit
[BTN 2] More Info

=== LINKS ===
[LINK 0] Home
[LINK 1] Products
[LINK 2] Contact

=== FORMS & INPUT FIELDS ===
Form 0:
  - email (text):
  - password (password): Username
  - subscribe (checkbox): Subscribe to newsletter

=== PAGE FEATURES ===
Has Search: true
Has Login: false

=== CONTENT ===
[page content...]

=== HOW TO INTERACT ===
Use actions:
- 'browser_click' to click buttons/links by their ID
- 'browser_fill_form' to fill and submit forms
- 'browser_visit' to navigate to a link
```

---

### 4. **browser_click** - Click Buttons & Links
Click on buttons, links, or any clickable element by selector.

```json
{
  "action": "browser_click",
  "value": {
    "url": "https://example.com",
    "selector": "button:contains('Sign Up')"
  }
}
```

Or by element ID from analysis:

```json
{
  "action": "browser_click",
  "value": {
    "url": "https://example.com",
    "selector": "button[0]"
  }
}
```

**Response:**
```
Clicked element. Page content after click:
[Sign Up page content...]
```

---

### 5. **browser_fill_form** - Submit Forms
Fill form fields and submit data.

```json
{
  "action": "browser_fill_form",
  "value": {
    "url": "https://example.com/contact",
    "data": "{\"name\": \"John Doe\", \"email\": \"john@example.com\", \"message\": \"Hello!\"}"
  }
}
```

**Response:**
```
Form submitted. Result page:
Thank you for your message! We'll get back to you soon.
[redirect page content...]
```

---

### 6. **browser_extract** - Extract Specific Info
Extract targeted information from a page.

```json
{
  "action": "browser_extract",
  "value": {
    "url": "https://example.com/pricing",
    "info": "pricing plans and features"
  }
}
```

**Response:**
```
=== PAGE INFORMATION ===
Title: Pricing Plans
Description: View our affordable pricing options

=== HEADINGS ===
- Basic Plan
- Professional Plan
- Enterprise Plan

=== AVAILABLE LINKS ===
[0] Features -> https://example.com/features
[1] FAQ -> https://example.com/faq

=== CONTENT RELEVANT TO: pricing plans and features ===
Basic Plan - $9/month
- 10 projects
- Email support

Professional Plan - $49/month
- Unlimited projects
- Priority support

Enterprise Plan - Custom pricing
- Everything included
- Dedicated support
```

---

## Common Workflows

### Workflow 1: Find Information on a Website

```
User: "Find the contact info on acme.com"

AI: "I'll visit acme.com and find their contact information for you."

Action 1: browser_visit to https://acme.com
Response: Shows all buttons, links, headings

Action 2: browser_click on "Contact" link
Response: Takes user to contact page

AI Final: "Here's acme.com's contact information:
- Email: hello@acme.com
- Phone: (555) 123-4567
- Address: 123 Main St, City, State"
```

### Workflow 2: Sign Up for a Service

```
User: "Create an account on service.com for me"

AI: "I'll navigate to service.com and help you create an account."

Action 1: browser_analyze https://service.com
Response: Shows sign up button location

Action 2: browser_click on sign up button
Response: Shows sign up form

Action 3: browser_fill_form with user details
Response: Account created

AI Final: "Your account has been created successfully!"
```

### Workflow 3: Extract Product Information

```
User: "Find all laptop products under $1000 on techstore.com"

AI: "I'll search techstore.com for laptops under $1000."

Action 1: browser_visit techstore.com
Response: Shows search button and navigation

Action 2: browser_click on search
Response: Shows search form

Action 3: browser_fill_form with search terms
Response: Shows results

AI Final: Shows all laptops under $1000 with prices and specs
```

---

## Advanced Interaction Patterns

### Pattern 1: Multi-Step Navigation
1. Visit homepage
2. Click category link
3. Click product link
4. Extract product details

### Pattern 2: Form Interaction
1. Analyze page for forms
2. Fill multiple form fields
3. Click submit
4. Extract confirmation info

### Pattern 3: Data Collection
1. Visit page
2. Analyze structure
3. Extract all links
4. Click each link
5. Collect data from each page

### Pattern 4: Search & Filter
1. Search for items
2. Filter results
3. Click on results
4. Extract details

---

## Response Examples

### Finding Information
```
User: "What's on the homepage of python.org?"

AI: "I'll visit python.org and see what's available on the homepage."

[browser_visit python.org]

AI: "The Python homepage has:
- Navigation menu with Documentation, Downloads, Community
- Featured articles about latest Python release
- Links to contribute and get involved
- Search functionality
- Download Python buttons
- Tutorial resources

Would you like me to explore any specific section?"
```

### Clicking Elements
```
User: "Go to the latest news on techcrunch.com"

AI: "I'll visit TechCrunch and find the latest news for you."

[browser_visit techcrunch.com]

AI: "I can see the TechCrunch homepage with several news articles. Would you like me to click on a specific article?"

User: "Click the first one"

[browser_click on first article link]

AI: "Here's the latest article on TechCrunch:
[Article content and details...]"
```

### Form Submission
```
User: "Subscribe me to the newsletter on example.com"

AI: "I'll visit example.com and subscribe you to their newsletter."

[browser_analyze example.com]
[browser_fill_form with email]

AI: "Great! I've subscribed you to the example.com newsletter. You should receive a confirmation email shortly."
```

---

## Tips for Best Results

✅ **Use browser_analyze first** - Understand page structure before interacting
✅ **Start with browser_visit** - See available buttons and links
✅ **Use specific selectors** - Target exact elements to click
✅ **Wait for page loads** - The agent automatically waits for pages
✅ **Provide context** - Tell the AI what you're looking for
✅ **Multi-step tasks** - Break complex actions into steps

---

## Supported Element Selection

The agent can find and click:
- ✅ Buttons (all types)
- ✅ Links (all href targets)
- ✅ Form fields (input, textarea, select)
- ✅ Checkboxes
- ✅ Radio buttons
- ✅ Dropdowns
- ✅ Custom interactive elements
- ✅ Elements with roles/attributes

---

## Limitations & Workarounds

| Issue | Workaround |
|-------|-----------|
| JavaScript-heavy pages | Use longer wait times, the agent handles this |
| Login required | Provide credentials via browser_fill_form |
| Captcha | Agent will explain what's blocking access |
| Page timeouts | Agent retries automatically |
| Complex navigation | Use browser_analyze to map structure |

---

## Action Reference

| Action | Purpose | Parameters |
|--------|---------|------------|
| `browser_search` | Search web | query string |
| `browser_visit` | Visit URL | {url, task} |
| `browser_analyze` | Analyze structure | URL string |
| `browser_click` | Click element | {url, selector} |
| `browser_fill_form` | Submit form | {url, data JSON} |
| `browser_extract` | Extract info | {url, info} |

---

## Examples by Use Case

### E-Commerce
- Visit product page
- Analyze reviews
- Click "Add to Cart"
- Submit order form

### Research
- Search for topic
- Visit relevant pages
- Extract key information
- Compile findings

### Account Management
- Visit login page
- Fill credentials
- Navigate to settings
- Update profile

### Data Collection
- Visit target site
- Click through pages
- Extract data from each
- Compile results

---

## Integration with Desktop Agent

Browser actions work alongside:
- 🖱️ Desktop mouse/keyboard control
- 📷 Screenshot analysis
- 📁 File operations
- 🖥️ System commands
- 💻 Python execution

**Example Combined Workflow:**
1. Take screenshot of desktop
2. Open browser via desktop click
3. Navigate to website via browser action
4. Extract data via browser_extract
5. Save results to file via file operations

---

## Getting Help

If an action fails:
1. AI will report the specific error
2. Try `browser_analyze` first to understand structure
3. Use more specific selectors
4. Break complex tasks into steps
5. Ask for alternative approaches

---

## Quick Reference

**See what's on a page:**
```json
{"action": "browser_visit", "value": {"url": "https://site.com", "task": "see all options"}}
```

**Understand page structure:**
```json
{"action": "browser_analyze", "value": "https://site.com"}
```

**Get specific info:**
```json
{"action": "browser_extract", "value": {"url": "https://site.com", "info": "what you need"}}
```

**Click something:**
```json
{"action": "browser_click", "value": {"url": "https://site.com", "selector": "button text"}}
```

**Submit a form:**
```json
{"action": "browser_fill_form", "value": {"url": "https://site.com", "data": "{\"field\": \"value\"}"}}
```

---

**Ready to explore the web!** Your AI agent can now interact with any website! 🌐
