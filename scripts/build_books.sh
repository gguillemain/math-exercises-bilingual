#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting bilingual books generation...${NC}"

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 is not installed. Please install it first.${NC}"
    exit 1
fi

# Generate the books using the Python script
echo "Generating French and German versions..."
python3 scripts/generate_books.py

# Check if pdflatex is installed
if ! command -v pdflatex &> /dev/null; then
    echo -e "${RED}pdflatex is not installed. Please install TexLive or similar.${NC}"
    exit 1
fi

# Function to compile a LaTeX file
compile_latex() {
    local dir=$1
    local lang=$2
    
    echo -e "${GREEN}Compiling $lang version...${NC}"
    cd "output/$lang"
    
    # Run pdflatex twice to resolve references
    pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
    pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✓ $lang version compiled successfully"
        mv main.pdf "../../math_book_$lang.pdf"
    else
        echo -e "${RED}✗ Error compiling $lang version${NC}"
    fi
    
    # Cleanup auxiliary files
    rm -f *.aux *.log *.out *.toc *.idx
    cd ../..
}

# Compile both versions
compile_latex "output/fr" "fr"
compile_latex "output/de" "de"

echo -e "${GREEN}Done!${NC}"
echo "Generated PDFs:"
echo " - math_book_fr.pdf (French version)"
echo " - math_book_de.pdf (German version)"