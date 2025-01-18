#!/usr/bin/env python3
import json
import os
from pathlib import Path
import shutil

class BilingualBookGenerator:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.chapters_dir = self.base_dir / 'chapters'
        self.output_dir = self.base_dir / 'output'
        self.languages = ['fr', 'de']

    def load_translations(self, chapter):
        """Load translations from JSON file for a specific chapter"""
        trans_file = self.chapters_dir / chapter / 'translations.json'
        try:
            with open(trans_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading translations from {trans_file}: {e}")
            return {}

    def process_chapter(self, chapter_name, language):
        """Process a single chapter for the specified language"""
        print(f"Processing chapter {chapter_name} for {language}...")
        chapter_dir = self.chapters_dir / chapter_name
        translations = self.load_translations(chapter_name)
        
        # Create output directory for each language
        output_chapter_dir = self.output_dir / language / chapter_name
        output_chapter_dir.mkdir(parents=True, exist_ok=True)

        # Process lesson
        lesson_file = chapter_dir / 'lesson' / 'lesson.tex'
        if lesson_file.exists():
            self.process_tex_file(lesson_file, output_chapter_dir / 'lesson.tex', translations, language)

        # Process exercises
        exercises_dir = chapter_dir / 'exercises'
        if exercises_dir.exists():
            for ex_file in exercises_dir.glob('*.tex'):
                self.process_tex_file(ex_file, output_chapter_dir / ex_file.name, translations, language)

    def process_tex_file(self, input_file, output_file, translations, language):
        """Process a single TeX file with translations"""
        print(f"Processing {input_file}...")
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace exercise titles and instructions
            for ex_id, ex_data in translations.get('exercises', {}).items():
                if 'title' in ex_data:
                    content = content.replace(
                        f'\\transTitle{{{ex_id}}}',
                        ex_data['title'][language]
                    )
                if 'instructions' in ex_data:
                    content = content.replace(
                        f'\\transInstructions{{{ex_id}}}',
                        ex_data['instructions'][language]
                    )

            # Replace vocabulary
            for term, trans_dict in translations.get('vocabulary', {}).items():
                content = content.replace(
                    f'\\trans{{{term}}}',
                    trans_dict[language]
                )

            # Ensure output directory exists
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write processed content
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"Successfully processed {input_file}")
        except Exception as e:
            print(f"Error processing {input_file}: {e}")
            raise

    def copy_static_files(self, language):
        """Copy static files to output directory"""
        print(f"Copying static files for {language}...")
        try:
            # Copy config directory
            src_config = self.base_dir / 'config'
            dst_config = self.output_dir / language / 'config'
            if src_config.exists():
                shutil.copytree(src_config, dst_config, dirs_exist_ok=True)
        except Exception as e:
            print(f"Error copying static files: {e}")
            raise

    def generate_main_tex(self, language):
        """Generate main.tex file for each language"""
        print(f"Generating main.tex for {language}...")
        try:
            output_main = self.output_dir / language / 'main.tex'
            main_template = self.base_dir / 'main.tex'
            
            if main_template.exists():
                with open(main_template, 'r', encoding='utf-8') as f:
                    template = f.read()

                # Modify for language
                if language == 'fr':
                    title = "Mathématiques"
                    babel_option = "french"
                else:
                    title = "Mathematik"
                    babel_option = "german"

                content = template.replace('\\input{config/latex/preamble}',
                                        f'\\input{{config/latex/preamble}}\n'
                                        f'\\selectlanguage{{{babel_option}}}')
                content = content.replace('Mathematik -- Mathématiques', title)

                output_main.parent.mkdir(parents=True, exist_ok=True)
                with open(output_main, 'w', encoding='utf-8') as f:
                    f.write(content)
        except Exception as e:
            print(f"Error generating main.tex: {e}")
            raise

    def generate_books(self):
        """Generate both French and German versions of the book"""
        print("Starting book generation...")
        try:
            # Clean output directory
            if self.output_dir.exists():
                shutil.rmtree(self.output_dir)
            self.output_dir.mkdir(parents=True)

            for language in self.languages:
                print(f"\nGenerating {language} version...")
                
                # Process each chapter
                for chapter_dir in self.chapters_dir.iterdir():
                    if chapter_dir.is_dir():
                        self.process_chapter(chapter_dir.name, language)
                
                # Copy static files
                self.copy_static_files(language)
                
                # Generate main.tex
                self.generate_main_tex(language)
            
            print("\nBook generation completed successfully!")
        except Exception as e:
            print(f"Error during book generation: {e}")
            raise

if __name__ == "__main__":
    generator = BilingualBookGenerator(".")
    generator.generate_books()
