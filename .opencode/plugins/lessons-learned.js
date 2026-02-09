/**
 * Lessons Learned Plugin for OpenCode
 *
 * Injects proactive reminders for the "lessons-learned" skill via system prompt transform.
 * Ensures the AI agent is aware of WHEN and HOW to trigger the lesson documentation workflow.
 *
 * This version uses relative path loading to ensure stability regardless of symlink status.
 */

import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export const LessonsLearnedPlugin = async ({ client }) => {
  // Load skill content relative to the plugin file
  // This assumes the structure:
  // .opencode/plugins/lessons-learned.js
  // skills/lessons-learned/SKILL.md
  const skillPath = path.resolve(__dirname, '../../skills/lessons-learned/SKILL.md');

  const getContext = () => {
    if (!fs.existsSync(skillPath)) {
      return null;
    }

    return `
<skill_reminder>
**Available Skill: lessons-learned**
Captures and documents problem-solving processes - failed attempts that eventually succeeded, unexpected tool interactions, configuration conflicts, or any debugging process worth documenting for future encounters.

**WHEN TO USE (Triggers):**
1. **After Solving Through Iteration**: Failed attempts that eventually succeeded after 2+ retries.
2. **Unexpected Tool/Config Behavior**: Tool interactions or configuration conflicts that weren't obvious.
3. **Complex Debugging Process**: Any debugging process that revealed valuable insights worth documenting.
4. **User Request**: "Let's document this", "Create a lesson", "We should remember this".

**INSTRUCTION:**
If any of these triggers occur during this session, you MUST:
1. Suggest creating a lesson-learned entry to the user.
2. If confirmed, use the \`skill\` tool to load \`lessons-learned\` and follow the workflow.
</skill_reminder>
`;
  };

  return {
    'experimental.chat.system.transform': async (_input, output) => {
      const context = getContext();
      if (context) {
        // Ensure system prompt array exists
        output.system ||= [];
        // Inject our reminder at the end of the system prompt
        output.system.push(context);
      }
    }
  };
};
