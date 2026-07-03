#!/usr/bin/env python3
"""
Generate a comprehensive PDF document from all markdown files.
This version properly handles math expressions and generates a complete PDF.
"""

import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import pypandoc
import yaml


class FinalPDFGenerator:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.metadata = {
            "title": "Oscillating Brane Dark Matter Theory - Complete Documentation",
            "author": "Romain Provencal",
            "date": datetime.now().strftime("%B %Y"),
            "subtitle": "The Universe as a Vibrating Membrane",
        }
        self.chapter_count = 0

    def find_markdown_files(self) -> List[Tuple[Path, Dict]]:
        """Find all markdown files and extract their front matter."""
        files = []

        # V8.2 structure — site pages + technical docs, no duplicates
        # Each entry = a page on the site = a chapter in the PDF
        doc_order = [
            "index.md",  # Ch 1: Home / Introduction
            "discoveries.md",  # Ch 2: Discovery & Correction
            "theory.md",  # Ch 3: Complete Theoretical Framework
            "chronology.md",  # Ch 4: Cosmic Chronology
            "predictions.md",  # Ch 5: Observational Predictions
            "laboratory.md",  # Ch 6: Laboratory Proofs
            "tools.md",  # Ch 7: Computational Tools
            "docs/theoretical_foundations.md",  # Appendix A: Simplified 4D EFT (Linearized Toy Model)
        ]

        for doc in doc_order:
            path = self.base_dir / doc
            if path.exists():
                front_matter = self.extract_front_matter(path)
                files.append((path, front_matter))

        return files

    def extract_front_matter(self, file_path: Path) -> Dict:
        """Extract YAML front matter from markdown file."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Match YAML front matter
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except:
                return {}
        return {}

    def fix_math_expressions(self, content: str) -> str:
        """Fix common math expression issues."""
        # Fix patterns where math expressions are split or malformed

        # Fix underscore issues in math mode (replace with proper subscript)
        content = re.sub(r"\\_", "_", content)

        # Fix incomplete fractions
        content = re.sub(
            r"\\frac\{([^}]+)\}\{([^}]*)\s*$",
            r"\\frac{\1}{\2}",
            content,
            flags=re.MULTILINE,
        )

        # Fix split math expressions like $\delta$$\tau$ -> $\delta\tau$
        content = re.sub(r"\$([^$]+)\$\$([^$]+)\$", r"$\1\2$", content)

        # Fix math expressions that have escaped underscores
        content = re.sub(r"\\\_([0-9a-zA-Z])", r"_\1", content)

        # Fix specific problematic patterns found in the error
        content = content.replace("$$\\Pi", "$$\\Pi")
        content = content.replace("\\dot{N}_i", "\\dot{N}_i")
        content = content.replace("m_{MN}", "m_{MN}")

        # Ensure math blocks are properly closed
        # Count $$ and ensure they're paired
        parts = content.split("$$")
        if len(parts) % 2 == 0:  # Odd number of $$, missing closing
            # Find the last unclosed $$ and close it
            content = content + "$$"

        return content

    def process_markdown(self, file_path: Path, front_matter: Dict) -> str:
        """Process a markdown file for inclusion in the PDF."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove front matter
        content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)

        # First, protect math expressions from Unicode conversion
        math_blocks = []

        # Extract display math blocks $$...$$
        def save_display_math(match):
            idx = len(math_blocks)
            math_blocks.append(match.group(0))
            return f"MATHBLOCK{idx}MATHBLOCK"

        content = re.sub(r"\$\$[^$]+\$\$", save_display_math, content, flags=re.DOTALL)

        # Extract inline math $...$
        def save_inline_math(match):
            idx = len(math_blocks)
            math_blocks.append(match.group(0))
            return f"MATHBLOCK{idx}MATHBLOCK"

        content = re.sub(r"\$[^$\n]+\$", save_inline_math, content)

        # Now do Unicode replacements on non-math content
        unicode_replacements = {
            # Greek letters outside math
            "τ": "tau",
            "σ": "sigma",
            "ρ": "rho",
            "π": "pi",
            "μ": "mu",
            "λ": "lambda",
            "η": "eta",
            "δ": "delta",
            "γ": "gamma",
            "ω": "omega",
            "φ": "phi",
            "χ": "chi",
            "ξ": "xi",
            "Δ": "Delta",
            "Ω": "Omega",
            # Ligatures
            "ﬀ": "ff",
            "ﬁ": "fi",
            "ﬂ": "fl",
            "ﬃ": "ffi",
            "ﬄ": "ffl",
            "ï": "i",
            # Symbols
            "∞": "infinity",
            "≈": "approximately",
            "≤": "<=",
            "≥": ">=",
            "≪": "<<",
            "≫": ">>",
            "∝": "proportional to",
            # Emojis
            "🌌": "[universe]",
            "📥": "[download]",
            "✓": "[check]",
            "☉": "Sun",
            "🤖": "[AI]",
            # Special characters
            "—": "---",
            "–": "--",
            "'": "'",
            "'": "'",
            """: '"',
            """: '"',
            "…": "...",
            "•": "*",
            "×": "x",
            "±": "+/-",
        }

        for old, new in unicode_replacements.items():
            content = content.replace(old, new)

        # Restore math blocks
        for idx, math_block in enumerate(math_blocks):
            # Fix the math block before restoring
            fixed_math = self.fix_math_expressions(math_block)
            content = content.replace(f"MATHBLOCK{idx}MATHBLOCK", fixed_math)

        # Fix image paths
        content = re.sub(
            r"!\[([^\]]*)\]\((/[^)]+)\)",
            lambda m: f"![{m.group(1)}]({self.base_dir}{m.group(2)})",
            content,
        )

        # Fix Jekyll image paths
        content = re.sub(
            r'!\[([^\]]*)\]\({{\s*["\']?/?([^}"\']+)["\']?\s*\|\s*relative_url\s*}}\)',
            lambda m: f"![{m.group(1)}]({self.base_dir}/{m.group(2)})",
            content,
        )

        # Get title and create chapter heading
        title = front_matter.get("title", file_path.stem.replace("_", " ").title())

        # Appendix detection: theoretical_foundations.md is Appendix A, not a chapter
        is_appendix = "theoretical_foundations" in str(file_path)
        if is_appendix:
            heading = "# Appendix A: Simplified 4D EFT (Linearized Toy Model)"
        else:
            self.chapter_count += 1
            heading = f"# Chapter {self.chapter_count}: {title}"

        if "_posts" in str(file_path):
            date = front_matter.get("date", "")
            if date:
                heading += f"\n\n*Date: {date}*"

        description = front_matter.get("description", "")
        if description:
            heading += f"\n\n*{description.strip()}*"

        # Remove existing top-level heading if present
        if content.strip().startswith("# "):
            lines = content.split("\n")
            content = "\n".join(lines[1:])

        # Fix section numbering conflicts
        # Remove "Chapter X:" prefixes if they exist (e.g., "# Chapter 4: Title" -> "# Title")
        content = re.sub(
            r"^(#)\s*Chapter\s+\d+:\s*(.*)$", r"\1 \2", content, flags=re.MULTILINE
        )

        # Handle deeper subsections first (e.g., "#### 4.1.1 Details" -> "#### Details")
        content = re.sub(
            r"^(#{2,6})\s*\d+\.\d+\.\d+\.?\s+(.*)$",
            r"\1 \2",
            content,
            flags=re.MULTILINE,
        )

        # Handle subsection numbering (e.g., "### 4.1 Model Comparison" -> "### Model Comparison")
        content = re.sub(
            r"^(#{2,6})\s*\d+\.\d+\.?\s+(.*)$", r"\1 \2", content, flags=re.MULTILINE
        )

        # Remove numbered sections (e.g., "## 4. Comparative Analysis" or "## 4 Comparative Analysis" -> "## Comparative Analysis")
        content = re.sub(
            r"^(#{2,6})\s*\d+\.?\s+(.*)$", r"\1 \2", content, flags=re.MULTILINE
        )

        return heading + "\n\n" + content + "\n\n\\newpage\n\n"

    def create_combined_markdown(self) -> str:
        """Combine all markdown files into a single document."""
        files = self.find_markdown_files()

        # Create header with proper LaTeX setup
        header = f"""---
title: "{self.metadata['title']}"
author: "{self.metadata['author']}"
date: "{self.metadata['date']}"
subtitle: "{self.metadata['subtitle']}"
documentclass: report
papersize: a4
fontsize: 11pt
geometry: margin=1in
toc: true
toc-depth: 2
numbersections: false
colorlinks: true
linkcolor: black
urlcolor: blue
header-includes:
  - \\usepackage{{amsmath}}
  - \\usepackage{{amssymb}}
  - \\usepackage{{amsthm}}
  - \\usepackage{{graphicx}}
  - \\usepackage{{hyperref}}
  - \\usepackage{{float}}
  - \\usepackage{{longtable}}
  - \\usepackage{{booktabs}}
  - \\usepackage[T1]{{fontenc}}
  - \\usepackage[utf8]{{inputenc}}
  - \\usepackage{{lmodern}}
---

\\newpage

# Preface

This document contains the complete theoretical framework and documentation for the Oscillating Brane Dark Matter Theory, where the universe is conceptualized as a vibrating 4-dimensional membrane in 5D space.

**Key Parameters:**

- Brane tension: 7.0e19 J/m²
- Oscillation period: T = 2.0 Gyr (±0.3)
- Extra dimension size: L = 0.2 microns
- MOND acceleration: a0 = 1.1e-10 m/s²

The theory proposes that dark matter effects emerge from membrane oscillations excited by gravitational flows, naturally producing dark energy and MOND-like phenomena.

\\newpage

"""

        combined = header

        # Process each file
        print(f"\nProcessing {len(files)} files for complete PDF...")
        for file_path, front_matter in files:
            print(f"  Chapter {self.chapter_count + 1}: {file_path.name}")
            content = self.process_markdown(file_path, front_matter)
            combined += content

        print(f"\nTotal chapters: {self.chapter_count}")

        return combined

    @staticmethod
    def sanitize_unicode_for_latex(text: str) -> str:
        """Replace Unicode characters that pdflatex cannot render.

        pdflatex only supports ASCII + LaTeX commands. Unicode symbols
        in plain text (outside $..$ blocks) are silently dropped, causing
        missing minus signs, vanishing π, etc.  This pre-processor converts
        them to safe LaTeX equivalents *before* pandoc sees the content.

        We must NOT touch content already inside LaTeX math delimiters
        ($..$ or $$..$$) because those already use \pi, \times, etc.
        """
        # ── Map of Unicode chars → LaTeX-safe replacements ──
        # Greek letters (text context → inline math)
        replacements = {
            "π": r"$\pi$",
            "Λ": r"$\Lambda$",
            "Δ": r"$\Delta$",
            "Σ": r"$\Sigma$",
            "Ω": r"$\Omega$",
            "Γ": r"$\Gamma$",
            "Θ": r"$\Theta$",
            "α": r"$\alpha$",
            "β": r"$\beta$",
            "γ": r"$\gamma$",
            "δ": r"$\delta$",
            "ε": r"$\varepsilon$",
            "ζ": r"$\zeta$",
            "η": r"$\eta$",
            "θ": r"$\theta$",
            "κ": r"$\kappa$",
            "λ": r"$\lambda$",
            "μ": r"$\mu$",
            "ν": r"$\nu$",
            "ξ": r"$\\xi$",
            "ρ": r"$\rho$",
            "σ": r"$\sigma$",
            "τ": r"$\tau$",
            "φ": r"$\varphi$",
            "χ": r"$\chi$",
            "ψ": r"$\psi$",
            "ω": r"$\omega$",
            # Operators and symbols
            "×": r"$\times$",
            "≃": r"$\simeq$",
            "≈": r"$\approx$",
            "≥": r"$\geq$",
            "≤": r"$\leq$",
            "≫": r"$\gg$",
            "≪": r"$\ll$",
            "±": r"$\pm$",
            "∓": r"$\mp$",
            "→": r"$\to$",
            "←": r"$\leftarrow$",
            "↔": r"$\leftrightarrow$",
            "∞": r"$\infty$",
            "∝": r"$\propto$",
            "∼": r"$\sim$",
            "ℓ": r"$\ell$",
            "ℏ": r"$\hbar$",
            "ℒ": r"$\mathcal{L}$",
            "∂": r"$\partial$",
            # Typographic
            "—": "---",
            "–": "--",
            "\u2018": "`",  # left single quote
            "\u2019": "'",  # right single quote
            "\u201c": "``",  # left double quote
            "\u201d": "''",  # right double quote
            # Superscripts → LaTeX
            "⁰": r"$^{0}$",
            "¹": r"$^{1}$",
            "²": r"$^{2}$",
            "³": r"$^{3}$",
            "⁴": r"$^{4}$",
            "⁵": r"$^{5}$",
            "⁶": r"$^{6}$",
            "⁷": r"$^{7}$",
            "⁸": r"$^{8}$",
            "⁹": r"$^{9}$",
            "⁻": r"$^{-}$",
            "⁺": r"$^{+}$",
            # Subscripts → LaTeX
            "₀": r"$_{0}$",
            "₁": r"$_{1}$",
            "₂": r"$_{2}$",
            "₃": r"$_{3}$",
            "₄": r"$_{4}$",
            "₅": r"$_{5}$",
            "₆": r"$_{6}$",
            "₇": r"$_{7}$",
            "₈": r"$_{8}$",
            "₉": r"$_{9}$",
            # Fractions
            "⅓": r"$\frac{1}{3}$",
            "½": r"$\frac{1}{2}$",
            "¼": r"$\frac{1}{4}$",
            # Misc
            "Ḣ": r"$\dot{H}$",
        }

        # Split text into math and non-math segments.
        # We only replace in non-math segments.
        # Pattern: match $$...$$ (display) or $...$ (inline), non-greedy.
        math_pattern = re.compile(r"(\$\$[\s\S]*?\$\$|\$[^\$\n]+?\$)")
        segments = math_pattern.split(text)

        result = []
        for i, seg in enumerate(segments):
            if i % 2 == 1:
                # This is a math segment — leave untouched
                result.append(seg)
            else:
                # This is a text segment — apply replacements
                for uchar, latex in replacements.items():
                    seg = seg.replace(uchar, latex)
                # Collapse adjacent inline math: $^{-}$$^{1}$$^{7}$ → $^{-17}$
                seg = re.sub(
                    r"\$\^\{(-?)\}\$\$\^\{(\d)\}\$\$\^\{(\d)\}\$",
                    r"$^{\1\2\3}$",
                    seg,
                )
                seg = re.sub(
                    r"\$\^\{(-?)\}\$\$\^\{(\d)\}\$",
                    r"$^{\1\2}$",
                    seg,
                )
                seg = re.sub(
                    r"\$_\{(\d)\}\$\$_\{(\d)\}\$",
                    r"$_{\1\2}$",
                    seg,
                )
                result.append(seg)

        return "".join(result)

    @staticmethod
    def convert_html_tables_to_markdown(text: str) -> str:
        """Convert simple HTML tables to markdown tables for pandoc/pdflatex.

        Raw HTML <table> blocks render as garbage in pdflatex.
        This converts them to markdown pipe-tables that pandoc handles.
        """

        def _html_table_to_md(match):
            html = match.group(0)
            # Extract rows
            rows = re.findall(r"<tr>(.*?)</tr>", html, re.DOTALL)
            if not rows:
                return html  # Can't parse, leave as-is

            md_rows = []
            for row in rows:
                # Extract cells (td or th)
                cells = re.findall(r"<(?:td|th)[^>]*>(.*?)</(?:td|th)>", row, re.DOTALL)
                # Strip HTML tags inside cells but keep text
                clean_cells = []
                for cell in cells:
                    cell = re.sub(r"<strong>(.*?)</strong>", r"**\1**", cell)
                    cell = re.sub(r"<em>(.*?)</em>", r"*\1*", cell)
                    cell = re.sub(r"<sup>(.*?)</sup>", r"$^{\1}$", cell)
                    cell = re.sub(r"<sub>(.*?)</sub>", r"$_{\1}$", cell)
                    cell = re.sub(r"<[^>]+>", "", cell)  # strip remaining tags
                    cell = cell.strip()
                    clean_cells.append(cell)
                if clean_cells:
                    md_rows.append("| " + " | ".join(clean_cells) + " |")

            if not md_rows:
                return html

            # Add header separator after first row
            ncols = md_rows[0].count("|") - 1
            separator = "|" + "|".join(["---"] * ncols) + "|"
            result = md_rows[0] + "\n" + separator
            for row in md_rows[1:]:
                result += "\n" + row

            return "\n\n" + result + "\n\n"

        # Match <table>...</table> blocks (possibly with attributes)
        text = re.sub(
            r"<table[^>]*>.*?</table>",
            _html_table_to_md,
            text,
            flags=re.DOTALL,
        )

        # Strip standalone HTML block elements that pdflatex can't render
        text = re.sub(r'<div[^>]*class="[^"]*"[^>]*>\s*</div>', "", text)
        text = re.sub(r"</?div[^>]*>", "", text)
        text = re.sub(r"<h3[^>]*>(.*?)</h3>", r"### \1", text)
        text = re.sub(r"<p><em>(.*?)</em></p>", r"*\1*", text, flags=re.DOTALL)
        text = re.sub(r"<img[^>]*>", "", text)  # strip bare img tags
        text = re.sub(r"</?p[^>]*>", "", text)  # strip p tags

        # Strip Jekyll/Liquid template tags (they render as garbage in PDF)
        text = re.sub(r"\{%.*?%\}", "", text)
        text = re.sub(r"\{\{.*?\}\}", "", text)

        # Fix indented markdown headers (4+ spaces = code block in pandoc)
        text = re.sub(r"^[ \t]+(#{1,6}\s)", r"\1", text, flags=re.MULTILINE)

        # Strip emoji characters (they render as boxes or [?] in pdflatex)
        emoji_pattern = re.compile(
            "["
            "\U0001f300-\U0001f9ff"  # Misc Symbols, Emoticons, etc.
            "\U00002600-\U000027bf"  # Misc symbols
            "\U0001fa00-\U0001fa6f"
            "\U0001fa70-\U0001faff"
            "]+",
            flags=re.UNICODE,
        )
        text = emoji_pattern.sub("", text)
        # Strip emoji name artifacts like [universe], [rocket], etc.
        text = re.sub(
            r"\[(?:universe|rocket|star|warning|check|microscope|telescope)\]\s*",
            "",
            text,
        )

        return text

    @staticmethod
    def fix_pdflatex_ligatures(text: str) -> str:
        r"""Fix fi/fl ligature rendering issue in pdflatex Computer Modern.

        pdflatex with CM fonts sometimes mangles fi/fl ligatures.
        Insert a zero-width space via LaTeX to break the ligature
        and force correct rendering: fi → f{}i, fl → f{}l.
        Only applied outside math blocks.
        """
        math_pattern = re.compile(r"(\$\$[\s\S]*?\$\$|\$[^\$\n]+?\$)")
        segments = math_pattern.split(text)

        result = []
        for i, seg in enumerate(segments):
            if i % 2 == 1:
                result.append(seg)
            else:
                seg = seg.replace("fi", "f{}i")
                seg = seg.replace("fl", "f{}l")
                result.append(seg)

        return "".join(result)

    @staticmethod
    def polish_combined_markdown(text: str) -> str:
        """Clean up hybrid LaTeX/text artifacts for readable standalone .md.

        After Unicode sanitization, the combined markdown has artifacts like
        tau$_{0}$ (should be $\\tau_0$) and 10$^{1}$$^{9}$ (should be $10^{19}$).
        This pass merges them into clean inline LaTeX.
        """

        # ── Merge adjacent inline math blocks ──
        # 10$^{1}$$^{9}$ → $10^{19}$  (split superscripts from Unicode digits)
        # Pattern: digit(s)$^{X}$$^{Y}$... → $digit^{XY...}$
        def merge_superscripts(m):
            prefix = m.group(1)  # e.g. "10" or ""
            exponents = re.findall(r"\^\{([^}]*)\}", m.group(0))
            merged = "".join(exponents)
            return f"${prefix}^{{{merged}}}$"

        text = re.sub(
            r"(\d*)\$\^\{[^}]*\}\$(?:\$\^\{[^}]*\}\$)+",
            merge_superscripts,
            text,
        )

        # Same for subscripts: X$_{0}$$_{8}$ → $X_{08}$
        def merge_subscripts(m):
            prefix = m.group(1)
            subs = re.findall(r"_\{([^}]*)\}", m.group(0))
            merged = "".join(subs)
            return f"${prefix}_{{{merged}}}$"

        text = re.sub(
            r"(\w*)\$_\{[^}]*\}\$(?:\$_\{[^}]*\}\$)+",
            merge_subscripts,
            text,
        )

        # ── Fix hybrid text+math patterns (protect display math blocks) ──
        hybrid_fixes = [
            (r"\btau\$_\{0\}\$", r"$\\tau_0$"),
            (r"\btau\$_\{BB\}\$", r"$\\tau_{BB}$"),
            (r"\bphi\$_\{crit\}\$", r"$\\phi_{crit}$"),
            (r"\bphi\$_\{0\}\$", r"$\\phi_0$"),
            (r"E_mu\$\\nu\$", r"$E_{\\mu\\nu}$"),
            (r"S_mu\$\\nu\$", r"$S_{\\mu\\nu}$"),
            (r"K_mu\$\\nu\$", r"$K_{\\mu\\nu}$"),
            (r"h_mu\$\\nu\$", r"$h_{\\mu\\nu}$"),
            (r"T\^mu_mu", r"$T^\\mu_\\mu$"),
            (r"\$\\Lambda\$_QCD", r"$\\Lambda_{QCD}$"),
            (r"\$\\Lambda\$CDM", r"$\\Lambda$CDM"),
            (r"(?<!\$)Deltaln K", r"$\\Delta\\ln K$"),
            (r"(?<!\$)Deltachi\b", r"$\\Delta\\chi$"),
            (r"\bchi\$\^\{2\}\$", r"$\\chi^2$"),
            (r"(?<!\$)Delta\$\\beta\$", r"$\\Delta\\beta$"),
        ]
        # Apply only outside display math $$...$$ blocks
        display_math = re.compile(r"(\$\$[\s\S]*?\$\$)")
        segments = display_math.split(text)
        result_segs = []
        for i, seg in enumerate(segments):
            if i % 2 == 1:
                result_segs.append(seg)  # display math — untouched
            else:
                for pattern, replacement in hybrid_fixes:
                    seg = re.sub(pattern, replacement, seg)
                result_segs.append(seg)
        text = "".join(result_segs)

        # ── Fix image paths for standalone readability ──
        # /root/bulk/.../plots/xxx.png → ./plots/xxx.png
        text = re.sub(r"!\[([^\]]*)\]\(/root/[^)]*?/plots/", r"![\1](./plots/", text)
        # /plots/xxx.png → ./plots/xxx.png
        text = re.sub(r"!\[([^\]]*)\]\(/plots/", r"![\1](./plots/", text)
        # HTML img tags
        text = re.sub(r'src="/root/[^"]*?/plots/', 'src="./plots/', text)
        text = re.sub(r'src="/plots/', 'src="./plots/', text)

        # ── Strip residual HTML block elements ──
        text = re.sub(r"<article[^>]*>.*?</article>", "", text, flags=re.DOTALL)
        text = re.sub(r"<time[^>]*>.*?</time>", "", text, flags=re.DOTALL)
        text = re.sub(r'<h2\s+style="[^"]*"[^>]*>(.*?)</h2>', r"## \1", text)
        text = re.sub(r"<span[^>]*>(.*?)</span>", r"\1", text)

        # ── Clean up multiple blank lines ──
        text = re.sub(r"\n{4,}", "\n\n\n", text)

        return text

    @staticmethod
    def cleanup_md_txt(text: str) -> str:
        """Post-process the .md.txt for AI/text-parser readability.

        This runs ONLY on the .md.txt copy (not on the content fed to
        pandoc/xelatex). It fixes cosmetic scories created by the
        sanitize_unicode_for_latex pass on plain-text sections.

        SAFETY: only targets patterns that are unambiguously broken
        formatting — never modifies content inside $$...$$ display math.
        All replacements use str.replace (exact match) to avoid regex
        side effects on valid LaTeX.
        """
        # ── 1. CRASH-LEVEL: Unicode diacritics that break LaTeX ──
        # phï (phi + diaeresis) → ddot{phi} — WILL crash xelatex
        text = text.replace("(ph\u00ef >> 0)", r"($\ddot{\phi} \gg 0$)")
        text = text.replace("ph\u00ef", r"$\ddot{\phi}$")
        # phi̇ (phi + combining dot above U+0307)
        text = text.replace("3Hphi\u0307", r"$3H\dot{\phi}$")
        text = text.replace("phi\u0307", r"$\dot{\phi}$")

        # ── 2. Broken motor equation symbols (plain text → inline math) ──
        text = text.replace(
            "**(3H + $\\Gamma$_rad)$\\dot{\\phi}$**",
            "**$(3H + \\Gamma_{rad})\\dot{\\phi}$**",
        )
        text = text.replace(
            "**R_PBH($\\dot{\\phi}$,$\\dot{\\phi}$)"
            "\u00b7$\\Theta$(|$\\dot{\\phi}$| - $\\dot{\\phi}$_crit)**",
            "**$\\mathcal{R}_{PBH}(\\phi, \\dot{\\phi})\\,"
            "\\Theta(|\\phi| - \\phi_{crit})$**",
        )
        text = text.replace("$\\Gamma$_rad", "$\\Gamma_{rad}$")
        text = text.replace("(xiRphi)", "($\\xi R\\phi$)")
        text = text.replace("**xiRphi**", "**$\\xi R\\phi$**")
        text = text.replace("xiRphi", "$\\xi R\\phi$")
        text = text.replace(
            "**$\\partial$V_GW/$\\partial$$\\dot{\\phi}$**",
            "**$\\frac{\\partial V_{GW}}{\\partial \\phi}$**",
        )

        # ── 3. Split-subscript scories: X$_{n}$ → $X_n$ ──
        text = re.sub(r"S\$_\{8\}\$", "$S_8$", text)
        text = re.sub(r"a\$_\{0\}\$", "$a_0$", text)
        text = re.sub(r"H\$_\{0\}\$", "$H_0$", text)
        text = re.sub(r"f\$_\{0\}\$", "$f_0$", text)
        text = re.sub(r"Q\$_\{(\d)\}\$", r"$Q_\1$", text)
        # Generic: any single letter followed by $_{X}$ pattern
        text = re.sub(r"(\w)\$_\{([^}]+)\}\$", r"$\1_{\2}$", text)

        # ── 4. Plain-text units and parameters ──
        text = text.replace("0.2 mum", "$0.2\\,\\mu$m")
        text = text.replace("25 mum", "25 $\\mu$m")
        text = text.replace("0.2 microns", "$0.2\\,\\mu$m")

        # ── 5. Leftover 1 eV vestiges ──
        text = text.replace("m_KK $\\simeq$ 1 eV", "$m_{KK} \\approx 3.78$ eV")
        text = text.replace("DeltaN_eff ~ 0.01", "$\\Delta N_{eff} \\sim 0.01$")
        text = text.replace(
            "Omega_c, sigma_v, m_chi",
            "$\\Omega_c$, $\\sigma_v$, $m_\\chi$",
        )

        # ── 6. Broken ell mode references ──
        text = text.replace("($\\ell$=0 mode)", "($\\ell=0$ mode)")
        text = text.replace("($\\ell$=0)", "($\\ell=0$)")

        # ── 7. Broken table entries ──
        text = text.replace(
            "DeltaC_$\\ell$/C_$\\ell$",
            "$\\Delta C_\\ell / C_\\ell$",
        )

        # ── 8. Plain-text physics variables (BBN, chronology, predictions) ──
        text = text.replace("w_eff = 1/3", "$w_{eff} = 1/3$")
        text = text.replace("w_eff $\\to$ 0", "$w_{eff} \\to 0$")
        text = text.replace("(1 - 3w_eff) = 0", "$(1 - 3w_{eff}) = 0$")
        text = text.replace("t_stick + t_slip", "$t_{stick} + t_{slip}$")
        text = text.replace("M_DM,tot", "$M_{DM,tot}$")
        text = text.replace("sigma_M approximately 1.5", "$\\sigma_M \\approx 1.5$")

        # ── 9. Broken exponent patterns in tables/text ──
        text = text.replace("v$^{4}$", "$v^4$")
        text = text.replace(
            "$v^4$ proportional to M_b",
            "$v^4 \\propto M_b$",
        )
        text = text.replace(
            "(rho proportional to r$^{-1}$)",
            "($\\rho \\propto r^{-1}$)",
        )
        text = text.replace(
            "sigma < 10$^{-48}$ cm$^{2}$",
            "$\\sigma < 10^{-48}$ cm$^2$",
        )

        # ── 10. Sigma notation in predictions ──
        for n in ["4", "5", "6", "3"]:
            text = text.replace(f"{n}sigma", f"${n}\\sigma$")

        # ── 11. Code block LaTeX cleanup ($ inside ``` blocks) ──
        text = text.replace("ds$^{2}$", "ds^2")
        text = text.replace("(J/m$^{2}$)", "(J/m^2)")
        text = text.replace("(J/m$^{3}$)", "(J/m^3)")

        # ── 12. Merge adjacent $...$ blocks created by sanitizer ──
        # e.g. $7.0$ $\times$ $10^{19}$ → $7.0 \times 10^{19}$
        # Only merge when separated by exactly one space
        text = re.sub(r"\$([^$]+)\$ \$([^$]+)\$", r"$\1 \2$", text)

        return text

    def generate_pdf_direct(self, output_path: Path) -> bool:
        """Generate PDF directly using pandoc with all content."""
        # Create combined markdown
        combined_md = self.create_combined_markdown()

        # Pipeline: sanitize Unicode → convert HTML → polish artifacts
        combined_md = self.sanitize_unicode_for_latex(combined_md)
        combined_md = self.convert_html_tables_to_markdown(combined_md)
        combined_md = self.polish_combined_markdown(combined_md)
        print(
            f"\n  Pre-processed: Unicode sanitized, HTML converted, markdown polished"
        )

        # Save intermediate markdown
        temp_md = output_path.with_suffix(".combined.md")
        with open(temp_md, "w", encoding="utf-8") as f:
            f.write(combined_md)

        print(f"\nCombined markdown saved to: {temp_md}")
        print(f"  Size: {len(combined_md)} bytes ({len(combined_md)/1024:.1f} KB)")

        # Generate PDF using multiple attempts with different engines
        engines = [
            (
                "pdflatex",
                ["--pdf-engine=pdflatex", "--pdf-engine-opt=-interaction=nonstopmode"],
            ),
            (
                "xelatex",
                ["--pdf-engine=xelatex", "--pdf-engine-opt=-interaction=nonstopmode"],
            ),
            (
                "lualatex",
                ["--pdf-engine=lualatex", "--pdf-engine-opt=-interaction=nonstopmode"],
            ),
        ]

        for engine_name, engine_args in engines:
            print(f"\nTrying PDF generation with {engine_name}...")
            try:
                # Create PDF using pandoc
                pypandoc.convert_file(
                    str(temp_md),
                    "pdf",
                    outputfile=str(output_path),
                    extra_args=[
                        *engine_args,
                        "--highlight-style=tango",
                        "--top-level-division=chapter",
                        "--template=default",
                    ],
                )

                if output_path.exists():
                    size = output_path.stat().st_size
                    print(f"\nSuccess with {engine_name}!")
                    print(f"  Generated: {output_path.name}")
                    print(f"  Size: {size/1024/1024:.1f} MB")
                    print(f"  Chapters: {self.chapter_count}")
                    return True

            except Exception as e:
                print(f"  Error with {engine_name}: {str(e)[:200]}...")
                continue

        return False

    def generate_pdf_parts_then_merge(self, output_path: Path) -> bool:
        """Alternative: Generate PDF in parts then merge."""
        print("\nTrying multi-part generation approach...")

        files = self.find_markdown_files()
        part_pdfs = []

        # Split into 3 parts
        parts = [
            ("Core Documentation", files[:6]),
            ("Technical Documentation", files[6:11]),
            ("Blog Posts", files[11:]),
        ]

        for part_name, part_files in parts:
            if not part_files:
                continue

            print(f"\nGenerating {part_name}...")
            part_md = self.create_part_markdown(part_files, part_name)

            # Save part markdown
            part_path = output_path.parent / f"part_{len(part_pdfs) + 1}.md"
            with open(part_path, "w", encoding="utf-8") as f:
                f.write(part_md)

            # Generate part PDF
            part_pdf = part_path.with_suffix(".pdf")
            try:
                pypandoc.convert_file(
                    str(part_path),
                    "pdf",
                    outputfile=str(part_pdf),
                    extra_args=[
                        "--pdf-engine=pdflatex",
                        "--pdf-engine-opt=-interaction=nonstopmode",
                        "--highlight-style=tango",
                    ],
                )

                if part_pdf.exists():
                    print(f"  Generated: {part_pdf.name}")
                    part_pdfs.append(part_pdf)
            except Exception as e:
                print(f"  Error: {e}")

        # Merge PDFs if we have multiple parts
        if len(part_pdfs) > 1:
            print("\nMerging PDF parts...")
            try:
                # Try pdfunite first
                cmd = ["pdfunite"] + [str(p) for p in part_pdfs] + [str(output_path)]
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0 and output_path.exists():
                    print("  Success with pdfunite!")
                    # Clean up parts
                    for p in part_pdfs:
                        p.unlink()
                    return True

            except Exception as e:
                print(f"  pdfunite failed: {e}")

        elif len(part_pdfs) == 1:
            # Just one part, rename it
            shutil.move(str(part_pdfs[0]), str(output_path))
            return True

        return False

    def create_part_markdown(
        self, files: List[Tuple[Path, Dict]], part_name: str
    ) -> str:
        """Create markdown for a part of the document."""
        header = f"""---
title: "{self.metadata['title']} - {part_name}"
author: "{self.metadata['author']}"
date: "{self.metadata['date']}"
documentclass: report
papersize: a4
fontsize: 11pt
geometry: margin=1in
numbersections: true
colorlinks: true
linkcolor: black
urlcolor: blue
---

"""

        content = header
        for file_path, front_matter in files:
            processed = self.process_markdown(file_path, front_matter)
            content += processed

        return content


def main():
    """Main entry point."""
    # Get the base directory
    base_dir = Path(__file__).parent.parent

    # Create output directory
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"oscillating_brane_theory_{timestamp}.pdf"

    # Create generator
    generator = FinalPDFGenerator(base_dir)

    # Try direct generation first
    success = generator.generate_pdf_direct(output_path)

    # If that fails, try the multi-part approach
    if not success:
        generator.chapter_count = 0  # Reset counter
        success = generator.generate_pdf_parts_then_merge(output_path)

    if success and output_path.exists():
        # Compress PDF with Ghostscript (convert bitmap images to JPEG)
        compressed_path = output_path.with_suffix(".compressed.pdf")
        try:
            gs_cmd = [
                "gs",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.5",
                "-dNOPAUSE",
                "-dBATCH",
                "-dQUIET",
                "-dDownsampleColorImages=true",
                "-dDownsampleGrayImages=true",
                "-dColorImageResolution=200",
                "-dGrayImageResolution=200",
                "-dColorImageDownsampleType=/Bicubic",
                "-dAutoFilterColorImages=false",
                "-dColorImageFilter=/DCTEncode",
                f"-sOutputFile={compressed_path}",
                str(output_path),
            ]
            result = subprocess.run(gs_cmd, capture_output=True, text=True)
            if result.returncode == 0 and compressed_path.exists():
                size_before = output_path.stat().st_size
                size_after = compressed_path.stat().st_size
                shutil.move(str(compressed_path), str(output_path))
                print(
                    f"\nPDF compressed: {size_before/1024/1024:.1f} MB"
                    f" -> {size_after/1024/1024:.1f} MB"
                    f" ({size_after/size_before*100:.0f}%)"
                )
            else:
                print(f"\nGhostscript compression skipped (gs not available)")
        except FileNotFoundError:
            print(f"\nGhostscript not installed, skipping compression")

        # Copy to latest versions
        latest_path = output_dir / "oscillating_brane_theory_latest.pdf"
        shutil.copy2(output_path, latest_path)
        print(f"\nLatest version copied to: {latest_path}")

        # Copy to root directory
        root_pdf_path = base_dir / "oscillating_brane_theory_latest.pdf"
        shutil.copy2(output_path, root_pdf_path)
        print(f"PDF copied to root for website: {root_pdf_path}")

        # Copy combined markdown to latest + root (as .txt for Jekyll compatibility)
        combined_md_path = output_path.with_suffix(".combined.md")
        if combined_md_path.exists():
            latest_md = output_dir / "oscillating_brane_theory_latest.combined.md"
            root_md = base_dir / "oscillating_brane_theory_latest.md.txt"
            shutil.copy2(combined_md_path, latest_md)

            # Post-process the .md.txt for AI/text readability
            # (fixes cosmetic scories from unicode sanitization on plain-text sections)
            with open(combined_md_path, "r", encoding="utf-8") as f:
                md_txt_content = f.read()
            md_txt_content = generator.cleanup_md_txt(md_txt_content)
            with open(root_md, "w", encoding="utf-8") as f:
                f.write(md_txt_content)
            print(f"Combined markdown copied to: {root_md} (post-processed)")

        print(f"\nPDF generation complete!")
        print(f"Total chapters: {generator.chapter_count}")
    else:
        print("\nPDF generation failed!")
        print("Please check that you have one of these installed:")
        print("  - pdflatex (texlive-latex-base)")
        print("  - xelatex (texlive-xetex)")
        print("  - lualatex (texlive-luatex)")


if __name__ == "__main__":
    main()
