#!/bin/bash
# Script to generate PDF and move it to the correct location for GitHub Pages

echo "Generating PDF documentation..."

# Change to the project root directory
cd "$(dirname "$0")/.."

# Generate the PDF
python scripts/generate_pdf.py

# Check if PDF was generated successfully
if [ -f "output/oscillating_brane_theory_latest.pdf" ]; then
    echo "PDF generated successfully!"
    
    # Copy to the root directory so it's accessible via the website
    cp output/oscillating_brane_theory_latest.pdf ./oscillating_brane_theory_latest.pdf
    
    # Also create a versioned copy with today's date
    DATE=$(date +%Y%m%d)
    cp output/oscillating_brane_theory_latest.pdf "./oscillating_brane_theory_${DATE}.pdf"
    
    echo "PDF files copied to root directory for web access"
    echo "Files created:"
    echo "  - oscillating_brane_theory_latest.pdf"
    echo "  - oscillating_brane_theory_${DATE}.pdf"
    
    # Add to git if in a git repository
    if [ -d ".git" ]; then
        git add oscillating_brane_theory_latest.pdf
        git add "oscillating_brane_theory_${DATE}.pdf"
        echo "PDF files added to git"
    fi
else
    echo "Error: PDF generation failed!"
    exit 1
fi