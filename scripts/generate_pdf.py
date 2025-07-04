#!/usr/bin/env python3
"""
Generate a comprehensive PDF document from all markdown files in the site.
Combines theory documents, blog posts, and other content into a single PDF.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import pypandoc
import yaml

# Install required packages:
# pip install pypandoc pyyaml


class PDFGenerator:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.content_files = []
        self.metadata = {
            "title": "Oscillating Brane Dark Matter Theory - Complete Documentation",
            "author": "Romain Provencal",
            "date": datetime.now().strftime("%B %Y"),
            "subtitle": "The Universe as a Vibrating Membrane",
        }

    def find_markdown_files(self) -> List[Tuple[Path, Dict]]:
        """Find all markdown files and extract their front matter."""
        files = []

        # Main documentation files (in order)
        doc_order = [
            "index.md",
            "theory.md",
            "docs/theory_v4_complete.md",
            "docs/theoretical_foundations.md",
            "chronology.md",
            "predictions.md",
            "tools.md",
            "about.md",
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

    def clean_unicode_artifacts(self, text: str) -> str:
        """Clean common Unicode artifacts from text."""
        # First, clean up corrupted patterns that O3 Pro found
        # These appear when Unicode characters get mangled during PDF conversion
        text = text.replace("10ff¹ff Hz", "10⁻¹⁷ Hz")  # Fix corrupted superscript
        text = text.replace(
            "ff27 times", "≈27 times"
        )  # Fix corrupted approximation symbol

        # Clean up common ligature artifacts
        replacements = {
            "ﬀ": "ff",  # ff ligature
            "ﬁ": "fi",  # fi ligature
            "ﬂ": "fl",  # fl ligature
            "ﬃ": "ffi",  # ffi ligature
            "ﬄ": "ffl",  # ffl ligature
            "ff¹": "⁻¹",  # This pattern appears when ⁻¹ gets corrupted
            # Remove these replacements to preserve mathematical notation
            # "−": "-",  # Keep minus sign for math
            # "–": "--",  # Keep en dash
            # "—": "---",  # Keep em dash
            # Keep smart quotes and special characters
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def convert_unicode_to_latex(self, text: str) -> str:
        """Convert Unicode mathematical symbols to LaTeX commands."""
        # First, handle specific number patterns with superscripts
        # This prevents split math expressions
        import re

        # Pattern for numbers with Unicode superscripts (e.g., 10⁻¹⁷)
        def replace_number_superscripts(match):
            base = match.group(1)
            superscript = match.group(2)

            # Convert entire superscript sequences first
            superscript_sequences = {
                "⁻¹⁷": "-17",
                "⁻¹⁸": "-18",
                "⁻¹⁰": "-10",
                "⁻⁷⁰": "-70",
                "¹⁹": "19",
                "¹⁸": "18",
                "¹⁷": "17",
                "¹⁶": "16",
                "¹⁵": "15",
                "¹⁴": "14",
                "¹³": "13",
                "¹²": "12",
                "¹¹": "11",
                "¹⁰": "10",
            }

            # Check for known sequences first
            for seq, replacement in superscript_sequences.items():
                if seq in superscript:
                    superscript = superscript.replace(seq, replacement)

            # Then handle individual characters
            superscript_chars = {
                "⁻": "-",
                "⁰": "0",
                "¹": "1",
                "²": "2",
                "³": "3",
                "⁴": "4",
                "⁵": "5",
                "⁶": "6",
                "⁷": "7",
                "⁸": "8",
                "⁹": "9",
            }

            # Replace remaining individual characters
            for uni, num in superscript_chars.items():
                superscript = superscript.replace(uni, num)

            # Wrap in braces if multi-character or negative
            if len(superscript) > 1 or "-" in superscript:
                return f"${base}^{{{superscript}}}$"
            else:
                return f"${base}^{superscript}$"

        # Replace number patterns with superscripts (e.g., 10⁻¹⁷ → $10^{-17}$)
        text = re.sub(
            r"(\d+)([\u2070-\u209f⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)", replace_number_superscripts, text
        )

        # Also handle superscripts after units (e.g., Gyr⁻¹ → Gyr$^{-1}$)
        def replace_unit_superscripts(match):
            unit = match.group(1)
            superscript = match.group(2)

            # Convert superscript characters
            superscript_chars = {
                "⁻¹": "^{-1}",
                "⁻²": "^{-2}",
                "⁻³": "^{-3}",
                "⁻": "^{-}",
                "¹": "^1",
                "²": "^2",
                "³": "^3",
            }

            for uni, latex in superscript_chars.items():
                superscript = superscript.replace(uni, latex)

            return f"{unit}${superscript}$"

        # Replace superscripts after common units
        text = re.sub(
            r"(Gyr|Hz|m|s|kg|GeV|eV|pc|Mpc|cm)([\u2070-\u209f⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)",
            replace_unit_superscripts,
            text,
        )

        # Fix patterns like "× $10^{-17}$" to be inside single math environment
        text = re.sub(r"×\s*\$(\d+\^{[^}]+})\$", r"$\\times \1$", text)
        text = re.sub(r"(\d+)\s*×\s*\$(\d+\^{[^}]+})\$", r"$\1 \\times \2$", text)

        # Handle emojis and special characters that should always be replaced
        emoji_replacements = {
            "🌌": "[universe]",
            "📥": "[download]",
            "✓": "[check]",
            "☉": "Sun",
            "🤖": "[AI]",
            "ï": "i",  # Convert to regular i
        }

        for old, new in emoji_replacements.items():
            text = text.replace(old, new)

        # For math blocks, we need different replacements (no $ wrapper)
        math_replacements = {
            "τ": r"\tau",
            "σ": r"\sigma",
            "ρ": r"\rho",
            "π": r"\pi",
            "μ": r"\mu",
            "λ": r"\lambda",
            "η": r"\eta",
            "δ": r"\delta",
            "γ": r"\gamma",
            "ω": r"\omega",
            "φ": r"\phi",
            "χ": r"\chi",
            "ξ": r"\xi",
            "Δ": r"\Delta",
            "Ω": r"\Omega",
            "₀": r"_0",
            "₁": r"_1",
            "₂": r"_2",
            "₃": r"_3",
            "₄": r"_4",
            "₅": r"_5",
            "₆": r"_6",
            "₇": r"_7",
            "₈": r"_8",
            "₉": r"_9",
            "₊": r"_+",
            "≈": r"\approx",
            "≃": r"\simeq",
            "≤": r"\leq",
            "≥": r"\geq",
            "≪": r"\ll",
            "≫": r"\gg",
            "≲": r"\lesssim",
            "≳": r"\gtrsim",
            "∝": r"\propto",
            "∂": r"\partial",
            "∞": r"\infty",
            "⊥": r"\perp",
            "ℓ": r"\ell",
            "ℏ": r"\hbar",
            "ℒ": r"\mathcal{L}",
            "⊙": r"\odot",
        }

        # Replace in math environments first
        import re

        # Pattern to match math environments
        math_pattern = r"(\$\$[\s\S]*?\$\$|\$[^\$\n]+\$|\\begin\{equation\}[\s\S]*?\\end\{equation\}|\\begin\{align\}[\s\S]*?\\end\{align\}|\\\[[\s\S]*?\\\])"

        def replace_in_math(match):
            math_text = match.group(0)
            # Replace mathematical symbols
            for old, new in math_replacements.items():
                if old in "τσρπμλδηγωφχξΔ":
                    # Greek letters: add space when followed by a letter
                    import re

                    pattern = re.escape(old) + r"(?=[a-zA-Z])"
                    replacement = new.replace("\\", "\\\\") + " "
                    math_text = re.sub(pattern, replacement, math_text)
                elif old == "∂":
                    # Special handling for partial derivative - always add space after
                    math_text = math_text.replace(old, new + " ")
                    continue
                # Always do the general replacement too (for cases not followed by letters)
                math_text = math_text.replace(old, new)
            return math_text

        text = re.sub(math_pattern, replace_in_math, text)

        # Now handle non-math text (add $ wrappers)
        non_math_replacements = {
            "τ": r"$\tau$",
            "σ": r"$\sigma$",
            "ρ": r"$\rho$",
            "π": r"$\pi$",
            "μ": r"$\mu$",
            "λ": r"$\lambda$",
            "η": r"$\eta$",
            "δ": r"$\delta$",
            "γ": r"$\gamma$",
            "ω": r"$\omega$",
            "φ": r"$\phi$",
            "χ": r"$\chi$",
            "ξ": r"$\xi$",
            "Δ": r"$\Delta$",
            "Ω": r"$\Omega$",
            "₀": r"$_0$",
            "₁": r"$_1$",
            "₂": r"$_2$",
            "₃": r"$_3$",
            "₄": r"$_4$",
            "₅": r"$_5$",
            "₆": r"$_6$",
            "₇": r"$_7$",
            "₈": r"$_8$",
            "₉": r"$_9$",
            "≈": r"$\approx$",
            "≃": r"$\simeq$",
            "≤": r"$\leq$",
            "≥": r"$\geq$",
            "≪": r"$\ll$",
            "≲": r"$\lesssim$",
            "≳": r"$\gtrsim$",
            "∝": r"$\propto$",
            "∂": r"$\partial$",
            "∞": r"$\infty$",
            "⊥": r"$\perp$",
            "ℓ": r"$\ell$",
            "ℏ": r"$\hbar$",
            "ℒ": r"$\mathcal{L}$",
            "⊙": r"$\odot$",
        }

        # Split and process non-math parts
        parts = re.split(math_pattern, text)
        for i in range(len(parts)):
            # Even indices are non-math text
            if i % 2 == 0:
                for old, new in non_math_replacements.items():
                    parts[i] = parts[i].replace(old, new)

        return "".join(parts)

    def process_markdown(
        self, file_path: Path, front_matter: Dict, is_first: bool = False
    ) -> str:
        """Process a markdown file for inclusion in the PDF."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove front matter
        content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)

        # Fix split math expressions BEFORE conversion
        # Pattern: number followed by $^{...}$
        content = re.sub(r"(\d+)\s*\$\^\{([^}]+)\}\$", r"$\1^{\2}$", content)

        # Also fix patterns like "× 10$^{-17}$" to be "× $10^{-17}$"
        content = re.sub(r"×\s*(\d+)\s*\$\^\{([^}]+)\}\$", r"× $\1^{\2}$", content)

        # Convert Unicode to LaTeX BEFORE cleaning artifacts
        # This prevents Unicode characters from being corrupted during conversion
        content = self.convert_unicode_to_latex(content)

        # Clean Unicode artifacts (only problematic ligatures, not math symbols)
        content = self.clean_unicode_artifacts(content)

        # Fix image paths to be absolute
        # Replace relative paths like /plots/image.png with absolute paths
        content = re.sub(
            r"!\[([^\]]*)\]\((/[^)]+)\)",
            lambda m: f"![{m.group(1)}]({self.base_dir}{m.group(2)})",
            content,
        )

        # Also fix image paths that start with {{ site.baseurl }} or similar
        content = re.sub(
            r'!\[([^\]]*)\]\({{\s*["\']?/?([^}"\']+)["\']?\s*\|\s*relative_url\s*}}\)',
            lambda m: f"![{m.group(1)}]({self.base_dir}/{m.group(2)})",
            content,
        )

        # Add chapter heading based on front matter
        title = front_matter.get("title", file_path.stem.replace("_", " ").title())

        # Determine heading level based on file type
        if "_posts" in str(file_path):
            heading = f"# {title}"
            date = front_matter.get("date", "")
            if date:
                heading += f"\n*{date}*"
        else:
            heading = f"# {title}"

        # Add description if available
        description = front_matter.get("description", "")
        if description:
            heading += f"\n\n*{description.strip()}*"

        # Check if content already starts with a heading
        content_stripped = content.strip()
        if content_stripped.startswith("# "):
            # Content already has a top-level heading, don't add another one
            # But ensure there's some content visible after the heading
            lines = content.split("\n")
            if len(lines) > 1 and lines[1].strip().startswith("##"):
                # Add a brief intro if the next line is a subheading
                lines.insert(1, "\n*Content from this section:*\n")
                content = "\n".join(lines)
            # IMPORTANT: Add newpage BEFORE to start a new chapter (unless it's the first)
            if is_first:
                return f"{content}\n"
            else:
                return f"\\newpage\n{content}\n"
        else:
            # Add the heading we created with newpage before (unless it's the first)
            if is_first:
                return f"{heading}\n\n{content}\n"
            else:
                return f"\\newpage\n{heading}\n\n{content}\n"

    def create_combined_markdown(self) -> str:
        """Combine all markdown files into a single document."""
        files = self.find_markdown_files()

        # Create header
        header = f"""---
title: "{self.metadata['title']}"
author: "{self.metadata['author']}"
date: "{self.metadata['date']}"
subtitle: "{self.metadata['subtitle']}"
documentclass: book
fontsize: 11pt
geometry: margin=1in
toc: true
toc-depth: 2
numbersections: true
chapters: true
urlcolor: blue
linkcolor: black
---

\\newpage

# Preface

This document contains the complete theoretical framework and documentation for the Oscillating Brane Dark Matter Theory, where the universe is conceptualized as a vibrating 4-dimensional membrane in 5D space. The theory proposes that dark matter effects emerge from membrane oscillations excited by gravitational flows, naturally producing dark energy and MOND-like phenomena.

**Key Parameters:**
- Brane tension: $\\tau_0$ = 7.0 × 10$^{19}$ J/m$^2$
- Oscillation period: T = 2.0 ± 0.3 Gyr
- Extra dimension size: L = 0.2 $\\mu$m
- MOND acceleration: a$_0$ = 1.1 × 10$^{-10}$ m/s$^2$

\\newpage

"""

        # Add table of contents will be auto-generated by pandoc

        # Process each file
        combined = header

        # Process all files without parts - just chapters
        for i, (file_path, front_matter) in enumerate(files):
            print(f"Processing: {file_path}")
            # Pass index to know if it's the first file
            content = self.process_markdown(file_path, front_matter, is_first=(i == 0))
            combined += content

        return combined

    def generate_pdf(self, output_path: Path):
        """Generate the PDF using pandoc."""
        # Create combined markdown
        combined_md = self.create_combined_markdown()

        # Save intermediate markdown (for debugging)
        temp_md = output_path.with_suffix(".combined.md")
        with open(temp_md, "w", encoding="utf-8") as f:
            f.write(combined_md)
        print(f"Combined markdown saved to: {temp_md}")

        # Convert to PDF using pandoc
        try:
            # Basic conversion - try pdflatex with minimal options
            pypandoc.convert_text(
                combined_md,
                "pdf",
                format="markdown",  # Basic markdown
                outputfile=str(output_path),
                extra_args=[
                    "--pdf-engine=xelatex",  # XeLaTeX for Unicode support
                    "--top-level-division=chapter",  # Each file = new chapter
                    "--highlight-style=tango",
                    "-V",
                    "geometry:margin=1in",
                    "-V",
                    "colorlinks=true",
                ],
            )
            print(f"PDF generated successfully: {output_path}")
            return  # Success! Exit the method

        except Exception as e:
            print(f"Error generating PDF: {e}")
            print(f"Error type: {type(e).__name__}")
            import traceback

            traceback.print_exc()
            # Re-raise to stop execution - NO FALLBACK!
            raise RuntimeError(f"Failed to generate PDF with XeLaTeX: {e}")


def main():
    """Main entry point."""
    # Get the base directory (parent of scripts/)
    base_dir = Path(__file__).parent.parent

    # Create output directory
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"oscillating_brane_theory_{timestamp}.pdf"

    # Create generator and run
    generator = PDFGenerator(base_dir)
    generator.generate_pdf(output_path)

    # Debug: Check if PDF was created
    print(f"\nChecking if PDF was created at: {output_path}")
    print(f"File exists: {output_path.exists()}")
    if output_path.exists():
        print(f"File size: {output_path.stat().st_size} bytes")
    else:
        print("ERROR: PDF file was NOT created!")
        # List files in output directory
        print("\nFiles in output directory:")
        for f in output_dir.iterdir():
            print(f"  - {f.name}")

    # Also create a "latest" version in output directory
    latest_path = output_dir / "oscillating_brane_theory_latest.pdf"
    if output_path.exists():
        import shutil

        shutil.copy2(output_path, latest_path)
        print(f"Latest version copied to: {latest_path}")

        # Copy to root directory for website access
        root_pdf_path = base_dir / "oscillating_brane_theory_latest.pdf"
        shutil.copy2(output_path, root_pdf_path)
        print(f"PDF copied to root for website: {root_pdf_path}")


if __name__ == "__main__":
    main()
