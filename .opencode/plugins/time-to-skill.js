/**
 * Time to Skill Plugin for OpenCode
 *
 * Injects proactive reminders for the "time-to-skill" skill via system prompt transform.
 * Monitors repeated task patterns and suggests converting them into reusable skills.
 *
 * This version uses relative path loading to ensure stability regardless of symlink status.
 */

import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export const TimeToSkillPlugin = async ({ client }) => {
  const skillPath = path.resolve(__dirname, '../../skills/time-to-skill/SKILL.md');

  const getContext = () => {
    if (!fs.existsSync(skillPath)) {
      return null;
    }
    return `
<skill_reminder>
**Available Skill: time-to-skill**
This skill helps you capture repeated workflows and convert them into reusable skills.

**WHEN TO USE (Triggers):**
1. **After 3+ Similar Tasks**: User performs conceptually similar tasks 3 or more times (semantic pattern matching, not just identical commands).
2. **Repeated Workflows**: User follows the same sequence of steps multiple times (e.g., "create branch → code → test → PR").
3. **User Request**: "Turn this into a skill", "Automate this workflow", "I keep doing this repeatedly".

**INSTRUCTION:**
If any of these triggers occur during this session, you MUST:
1. Suggest converting the workflow into a reusable skill to the user.
2. Explain the pattern you detected and estimated time savings.
3. If confirmed, use the \`skill\` tool to load \`time-to-skill\` and follow the workflow.

**DETECTION GUIDELINES:**
- Use semantic analysis to identify similar tasks (not just command matching)
- Track workflow patterns (sequences of operations)
- Threshold: 3 occurrences within the same session or day
- Avoid suggesting for trivial tasks (< 3 steps) or one-off operations
</skill_reminder>
`;
  };

  return {
    'experimental.chat.system.transform': async (_input, output) => {
      const context = getContext();
      if (context) {
        output.system ||= [];
        output.system.push(context);
      }
    }
  };
};
