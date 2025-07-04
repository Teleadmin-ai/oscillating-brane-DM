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

    def process_markdown(self, file_path: Path, front_matter: Dict) -> str:
        """Process a markdown file for inclusion in the PDF."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove front matter
        content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)

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
            heading = f"## Blog Post: {title}"
            date = front_matter.get("date", "")
            if date:
                heading += f"\n*{date}*"
        else:
            heading = f"# {title}"

        # Add description if available
        description = front_matter.get("description", "")
        if description:
            heading += f"\n\n*{description.strip()}*"

        return f"{heading}\n\n{content}\n\\newpage\n"

    def create_combined_markdown(self) -> str:
        """Combine all markdown files into a single document."""
        files = self.find_markdown_files()

        # Create header
        header = f"""---
title: "{self.metadata['title']}"
author: "{self.metadata['author']}"
date: "{self.metadata['date']}"
subtitle: "{self.metadata['subtitle']}"
documentclass: report
fontsize: 11pt
geometry: margin=1in
toc: true
toc-depth: 3
numbersections: true
urlcolor: blue
linkcolor: black
---

\\newpage

# Preface

This document contains the complete theoretical framework and documentation for the Oscillating Brane Dark Matter Theory, where the universe is conceptualized as a vibrating 4-dimensional membrane in 5D space. The theory proposes that dark matter effects emerge from membrane oscillations excited by gravitational flows, naturally producing dark energy and MOND-like phenomena.

**Key Parameters:**
- Brane tension: τ₀ = 7.0 × 10¹⁹ J/m²
- Oscillation period: T = 2.0 ± 0.3 Gyr
- Extra dimension size: L = 0.2 μm
- MOND acceleration: a₀ = 1.1 × 10⁻¹⁰ m/s²

\\newpage

"""

        # Add table of contents will be auto-generated by pandoc

        # Process each file
        combined = header

        # Add main content
        combined += "\\part{Core Theory}\n\n"
        for i, (file_path, front_matter) in enumerate(
            files[:4]
        ):  # First 4 are core docs
            print(f"Processing: {file_path}")
            combined += self.process_markdown(file_path, front_matter)

        # Add supporting documents
        combined += "\\part{Supporting Documentation}\n\n"
        for file_path, front_matter in files[4:8]:  # Next batch
            if "posts" not in str(file_path):
                print(f"Processing: {file_path}")
                combined += self.process_markdown(file_path, front_matter)

        # Add blog posts
        if any("posts" in str(fp) for fp, _ in files):
            combined += "\\part{Research Blog Posts}\n\n"
            for file_path, front_matter in files:
                if "_posts" in str(file_path):
                    print(f"Processing: {file_path}")
                    combined += self.process_markdown(file_path, front_matter)

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
            # Basic conversion
            pypandoc.convert_text(
                combined_md,
                "pdf",
                format="markdown",
                outputfile=str(output_path),
                extra_args=[
                    "--pdf-engine=xelatex",  # or pdflatex, lualatex
                    "--highlight-style=tango",
                    "--top-level-division=chapter",
                    "-V",
                    "colorlinks=true",
                    "-V",
                    "toccolor=blue",
                    "-V",
                    "urlcolor=blue",
                    "-V",
                    "linkcolor=black",
                    "--dpi=150",  # Reduce image resolution
                    "-V",
                    "classoption=compress",  # Enable compression
                    "-V",
                    "fontsize=10pt",  # Slightly smaller font
                ],
            )
            print(f"PDF generated successfully: {output_path}")

        except RuntimeError as e:
            print(f"Error generating PDF: {e}")
            print("\nTrying alternative method with HTML intermediate...")

            # Alternative: markdown -> HTML -> PDF
            try:
                import pdfkit  # requires: pip install pdfkit

                html = pypandoc.convert_text(combined_md, "html", format="markdown")
                pdfkit.from_string(html, str(output_path))
                print(f"PDF generated via HTML: {output_path}")
            except Exception as e2:
                print(f"Alternative method also failed: {e2}")
                print("\nPlease ensure you have either:")
                print("1. pandoc and a LaTeX distribution (texlive, miktex) installed")
                print("2. wkhtmltopdf installed for the HTML->PDF conversion")


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

    # Also create a "latest" version
    latest_path = output_dir / "oscillating_brane_theory_latest.pdf"
    if output_path.exists():
        import shutil

        shutil.copy2(output_path, latest_path)
        print(f"Latest version copied to: {latest_path}")


if __name__ == "__main__":
    main()
