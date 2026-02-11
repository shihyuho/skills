# GitHub Actions Dynamic Matrix Research Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Research best practices for dynamic matrix generation in GitHub Actions for directory-based validation jobs and provide a robust pattern.

**Architecture:** Two-job pattern: a "discovery" job that outputs a JSON array of directories, and a "matrix" job that consumes this array to run parallel validation.

**Tech Stack:** GitHub Actions, Shell (bash/sh), JSON (jq).

---

### Task 1: Documentation Discovery (Phase 0.5)

**Step 1: Find official GitHub Actions documentation for dynamic matrices**
- Search for "GitHub Actions dynamic matrix documentation"
- Identify the official URL and base structure.

**Step 2: Check for versioning and sitemap**
- Verify if there are specific versions or if it's just "latest".
- Fetch sitemap if possible to find related sections (e.g., expressions, outputs).

### Task 2: Targeted Research (Phase 1)

**Step 1: Research JSON output safety**
- Find best practices for escaping JSON in GHA outputs.
- Look for `jq` patterns to generate valid JSON arrays from directory lists.

**Step 2: Research shell portability**
- Compare `find`, `ls`, and globbing in GHA runners (Ubuntu, macOS, Windows).
- Identify common pitfalls with spaces or special characters in directory names.

**Step 3: Find real-world examples**
- Use `grep_app_searchGitHub` to find repositories using `matrix: ${{ fromJson(needs.job_id.outputs.matrix) }}`.

### Task 3: Evidence Synthesis (Phase 2)

**Step 1: Construct the robust pattern**
- Draft the YAML for the discovery job and the matrix job.
- Include comments on shell portability and safety.

**Step 2: Document pitfalls and citations**
- List common errors (e.g., output size limits, JSON formatting).
- Provide GitHub permalinks to evidence.

**Step 3: Final Review**
- Verify the pattern against the user's context (`skills/*` validation).
