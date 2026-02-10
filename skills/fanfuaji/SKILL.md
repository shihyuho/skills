---
name: fanfuaji
description: Use when user requests Chinese text conversion - "使用台灣用語", "轉換成台灣用語", "簡體轉繁體", "繁體轉簡體", simplified/traditional conversion, regional variants (China/Taiwan/Hong Kong), or phonetic transcription (Pinyin/Bopomofo)
---

# Fanhuaji API

## Overview

Fanhuaji (繁化姬) provides a powerful API for Chinese text conversion, supporting various character systems, regional variants, and phonetic transcriptions. The API handles bidirectional conversion between simplified and traditional Chinese, plus region-specific terminology adjustments.

**Core principle:** Send text to `/convert` endpoint with converter type and optional parameters. API returns converted text with metadata.

## When to Use

Use this skill when:
- Converting between simplified and traditional Chinese
- Applying regional terminology (China, Taiwan, Hong Kong)
- Converting Chinese to Pinyin or Bopomofo (Zhuyin)
- Converting to Mars text (火星文)
- Need fine-grained control over conversion modules
- Custom replacement rules or protected terms required

Don't use when:
- Simple one-off conversions (use website instead)
- Real-time user input (API has rate limits)
- Client-side only solutions needed (API requires network)

## API Endpoint

**Base URL:** `https://api.zhconvert.org`

**Endpoint:** `POST /convert`

**Request Format:** `application/x-www-form-urlencoded`

## Quick Reference

### Available Converters

| Converter | API Name | Description | Category |
|-----------|----------|-------------|----------|
| 简体化 | `Simplified` | Convert to simplified Chinese | Basic |
| 繁體化 | `Traditional` | Convert to traditional Chinese | Basic |
| 中国化 | `China` | Simplified + China terminology | Regional |
| 香港化 | `Hongkong` | Traditional + Hong Kong terminology | Regional |
| 台灣化 | `Taiwan` | Traditional + Taiwan terminology | Regional |
| 拼音化 | `Pinyin` | Convert to Pinyin romanization | Phonetic |
| 注音化 | `Bopomofo` | Convert to Bopomofo (Zhuyin) | Phonetic |
| 火星化 | `Mars` | Convert to Mars text (internet slang) | Special |
| 维基简体化 | `WikiSimplified` | Simplified (Wikipedia dictionary only) | Wiki |
| 維基繁體化 | `WikiTraditional` | Traditional (Wikipedia dictionary only) | Wiki |

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `converter` | string | Converter type (see table above) | `"Taiwan"` |
| `text` | string | Text to convert | `"软件"` |

### Optional Parameters

| Parameter | Type | Format | Description |
|-----------|------|--------|-------------|
| `apiKey` | string | - | API key for commercial use (leave empty for free tier) |
| `modules` | JSON string | `{"ModuleName": 0\|1}` | Enable/disable conversion modules (1=on, 0=off) |
| `userPreReplace` | string | `old1=new1\nold2=new2` | Replace before conversion (newline-separated) |
| `userPostReplace` | string | `old1=new1\nold2=new2` | Replace after conversion (newline-separated) |
| `userProtectReplace` | string | `term1\nterm2\nterm3` | Protect terms from conversion (newline-separated) |
| `diffEnable` | boolean | - | Return diff between original and converted (default: false) |
| `prettify` | boolean | - | Prettify JSON response (default: false) |

## Implementation

### Quick Start: Using the Provided Script

**This skill includes `scripts/fanfuaji.py` - a ready-to-use Python wrapper for the API.**

**Installation:**
```bash
pip install -r scripts/requirements.txt
```

**As CLI:**
```bash
# Basic conversion
python scripts/fanfuaji.py "软件开发" --converter Taiwan

# With protected terms
python scripts/fanfuaji.py "软件" --converter Taiwan --protect "软件"

# With post-conversion replacement
python scripts/fanfuaji.py "哦" --converter Taiwan --post-replace "哦=喔"

# With module control
python scripts/fanfuaji.py "内存" --converter Taiwan --modules '{"GanToZuo": 0}'

# Show details
python scripts/fanfuaji.py "软件" --converter Taiwan --verbose
```

**As Python library:**
```python
import sys
sys.path.insert(0, 'scripts')
from fanfuaji import convert_text, FanfuajiAPI, Converter

# Simple conversion
result = convert_text("软件开发", Converter.TAIWAN)
print(result)  # Output: 軟體開發

# Advanced usage with API client
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

### Direct API Request (Python)

```python
import requests

# Basic conversion
response = requests.post(
    url="https://api.zhconvert.org/convert",
    data={
        "converter": "Taiwan",
        "text": "软件开发"
    },
    headers={"user-agent": "MyApp/1.0"}
)

result = response.json()

if result["code"] == 0:
    print(result["data"]["text"])  # Output: 軟體開發
else:
    print(f"Error: {result['msg']}")
```

### Advanced Request with Options

```python
import requests
import json

# Taiwan localization with custom rules
response = requests.post(
    url="https://api.zhconvert.org/convert",
    data={
        "converter": "Taiwan",
        "text": "内存和硬盘空间",
        "apiKey": "",  # Empty for free tier
        
        # Disable specific module
        "modules": json.dumps({
            "GanToZuo": 0  # Disable 干→幹 conversion
        }),
        
        # Post-conversion replacement
        "userPostReplace": "哦=喔\n啰=囉",
        
        # Protect terms from conversion
        "userProtectReplace": "內存",  # Keep "內存" unchanged
        
        "prettify": False
    }
)

result = response.json()
```

### JavaScript/TypeScript Example

```typescript
async function convertText(text: string, converter: string): Promise<string> {
    const response = await fetch("https://api.zhconvert.org/convert", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "MyApp/1.0"
        },
        body: new URLSearchParams({
            converter: converter,
            text: text,
            prettify: "false"
        })
    });

    const result = await response.json();

    if (result.code === 0) {
        return result.data.text;
    } else {
        throw new Error(`Fanhuaji API error: ${result.msg}`);
    }
}

// Usage
const converted = await convertText("软件", "Taiwan");
console.log(converted);  // Output: 軟體
```

### Response Structure

```json
{
    "code": 0,
    "msg": "success",
    "revisions": {
        "build": "2024.10.15",
        "msg": "Release note",
        "time": 1729000000
    },
    "execTime": 0.123,
    "data": {
        "converter": "Taiwan",
        "text": "軟體開發",
        "diff": null,
        "jpTextStyles": [],
        "usedModules": ["Traditional", "TW"],
        "textFormat": "text"
    }
}
```

**Response Fields:**
- `code`: `0` = success, non-zero = error
- `msg`: Status message
- `data.text`: Converted text result
- `data.usedModules`: List of modules applied
- `execTime`: API execution time in seconds

## Common Mistakes

**Note:** Using the provided `fanfuaji.py` script avoids these mistakes automatically.

### ❌ Wrong: Sending modules as dictionary
```python
data = {
    "modules": {"GanToZuo": 0}  # Wrong - dict object
}
```

### ✅ Correct: JSON string
```python
import json
data = {
    "modules": json.dumps({"GanToZuo": 0})  # Correct - JSON string
}
```

---

### ❌ Wrong: Multi-line strings with escaped newlines
```python
data = {
    "userPostReplace": "哦\\n喔"  # Wrong - escaped newline
}
```

### ✅ Correct: Real newline characters
```python
data = {
    "userPostReplace": "哦=喔\n啰=囉"  # Correct - actual newlines
}
```

---

### ❌ Wrong: Array for protected terms
```python
data = {
    "userProtectReplace": ["內存", "硬盤"]  # Wrong - array
}
```

### ✅ Correct: Newline-separated string
```python
data = {
    "userProtectReplace": "內存\n硬盤"  # Correct - newline-separated
}
```

---

### ❌ Wrong: Not checking response code
```python
result = response.json()
text = result["data"]["text"]  # May crash if error
```

### ✅ Correct: Always check code first
```python
result = response.json()
if result["code"] == 0:
    text = result["data"]["text"]
else:
    handle_error(result["msg"])
```

## Parameter Format Reference

### modules (JSON string)

```python
# Format: JSON object with module names as keys, 0 or 1 as values
import json

modules = json.dumps({
    "GanToZuo": 0,      # Disable this module
    "AnotherModule": 1  # Enable this module
})
```

**Common modules:**
- `GanToZuo`: 干↔幹 conversion
- Check official docs for complete module list

### userPreReplace (newline-separated pairs)

```python
# Format: old=new, one per line
user_pre_replace = "旧词=新词\n另一个=替换"
```

Replacements applied **before** conversion.

### userPostReplace (newline-separated pairs)

```python
# Format: old=new, one per line
user_post_replace = "哦=喔\n啰=囉"
```

Replacements applied **after** conversion.

### userProtectReplace (newline-separated terms)

```python
# Format: one term per line
user_protect_replace = "內存\n硬盤\nSSD"
```

Protected terms are **not converted**.

## Error Handling

**Using the provided script:**
```python
from fanfuaji import convert_text, Converter

try:
    result = convert_text("软件", Converter.TAIWAN)
    print(result)
except (ValueError, RuntimeError) as e:
    print(f"Error: {e}")
```

**Direct API usage:**
```python
import requests
from requests.exceptions import RequestException

def safe_convert(text: str, converter: str) -> str:
    try:
        response = requests.post(
            url="https://api.zhconvert.org/convert",
            data={"converter": converter, "text": text},
            timeout=10,  # Add timeout
            verify=True   # Verify SSL certificate
        )
        
        response.raise_for_status()  # Raise for HTTP errors
        
        result = response.json()
        
        if result["code"] != 0:
            raise ValueError(f"API error: {result['msg']}")
        
        return result["data"]["text"]
        
    except RequestException as e:
        # Network errors, timeouts, etc.
        raise RuntimeError(f"Request failed: {e}") from e
    except (KeyError, ValueError) as e:
        # Invalid response format or API error
        raise RuntimeError(f"Invalid response: {e}") from e
```

## Commercial Use

**Free tier:** Available for general use without API key.

**Commercial use:** Requires paid API key. See [Fanhuaji commercial documentation](https://docs.zhconvert.org/commercial).

**Rate limits:** Check official docs for current limits. Implement retry logic with exponential backoff for production use.

## Related Resources

- [Fanhuaji Official Site](https://zhconvert.org)
- [Fanhuaji API Documentation](https://docs.zhconvert.org)
- [GitHub Discussions](https://github.com/Fanhuaji/discussion/issues)
- [Telegram Group](https://t.me/fanhuaji)

## Real-World Impact

**Sublime Text Plugin:** [Sublime-Fanhuaji](https://github.com/Fanhuaji/Sublime-Fanhuaji) demonstrates production usage with:
- Batch text conversion with delimiter strategy
- Settings-based configuration
- Module customization
- Error handling patterns
