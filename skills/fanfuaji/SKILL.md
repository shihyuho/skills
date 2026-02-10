---
name: fanfuaji
description: Use when user requests Chinese text conversion, checking, or ensuring terminology - "使用繁體中文", "使用台灣用語", "轉換成台灣用語", "確保都是台灣用語", "統一台灣用語", "改成台灣用語", "用台灣的說法", "簡體轉繁體", "繁體轉簡體", "全部改成繁體", "轉成台灣繁體", check/ensure Taiwan/Hong Kong/China terminology, simplified/traditional conversion, or phonetic transcription (Pinyin/Bopomofo)
---

# Fanfuaji - Chinese Text Converter

## Overview

Convert Chinese text between simplified/traditional, regional variants (China/Taiwan/Hong Kong), and phonetic forms (Pinyin/Bopomofo) using the Fanhuaji API.

**This skill includes `scripts/fanfuaji.py` - a ready-to-use Python wrapper that handles all API complexity.**

## When to Use

Use this skill when:
- User requests output in Traditional Chinese, Taiwan terminology, etc.
- Converting between simplified ↔ traditional Chinese
- Applying regional terminology (China, Taiwan, Hong Kong)
- Converting to Pinyin or Bopomofo (Zhuyin)
- Need custom replacement rules or term protection

## Important: Converter Selection

**If user does NOT explicitly specify the conversion target (Taiwan/Hong Kong/China/Simplified/Traditional), you MUST ask first.**

Use the `question` tool to present single-choice options:

```
Which converter would you like to use?
```

**Common options:**
- 台灣化 (Taiwan) - Traditional Chinese with Taiwan terminology
- 繁體化 (Traditional) - Traditional Chinese only
- 简体化 (Simplified) - Simplified Chinese only
- 中国化 (China) - Simplified Chinese with China terminology
- 香港化 (Hongkong) - Traditional Chinese with Hong Kong terminology

**Examples of ambiguous requests:**
- ❌ "轉換成繁體" → Ask: Traditional or Taiwan? Hong Kong?
- ❌ "使用繁體中文" → Ask: Which region?
- ❌ "確保都是繁體" → Ask: Traditional only or Taiwan/Hong Kong variant?
- ✅ "使用台灣用語" → Clear: Use Taiwan converter
- ✅ "轉成香港繁體" → Clear: Use Hongkong converter

## Quick Reference: Available Converters

| Converter | API Name | Description |
|-----------|----------|-------------|
| 繁體化 | `Traditional` | Convert to traditional Chinese |
| 台灣化 | `Taiwan` | Traditional + Taiwan terminology |
| 香港化 | `Hongkong` | Traditional + Hong Kong terminology |
| 注音化 | `Bopomofo` | Convert to Bopomofo (Zhuyin) |
| 維基繁體化 | `WikiTraditional` | Traditional (Wikipedia dict only) |
| 简体化 | `Simplified` | Convert to simplified Chinese |
| 中国化 | `China` | Simplified + China terminology |
| 拼音化 | `Pinyin` | Convert to Pinyin romanization |
| 维基简体化 | `WikiSimplified` | Simplified (Wikipedia dict only) |
| 火星化 | `Mars` | Convert to Mars text (internet slang) |

## Using the Script

### Basic Usage

```bash
# Convert text
python scripts/fanfuaji.py "软件开发" --converter Taiwan
# Output: 軟體開發

# Convert file
python scripts/fanfuaji.py --file input.txt --converter Taiwan

# File to file (supports file:// URI)
python scripts/fanfuaji.py -f input.txt -o output.txt -c Taiwan
python scripts/fanfuaji.py -f file:///in.txt -o file:///out.txt -c Taiwan
```

### Advanced Options

```bash
# Protect specific terms from conversion
python scripts/fanfuaji.py "软件" --converter Taiwan --protect "软件"

# Post-conversion replacement
python scripts/fanfuaji.py "哦" --converter Taiwan --post-replace "哦=喔,啰=囉"

# Disable specific modules
python scripts/fanfuaji.py "内存" --converter Taiwan --modules '{"GanToZuo": 0}'

# Verbose output
python scripts/fanfuaji.py "软件" --converter Taiwan --verbose
```

### As Python Library

```python
import sys
sys.path.insert(0, 'scripts')
from fanfuaji import convert_text, FanfuajiAPI, Converter

# Simple conversion
result = convert_text("软件开发", Converter.TAIWAN)
print(result)  # Output: 軟體開發

# Advanced usage
with FanfuajiAPI() as api:
    result = api.convert(
        text="内存和硬盘",
        converter=Converter.TAIWAN,
        modules={"GanToZuo": 0},
        user_post_replace={"哦": "喔"},
        user_protect_replace=["內存"]
    )
    print(result.text)
    print(f"Used modules: {result.used_modules}")
```

## Common Use Cases

### User Asks for Taiwan Terminology

```bash
# User: "使用台灣用語輸出"
python scripts/fanfuaji.py "软件和内存" --converter Taiwan
# Output: 軟體和記憶體
```

### Convert File Content

```bash
# Read simplified Chinese file, output traditional
python scripts/fanfuaji.py --file document.txt --converter Taiwan --output output.txt
```

### Batch Processing with Custom Rules

```bash
# Convert with term protection and replacement
python scripts/fanfuaji.py \
  --file input.txt \
  --converter Taiwan \
  --protect "API,GitHub" \
  --post-replace "哦=喔,啰=囉" \
  --output converted.txt
```

## Script Features

- ✅ **Zero dependencies** (uses stdlib `urllib`)
- ✅ **File I/O support** (text, file paths, file:// URIs)
- ✅ **Error handling** (network, API errors, file errors)
- ✅ **Flexible output** (stdout or file)
- ✅ **Full API access** (modules, replacements, protection)

## Related Resources

- [Fanhuaji Official Site](https://zhconvert.org)
- [API Documentation](https://docs.zhconvert.org)
- [Script Source](scripts/fanfuaji.py) - Read for implementation details
- [GitHub Discussions](https://github.com/Fanhuaji/discussion/issues)

## Notes

- **Free tier** available without API key
- **Commercial use** requires paid API key ([details](https://docs.zhconvert.org/commercial))
- **Rate limits** apply - check official docs
- Script handles all API parameter formatting automatically
