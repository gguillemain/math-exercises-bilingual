#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path

class BilingualBookGenerator:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.chapters_dir = self.base_dir / 'chapters'
        self.output_dir = self.base_dir / 'output'
        self.languages = ['fr', 'de']

    def load_translations(self, chapter):
        """Load translations from JSON file for a specific chapter"""
        trans_file = self.chapters_dir / chapter / 'translations.json'
        with open(trans_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def process_chapter(self, chapter_name, language):
        """Process a single chapter for the specified language"""
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
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace exercise titles
        for ex_id, ex_data in translations.get('exercises', {}).items():
            if 'title' in ex_data:
                pattern = fr'\\exo{{.*?{ex_id}.*?}}'
                replacement = f'\\exo{{{ex_data["title"][language]}}}'
                content = re.sub(pattern, replacement, content)

        # Replace vocabulary
        for term, translations_dict in translations.get('vocabulary', {}).items():
            content = content.replace(f'\\vocab{{{term}}}', translations_dict[language])

        # Replace instructions
        for ex_id, ex_data in translations.get('exercises', {}).items():
            if 'instructions' in ex_data:
                content = content.replace(
                    f'\\instructions{{{ex_id}}}',
                    ex_data['instructions'][language]
                )

        # Write processed content
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate_main_tex(self, language):
        """Generate main.tex file for each language"""
        output_main = self.output_dir / language / 'main.tex'
        
        # Read template
        with open(self.base_dir / 'main.tex', 'r', encoding='utf-8') as f:
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

        # Write output
        output_main.parent.mkdir(parents=True, exist_ok=True)
        with open(output_main, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate_books(self):
        """Generate both French and German versions of the book"""
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        for language in self.languages:
            print(f"Generating {language} version...")
            
            # Process each chapter
            for chapter_dir in self.chapters_dir.iterdir():
                if chapter_dir.is_dir():
                    self.process_chapter(chapter_dir.name, language)
            
            # Generate main.tex
            self.generate_main_tex(language)
            
            # Copy configuration files
            config_dir = self.output_dir / language / 'config'
            config_dir.mkdir(parents=True, exist_ok=True)
            os.system(f'cp -r {self.base_dir}/config/* {config_dir}')

if __name__ == "__main__":
    generator = BilingualBookGenerator(".")
    generator.generate_books()
