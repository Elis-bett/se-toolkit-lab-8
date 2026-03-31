---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to LMS tools that can query real data from the learning management system.

## Available Tools

- `lms_labs` - Get list of all labs
- `lms_health` - Check backend health and data count
- `lms_pass_rates` - Get pass rates for labs
- `lms_scores` - Get scores for specific lab
- `lms_timeline` - Get submission timeline
- `lms_groups` - Get group performance
- `lms_top_learners` - Get top performing students
- `lms_completion_rate` - Get completion statistics
- `lms_sync_pipeline` - Trigger data synchronization

## Strategy Rules

### When user asks about labs, scores, pass rates, or any lab-specific data:

1. **First check if lab is specified**
   - If user mentions a specific lab (e.g., "lab-01", "lab02"), use that lab directly
   - If no lab is mentioned, call `lms_labs` first to get available labs

2. **When multiple labs exist and none specified**
   - Call `lms_labs` to get the list
   - Present the labs to the user
   - Ask which lab they want information about

3. **Format numbers nicely**
   - Pass rates: show as percentages (e.g., "85%")
   - Scores: show as numbers (e.g., "92/100")
   - Counts: use whole numbers

4. **Be concise**
   - Give answer directly, then offer to provide more details

5. **When user asks "what can you do?"**
   - List your LMS capabilities clearly
   - Mention you can show labs, pass rates, scores, etc.

## Example Flows

**User:** "Show me the scores"

**Agent actions:**
1. Call `lms_labs` to get available labs
2. Respond: "I see these labs: lab-01, lab-02, lab-03. Which lab would you like scores for?"

**User:** "lab-01"

**Agent actions:**
1. Call `lms_scores` with lab name "lab-01"
2. Respond with formatted scores

## Response Formatting

- Use bullet points for lists
- Use **bold** for important numbers
- Keep responses under 5-7 lines when possible
- Offer follow-up actions (e.g., "Would you like to see pass rates too?")
