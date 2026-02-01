"""Font fallback helpers for Kivy markup rendering."""

from __future__ import annotations

import logging
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

from fontTools.ttLib import TTCollection, TTFont
from kivy.core.text import LabelBase
from kivy.resources import resource_find

_fonttools_logger = logging.getLogger("fontTools")
if _fonttools_logger.level < logging.WARNING:
    _fonttools_logger.setLevel(logging.WARNING)


def escape_kivy_markup(text: str) -> str:
    """Escape Kivy markup special characters for safe display."""
    text = text.replace('&', '&amp;')
    text = text.replace('[', '&bl;')
    text = text.replace(']', '&br;')
    return text


_NEUTRAL_CODEPOINTS = frozenset({
    0x200D,  # zero width joiner
    0x200C,  # zero width non-joiner
    0xFEFF,  # zero width no-break space
})


def _is_neutral_char(ch: str) -> bool:
    if ch.isspace():
        return True
    if unicodedata.combining(ch):
        return True
    codepoint = ord(ch)
    if codepoint in _NEUTRAL_CODEPOINTS:
        return True
    if 0xFE00 <= codepoint <= 0xFE0F:
        return True
    if 0xE0100 <= codepoint <= 0xE01EF:
        return True
    return False


@lru_cache(maxsize=128)
def _resolve_font_path(font_name: str) -> Optional[str]:
    if not font_name:
        return None

    raw_path = Path(font_name)
    if raw_path.suffix.lower() in ('.ttf', '.ttc', '.otf', '.otc') and raw_path.exists():
        return str(raw_path)

    resolved = resource_find(font_name)
    if resolved:
        return resolved

    font_registry = getattr(LabelBase, '_fonts', {}) or {}
    entry = font_registry.get(font_name)

    candidates: List[str] = []
    if isinstance(entry, str):
        candidates.append(entry)
    elif isinstance(entry, (list, tuple, set)):
        candidates.extend([value for value in entry if isinstance(value, str)])
    elif isinstance(entry, dict):
        for key in ('regular', 'fn_regular', 'file', 'filename', 'path'):
            value = entry.get(key)
            if isinstance(value, str):
                candidates.append(value)
        candidates.extend([value for value in entry.values() if isinstance(value, str)])

    for candidate in candidates:
        resolved_candidate = resource_find(candidate) or candidate
        if Path(resolved_candidate).exists():
            return resolved_candidate

    return None


@lru_cache(maxsize=64)
def _load_font_codepoints(font_path: str) -> frozenset[int]:
    if not font_path:
        return frozenset()

    normalized_path = font_path.lower()

    try:
        if normalized_path.endswith(('.ttc', '.otc')):
            collection = TTCollection(font_path)
            codepoints: set[int] = set()
            try:
                for font in collection.fonts:
                    cmap = font.getBestCmap() or {}
                    codepoints.update(cmap.keys())
            finally:
                collection.close()
            return frozenset(codepoints)

        font = TTFont(font_path, lazy=True)
        try:
            cmap = font.getBestCmap() or {}
            return frozenset(cmap.keys())
        finally:
            font.close()
    except Exception:
        return frozenset()


def _font_supports_codepoint(font_name: str, codepoint: int) -> bool:
    font_path = _resolve_font_path(font_name)
    if not font_path:
        return False
    return codepoint in _load_font_codepoints(font_path)


def _select_font_for_char(ch: str, fonts: Sequence[str], current_font: Optional[str]) -> str:
    if not fonts:
        return current_font or ''

    if _is_neutral_char(ch):
        return current_font or fonts[0]

    codepoint = ord(ch)
    for font_name in fonts:
        if _font_supports_codepoint(font_name, codepoint):
            return font_name

    return fonts[0]


def _split_runs(text: str, fonts: Sequence[str]) -> List[Tuple[str, str]]:
    runs: List[Tuple[str, str]] = []
    current_font: Optional[str] = None
    buffer: List[str] = []

    for ch in text:
        next_font = _select_font_for_char(ch, fonts, current_font)
        if current_font is None:
            current_font = next_font

        if next_font != current_font:
            runs.append((current_font, ''.join(buffer)))
            buffer = [ch]
            current_font = next_font
        else:
            buffer.append(ch)

    if buffer:
        runs.append((current_font or fonts[0], ''.join(buffer)))

    return runs


def apply_fallback_markup(text: str,
                          primary_font: str,
                          fallback_fonts: Optional[Iterable[str]] = None,
                          enabled: bool = True,
                          wrap_primary: bool = False,
                          base_font_size: Optional[float] = None,
                          font_scales: Optional[dict] = None) -> str:
    escaped = escape_kivy_markup(text)
    if not text:
        return escaped

    # When fallback is disabled but wrap_primary is True, still wrap with primary font
    if not enabled:
        if wrap_primary:
            return f'[font={primary_font}]{escaped}[/font]'
        return escaped

    fallback_list = [font for font in (fallback_fonts or []) if font]
    fonts = [primary_font] + [font for font in fallback_list if font != primary_font]

    if not fonts:
        return escape_kivy_markup(text)

    runs = _split_runs(text, fonts)
    rendered: List[str] = []
    font_scales = font_scales or {}

    for font_name, run_text in runs:
        escaped = escape_kivy_markup(run_text)
        scale = font_scales.get(font_name, 1.0)
        size_tag = None
        if base_font_size and scale and scale != 1.0:
            size_value = max(1, int(round(base_font_size * float(scale))))
            size_tag = f'[size={size_value}]'

        if font_name == primary_font and not wrap_primary and not size_tag:
            rendered.append(escaped)
            continue

        prefix = ''
        suffix = ''
        if font_name == primary_font and not wrap_primary:
            prefix = ''
            suffix = ''
        else:
            prefix += f'[font={font_name}]'
            suffix = '[/font]' + suffix

        if size_tag:
            prefix += size_tag
            suffix = '[/size]' + suffix

        rendered.append(f'{prefix}{escaped}{suffix}')

    return ''.join(rendered)
