#!/usr/bin/env python3
"""
Fanfuaji (繁化姬) API Client

A Python wrapper for the Fanhuaji Chinese text conversion API.
Supports conversion between simplified/traditional Chinese, regional variants,
and phonetic transcriptions.

Usage as library:
    from fanfuaji import convert_text, Converter
    
    result = convert_text("软件开发", Converter.TAIWAN)
    print(result)  # Output: 軟體開發

Usage as CLI:
    python fanfuaji.py "软件开发" --converter Taiwan
    python fanfuaji.py "软件" --converter Taiwan --protect "软件"
    python fanfuaji.py "哦" --converter Taiwan --post-replace "哦=喔"
"""

import argparse
import json
import sys
from enum import Enum
from typing import Optional, Dict, List
from dataclasses import dataclass

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


class Converter(str, Enum):
    """Available converter types."""
    SIMPLIFIED = "Simplified"
    TRADITIONAL = "Traditional"
    CHINA = "China"
    HONGKONG = "Hongkong"
    TAIWAN = "Taiwan"
    PINYIN = "Pinyin"
    BOPOMOFO = "Bopomofo"
    MARS = "Mars"
    WIKI_SIMPLIFIED = "WikiSimplified"
    WIKI_TRADITIONAL = "WikiTraditional"


@dataclass
class ConversionResult:
    """Result of text conversion."""
    text: str
    converter: str
    used_modules: List[str]
    exec_time: float
    
    def __str__(self) -> str:
        return self.text


class FanfuajiAPI:
    """Fanfuaji API client."""
    
    BASE_URL = "https://api.zhconvert.org"
    
    def __init__(self, api_key: str = "", verify_ssl: bool = True):
        """
        Initialize API client.
        
        Args:
            api_key: API key for commercial use (empty for free tier)
            verify_ssl: Whether to verify SSL certificate
        """
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "FanfuajiPython/1.0"
        })
    
    def convert(
        self,
        text: str,
        converter: str,
        modules: Optional[Dict[str, int]] = None,
        user_pre_replace: Optional[Dict[str, str]] = None,
        user_post_replace: Optional[Dict[str, str]] = None,
        user_protect_replace: Optional[List[str]] = None,
        diff_enable: bool = False,
        prettify: bool = False,
        timeout: int = 10
    ) -> ConversionResult:
        """
        Convert text using specified converter.
        
        Args:
            text: Text to convert
            converter: Converter type (use Converter enum)
            modules: Module settings dict {module_name: 0|1}
            user_pre_replace: Replace before conversion {old: new}
            user_post_replace: Replace after conversion {old: new}
            user_protect_replace: Terms to protect from conversion
            diff_enable: Return diff between original and converted
            prettify: Prettify JSON response
            timeout: Request timeout in seconds
            
        Returns:
            ConversionResult with converted text and metadata
            
        Raises:
            ValueError: If API returns error
            RuntimeError: If request fails
        """
        data = {
            "converter": converter,
            "text": text,
            "apiKey": self.api_key,
            "diffEnable": diff_enable,
            "prettify": prettify
        }
        
        # Format modules as JSON string
        if modules:
            data["modules"] = json.dumps(modules)
        
        # Format pre-replace as newline-separated
        if user_pre_replace:
            data["userPreReplace"] = "\n".join(
                f"{old}={new}" for old, new in user_pre_replace.items()
            )
        
        # Format post-replace as newline-separated
        if user_post_replace:
            data["userPostReplace"] = "\n".join(
                f"{old}={new}" for old, new in user_post_replace.items()
            )
        
        # Format protect terms as newline-separated
        if user_protect_replace:
            data["userProtectReplace"] = "\n".join(user_protect_replace)
        
        try:
            response = self.session.post(
                url=f"{self.BASE_URL}/convert",
                data=data,
                verify=self.verify_ssl,
                timeout=timeout
            )
            response.raise_for_status()
            
        except requests.exceptions.Timeout:
            raise RuntimeError(f"Request timeout after {timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            raise RuntimeError(f"Connection failed: {e}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        
        try:
            result = response.json()
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON response: {e}")
        
        # Check API response code
        if result.get("code") != 0:
            raise ValueError(f"API error: {result.get('msg', 'Unknown error')}")
        
        data_obj = result.get("data", {})
        
        return ConversionResult(
            text=data_obj.get("text", ""),
            converter=data_obj.get("converter", converter),
            used_modules=data_obj.get("usedModules", []),
            exec_time=result.get("execTime", 0.0)
        )
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


# Convenience function for simple conversions
def convert_text(
    text: str,
    converter: str = Converter.TAIWAN,
    **kwargs
) -> str:
    """
    Convert text using specified converter (simple interface).
    
    Args:
        text: Text to convert
        converter: Converter type (default: Taiwan)
        **kwargs: Additional parameters passed to FanfuajiAPI.convert()
        
    Returns:
        Converted text string
        
    Example:
        >>> convert_text("软件开发", Converter.TAIWAN)
        '軟體開發'
    """
    with FanfuajiAPI() as api:
        result = api.convert(text, converter, **kwargs)
        return result.text


def main():
    """CLI interface."""
    parser = argparse.ArgumentParser(
        description="Fanfuaji Chinese text converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "软件开发" --converter Taiwan
  %(prog)s "软件" --converter Taiwan --protect "软件"
  %(prog)s "哦" --converter Taiwan --post-replace "哦=喔"
  %(prog)s "内存" --converter Taiwan --modules '{"GanToZuo": 0}'
  
Available converters:
  Simplified, Traditional, China, Hongkong, Taiwan,
  Pinyin, Bopomofo, Mars, WikiSimplified, WikiTraditional
        """
    )
    
    parser.add_argument(
        "text",
        help="Text to convert"
    )
    
    parser.add_argument(
        "-c", "--converter",
        default="Taiwan",
        choices=[c.value for c in Converter],
        help="Converter type (default: Taiwan)"
    )
    
    parser.add_argument(
        "--api-key",
        default="",
        help="API key for commercial use"
    )
    
    parser.add_argument(
        "--modules",
        type=str,
        help='Module settings as JSON string, e.g., \'{"GanToZuo": 0}\''
    )
    
    parser.add_argument(
        "--pre-replace",
        type=str,
        help='Pre-conversion replacements, e.g., "旧=新,另一个=替换"'
    )
    
    parser.add_argument(
        "--post-replace",
        type=str,
        help='Post-conversion replacements, e.g., "哦=喔,啰=囉"'
    )
    
    parser.add_argument(
        "--protect",
        type=str,
        help='Protected terms (comma-separated), e.g., "內存,硬盤,SSD"'
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed conversion information"
    )
    
    parser.add_argument(
        "--no-verify-ssl",
        action="store_true",
        help="Disable SSL certificate verification"
    )
    
    args = parser.parse_args()
    
    # Parse optional parameters
    kwargs = {}
    
    if args.modules:
        try:
            kwargs["modules"] = json.loads(args.modules)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in --modules: {args.modules}", file=sys.stderr)
            sys.exit(1)
    
    if args.pre_replace:
        kwargs["user_pre_replace"] = dict(
            pair.split("=", 1) for pair in args.pre_replace.split(",")
        )
    
    if args.post_replace:
        kwargs["user_post_replace"] = dict(
            pair.split("=", 1) for pair in args.post_replace.split(",")
        )
    
    if args.protect:
        kwargs["user_protect_replace"] = [
            term.strip() for term in args.protect.split(",")
        ]
    
    # Perform conversion
    try:
        with FanfuajiAPI(
            api_key=args.api_key,
            verify_ssl=not args.no_verify_ssl
        ) as api:
            result = api.convert(
                text=args.text,
                converter=args.converter,
                timeout=args.timeout,
                **kwargs
            )
            
            if args.verbose:
                print(f"Converter: {result.converter}")
                print(f"Used modules: {', '.join(result.used_modules)}")
                print(f"Execution time: {result.exec_time:.3f}s")
                print(f"Result: {result.text}")
            else:
                print(result.text)
                
    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
