#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print error and exit
error_exit() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

# Function to check if a command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        error_exit "$1 is not installed. Please install it first."
    fi
}

echo -e "${GREEN}Starting bilingual books generation...${NC}"

# Check required commands
check_command python3
check_command pdflatex

# Create a temporary directory for compilation
TEMP_DIR="temp_build"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Generate the books using the Python script
echo -e "${YELLOW}Generating French and German versions...${NC}"
python3 scripts/generate_books.py || error_exit "Book generation failed"

# Function to compile a LaTeX file
compile_latex() {
    local lang=$1
    local attempts=2  # Number of compilation attempts
    
    echo -e "${YELLOW}Compiling $lang version...${NC}"
    
    # Create temp directory for this language
    local temp_lang_dir="$TEMP_DIR/$lang"
    mkdir -p "$temp_lang_dir"
    
    # Create proper directory structure for aux files
    mkdir -p "$temp_lang_dir/parallelperp/lesson"
    mkdir -p "$temp_lang_dir/parallelperp/exercises"
    
    # Copy required files
    cp output/$lang/main.tex "$temp_lang_dir/"
    cp -r output/$lang/config "$temp_lang_dir/"
    cp -r output/$lang/parallelperp/* "$temp_lang_dir/parallelperp/"
    
    # Change to temp directory
    cd "$temp_lang_dir" || error_exit "Could not change to $temp_lang_dir directory"
    
    # Run pdflatex multiple times
    for i in $(seq 1 $attempts); do
        echo -e "${YELLOW}LaTeX compilation attempt $i/${attempts}...${NC}"
        TEXINPUTS=".:$temp_lang_dir:" pdflatex -interaction=nonstopmode -output-directory="$temp_lang_dir" main.tex > compile.log 2>&1
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ $lang version compiled successfully${NC}"
            mv main.pdf "../../math_book_$lang.pdf"
            cd ../.. || error_exit "Could not return to root directory"
            return 0
        else
            if [ $i -eq $attempts ]; then
                echo -e "${RED}✗ Error compiling $lang version${NC}"
                echo -e "${YELLOW}Last few lines of the log:${NC}"
                tail -n 20 compile.log
                cd ../.. || error_exit "Could not return to root directory"
                return 1
            fi
        fi
    done
}

# Compile both versions
compile_latex "fr" || error_exit "French compilation failed"
compile_latex "de" || error_exit "German compilation failed"

# Clean up
echo -e "${YELLOW}Cleaning up temporary files...${NC}"
rm -rf "$TEMP_DIR"

echo -e "${GREEN}Done!${NC}"
echo "Generated PDFs:"
echo " - math_book_fr.pdf (French version)"
echo " - math_book_de.pdf (German version)"