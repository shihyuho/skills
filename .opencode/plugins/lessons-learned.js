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

  // Helper to generate context injection
  const getContext = () => {
    // Check if skill exists
    if (!fs.existsSync(skillPath)) {
      // If the skill file is missing (repo structure broken), we fail gracefully
      return null;
    }

    // We inject a condensed reminder to trigger the skill usage
    return `
<skill_reminder>
**Available Skill: lessons-learned**
This skill helps you capture and learn from mistakes to prevent repeated errors.

**WHEN TO USE (Triggers):**
1. **After Task Failure/Error**: Type errors, runtime exceptions, config mistakes.
2. **After Multiple Retries**: Same issue requires 2+ attempts to resolve.
3. **Unexpected Complexity**: Simple tasks turn hard.
4. **User Request**: "Let's document this", "Create a lesson".

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
