# Fanfuaji API Skill

Chinese text conversion API reference for simplified/traditional conversion and regional variants.

## Overview

This skill provides comprehensive guidance for using the Fanhuaji (繁化姬) API to convert Chinese text between different character systems, regional variants, and phonetic transcriptions.

**Key capabilities:**
- Simplified ↔ Traditional Chinese conversion
- Regional terminology (China, Taiwan, Hong Kong)
- Phonetic transcription (Pinyin, Bopomofo/Zhuyin)
- Custom replacement rules
- Term protection from conversion

## When to Use

Use this skill when:
- Building applications that need Chinese text conversion
- Implementing localization for different Chinese-speaking regions
- Converting Chinese to romanized forms (Pinyin)
- Need fine-grained control over conversion behavior

## Features

- **10 converter types** for different use cases
- **Module system** to enable/disable specific conversions
- **Custom replacements** before and after conversion
- **Protected terms** that won't be converted
- **Complete API reference** with Python and TypeScript examples

## How It Works

The Fanhuaji API accepts POST requests with:
1. **Converter type** (Taiwan, Simplified, Pinyin, etc.)
2. **Text to convert**
3. **Optional parameters** for fine-grained control

Returns JSON response with:
- Converted text
- Modules used
- Execution time
- Optional diff

## Examples

### Using the Python Script (Recommended)

```bash
# Install dependencies first
pip install -r scripts/requirements.txt

# Basic conversion
python scripts/fanfuaji.py "软件开发" --converter Taiwan
# Output: 軟體開發

# With protected terms
python scripts/fanfuaji.py "软件" --converter Taiwan --protect "软件"

# With detailed output
python scripts/fanfuaji.py "软件" --converter Taiwan --verbose
```

### As Python Library

```python
import sys
sys.path.insert(0, 'scripts')
from fanfuaji import convert_text, Converter

# Simple conversion
result = convert_text("软件开发", Converter.TAIWAN)
print(result)  # Output: 軟體開發
```

### Basic Conversion

```python
import requests

response = requests.post(
    url="https://api.zhconvert.org/convert",
    data={
        "converter": "Taiwan",
        "text": "软件开发"
    }
)

result = response.json()
print(result["data"]["text"])  # Output: 軟體開發
```

### Advanced with Custom Rules

```python
import json

response = requests.post(
    url="https://api.zhconvert.org/convert",
    data={
        "converter": "Taiwan",
        "text": "内存和硬盘",
        "modules": json.dumps({"GanToZuo": 0}),
        "userPostReplace": "哦=喔",
        "userProtectReplace": "內存"
    }
)
```

## File Structure

```
fanfuaji/
├── SKILL.md              # Complete API reference for AI agents
├── README.md             # Human-readable overview (this file)
└── scripts/
    ├── fanfuaji.py       # Python API wrapper and CLI tool
    └── requirements.txt  # Python dependencies
```

## Installation

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Or install requests directly
pip install requests
```

## Best Practices

**Do:**
- Always check `code` field in response (0 = success)
- Use JSON string for `modules` parameter
- Use newline-separated strings for replacement rules
- Include timeout in production requests
- Implement retry logic with exponential backoff

**Don't:**
- Send `modules` as Python dict (must be JSON string)
- Use escaped newlines in replacement strings
- Send protected terms as array (must be newline-separated)
- Skip error handling

## Limitations

- Free tier has rate limits (check official docs)
- Commercial use requires API key
- Network latency affects conversion speed
- Not suitable for real-time user input conversion

## Related Files

- [SKILL.md](SKILL.md) - Complete API reference with all converters, parameters, and examples
- [Fanhuaji Official Site](https://zhconvert.org)
- [API Documentation](https://docs.zhconvert.org)

## License

MIT
