import path from "path";

const SOT_FILES = ["task_plan.md", "findings.md", "progress.md"];
const NOTES_ROOT = path.join("docs", "notes");
const DEBOUNCE_MS = 12000;
const COOLDOWN_MS = 45000;

function resolveAbsPath(inputPath, worktree) {
  if (!inputPath || typeof inputPath !== "string") return "";
  if (path.isAbsolute(inputPath)) return path.resolve(inputPath);
  return path.resolve(worktree, inputPath);
}

function isSotTarget(inputPath, worktree) {
  const abs = resolveAbsPath(inputPath, worktree);
  if (!abs) return false;
  return SOT_FILES.some((name) => abs === path.resolve(worktree, name));
}

function isNotesTarget(inputPath, worktree) {
  const abs = resolveAbsPath(inputPath, worktree);
  if (!abs) return false;
  const notesAbs = path.resolve(worktree, NOTES_ROOT);
  return abs === notesAbs || abs.startsWith(`${notesAbs}${path.sep}`);
}

function createHarvestAutoCapturePlugin({ client, worktree }) {
  let activeSessionID = "";
  let pendingSotChange = false;
  let waitingCaptureSignal = false;
  let captureInFlight = false;
  let debounceTimer = null;
  let lastTriggerAtMs = 0;

  const log = async (level, message, extra = {}) => {
    if (!client?.app?.log) return;
    try {
      await client.app.log({
        body: {
          service: "harvest-auto-capture",
          level,
          message,
          extra,
        },
      });
    } catch {
    }
  };

  const captureCore = async (sessionID, reason) => {
    if (!sessionID || captureInFlight) return;

    const nowMs = Date.now();
    if (nowMs - lastTriggerAtMs < COOLDOWN_MS) return;

    captureInFlight = true;
    try {
      let dispatched = false;
      let lastError = null;

      for (let attempt = 1; attempt <= 2; attempt += 1) {
        try {
          await client.session.prompt({
            path: { id: sessionID },
            query: { directory: worktree },
            body: {
              parts: [
                {
                  type: "text",
                  text: "Invoke `harvest:harvest` now and force one key-update snapshot from current SOT (`task_plan.md`, `findings.md`, `progress.md`) with `when/change/why/source_ref`, same-day append, and `sot_fingerprint` dedupe/no-op.",
                },
              ],
            },
          });
          dispatched = true;
          break;
        } catch (error) {
          lastError = error;
          await log("warn", "harvest capture dispatch failed", {
            reason,
            sessionID,
            attempt,
            error: error instanceof Error ? error.message : String(error),
          });
        }
      }

      if (!dispatched) {
        throw (lastError ?? new Error("Unknown dispatch failure"));
      }

      pendingSotChange = false;
      waitingCaptureSignal = true;
      lastTriggerAtMs = Date.now();
      await log("info", "harvest capture dispatched", { reason, sessionID });
    } catch (error) {
      pendingSotChange = true;
      waitingCaptureSignal = false;
      await log("warn", "harvest capture failed", {
        reason,
        sessionID,
        error: error instanceof Error ? error.message : String(error),
      });
    } finally {
      captureInFlight = false;
    }
  };

  const scheduleCapture = (reason) => {
    pendingSotChange = true;
    waitingCaptureSignal = false;
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const sessionID = activeSessionID;
      if (sessionID) void captureCore(sessionID, "debounced-sot-change");
    }, DEBOUNCE_MS);
  };

  return {
    event: async ({ event }) => {
      if (!event?.type) return;

      if (event.type === "session.created" || event.type === "session.updated") {
        activeSessionID = event?.properties?.info?.id || activeSessionID;
      }

      if (event.type === "session.status") {
        activeSessionID = event?.properties?.sessionID || activeSessionID;
      }

      if (event.type === "file.edited" || event.type === "file.watcher.updated") {
        const changed = event?.properties?.file;

        if (waitingCaptureSignal && isNotesTarget(changed, worktree)) {
          waitingCaptureSignal = false;
          await log("info", "harvest capture confirmed by notes output", {
            changed,
          });
        }

        if (isSotTarget(changed, worktree)) {
          scheduleCapture("sot-file-edited");
        }
      }

      if (event.type === "session.idle") {
        const sessionID = event?.properties?.sessionID || activeSessionID;
        if (!sessionID) return;
        activeSessionID = sessionID;
        if (pendingSotChange) {
          await captureCore(sessionID, "session-idle-convergence");
        }
      }
    },
  };
}

export const harvest = async (input) => createHarvestAutoCapturePlugin(input);
