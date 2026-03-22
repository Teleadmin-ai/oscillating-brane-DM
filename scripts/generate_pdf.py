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
            "title": "Oscillating Brane Dark Matter Theory V8.0 — Hybrid Topology Edition",
            "author": "Romain Provencal",
            "date": datetime.now().strftime("%B %Y"),
            "subtitle": "The Cosmic Yoyo: A Vibrating 4D Membrane in 5D Anti-de Sitter Space",
        }
        self.chapter_count = 0

    # V8.0 Restructured chapter titles — eliminates all Frankenstein duplicates
    CHAPTER_TITLES = {
        "index.md": "The Cosmic Yoyo Theory",
        "discoveries.md": "Discovery & Correction of Modern Cosmology",
        "theory.md": "Complete Theoretical Framework",
        "chronology.md": "Cosmic Chronology: From Inflation to the Current Beat",
        "docs/foundations_parts/part1_mathematical_framework.md": "Mathematical Framework & Stability",
        "predictions.md": "Observational Predictions & Experimental Tests",
        "docs/foundations_parts/part2_comparative_predictions.md": "Comparative Analysis & Falsifiability",
        "docs/foundations_parts/part3_current_limitations.md": "Current Limitations & Theoretical Challenges",
        "docs/foundations_parts/part4_development_roadmap.md": "Computational Tools, Roadmap & References",
    }

    def find_markdown_files(self) -> List[Tuple[Path, Dict]]:
        """Find markdown files for the 8-chapter V8.0 structure (no duplicates).

        Eliminated files (absorbed into canonical chapters):
        - about.md → acknowledgments in preface
        - tools.md → absorbed into Ch 8 (part4_development_roadmap)
        - docs/theory_v4_complete.md → duplicates theory.md
        - docs/theoretical_foundations.md → duplicates theory.md + part1
        - docs/observational_tests.md → duplicates predictions.md
        - All _posts/*.md → duplicate various chapters
        """
        files = []

        # V8.0 curated file list — 8 chapters, zero duplication
        doc_order = [
            "index.md",  # Frontmatter / Introduction
            "discoveries.md",  # Ch 1: Discovery & Correction
            "theory.md",  # Ch 2: Theoretical Framework (canonical)
            "chronology.md",  # Ch 3: Cosmic Chronology
            "docs/foundations_parts/part1_mathematical_framework.md",  # Ch 4: Math Framework & Stability
            "predictions.md",  # Ch 5: Predictions & Tests
            "docs/foundations_parts/part2_comparative_predictions.md",  # Ch 6: Comparative & Falsifiability
            "docs/foundations_parts/part3_current_limitations.md",  # Ch 7: Limitations & Challenges
            "docs/foundations_parts/part4_development_roadmap.md",  # Ch 8: Tools, Roadmap & References
        ]

        for doc in doc_order:
            path = self.base_dir / doc
            if path.exists():
                front_matter = self.extract_front_matter(path)
                # Override title with V8.0 restructured chapter title
                if doc in self.CHAPTER_TITLES:
                    front_matter["title"] = self.CHAPTER_TITLES[doc]
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

**Version 8.0 --- Hybrid Topology Edition (March 2026)**

The Universe is a vibrating 4D membrane in 5D Anti-de Sitter space, driven by a hybrid stick-slip motor: macroscopic Cosmic Web forcing via Israel junction conditions (the muscle) + microscopic ER=EPR-entangled PBH network for quantum synchronization (the metronome).

**Key Parameters:**

| Parameter | Value |
|-----------|-------|
| Brane tension $\\tau_0$ | $7.0 \\times 10^{{19}}$ J/m$^2$ = 0.017 GeV$^3$ |
| Energy scale $\\tau_0^{{1/3}}$ | 257 MeV $\\approx \\Lambda_{{QCD}}$ |
| Period $T$ | 2.0 $\\pm$ 0.3 Gyr |
| Phase $\\phi_0$ | $\\pi/2$ |
| Extra dimension $L$ | 0.2 $\\mu$m |
| PBH mass function | $10^{{-14}}$ to $10^{{-10}}$ $M_\\odot$ (log-normal) |
| Fresnel parameter | $w_F \\approx 0.03 \\ll 1$ |

**Three anomalies resolved:** DESI phantom crossing, $S_8$ tension (scale-dependent Yukawa), Planck ISW ($\\Delta\\chi^2 = 32.9$, $6\\sigma$). **Definitive future test:** SKA 21 cm reionization modulation (2027+).

*Human-AI collaboration: Romain Provencal (conceptual architect) with Claude (Anthropic) and Gemini DeepThink (Google) as mathematical co-processors.*

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

    def generate_pdf_direct(self, output_path: Path) -> bool:
        """Generate PDF directly using pandoc with all content."""
        # Create combined markdown
        combined_md = self.create_combined_markdown()

        # Save intermediate markdown
        temp_md = output_path.with_suffix(".combined.md")
        with open(temp_md, "w", encoding="utf-8") as f:
            f.write(combined_md)

        print(f"\nCombined markdown saved to: {temp_md}")
        print(f"  Size: {len(combined_md)} bytes ({len(combined_md)/1024:.1f} KB)")

        # Generate PDF using multiple attempts with different engines
        # xelatex first — source files contain Unicode (Greek letters, symbols)
        # that pdflatex cannot handle without heavy preprocessing
        engines = [
            (
                "xelatex",
                ["--pdf-engine=xelatex", "--pdf-engine-opt=-interaction=nonstopmode"],
            ),
            (
                "lualatex",
                ["--pdf-engine=lualatex", "--pdf-engine-opt=-interaction=nonstopmode"],
            ),
            (
                "pdflatex",
                ["--pdf-engine=pdflatex", "--pdf-engine-opt=-interaction=nonstopmode"],
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
        # Copy to latest versions
        latest_path = output_dir / "oscillating_brane_theory_latest.pdf"
        shutil.copy2(output_path, latest_path)
        print(f"\nLatest version copied to: {latest_path}")

        # Copy to root directory
        root_pdf_path = base_dir / "oscillating_brane_theory_latest.pdf"
        shutil.copy2(output_path, root_pdf_path)
        print(f"PDF copied to root for website: {root_pdf_path}")

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
