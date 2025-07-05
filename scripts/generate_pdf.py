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

        # Main documentation files (in order)
        doc_order = [
            "index.md",
            "theory.md",
            "chronology.md",
            "predictions.md",
            "tools.md",
            "about.md",
            # Technical docs
            "docs/theory_v4_complete.md",
            # Split foundation files
            "docs/foundations_parts/part1_mathematical_framework.md",
            "docs/foundations_parts/part2_comparative_predictions.md",
            "docs/foundations_parts/part3_current_limitations.md",
            "docs/foundations_parts/part4_development_roadmap.md",
        ]

        # Add ordered docs first
        for doc in doc_order:
            path = self.base_dir / doc
            if path.exists():
                front_matter = self.extract_front_matter(path)
                files.append((path, front_matter))

        # Add blog posts
        posts_dir = self.base_dir / "_posts"
        if posts_dir.exists():
            posts = sorted(posts_dir.glob("*.md"), reverse=True)
            for post in posts:
                front_matter = self.extract_front_matter(post)
                files.append((post, front_matter))

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
        content = re.sub(r'^(#)\s*Chapter\s+\d+:\s*(.*)$', r'\1 \2', content, flags=re.MULTILINE)
        
        # Handle deeper subsections first (e.g., "#### 4.1.1 Details" -> "#### Details")
        content = re.sub(r'^(#{2,6})\s*\d+\.\d+\.\d+\.?\s+(.*)$', r'\1 \2', content, flags=re.MULTILINE)
        
        # Handle subsection numbering (e.g., "### 4.1 Model Comparison" -> "### Model Comparison")
        content = re.sub(r'^(#{2,6})\s*\d+\.\d+\.?\s+(.*)$', r'\1 \2', content, flags=re.MULTILINE)
        
        # Remove numbered sections (e.g., "## 4. Comparative Analysis" or "## 4 Comparative Analysis" -> "## Comparative Analysis")
        content = re.sub(r'^(#{2,6})\s*\d+\.?\s+(.*)$', r'\1 \2', content, flags=re.MULTILINE)

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

- Brane tension: $\\tau_0 = 7.0 \\times 10^{19}$ J/m$^2$
- Oscillation period: T = $2.0 \\pm 0.3$ Gyr
- Extra dimension size: L = 0.2 $\\mu$m
- MOND acceleration: $a_0 = 1.1 \\times 10^{-10}$ m/s$^2$

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
