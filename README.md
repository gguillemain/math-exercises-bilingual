# Manuel de Mathématiques Bilingue / Zweisprachiges Mathematik-Lehrbuch

Ce dépôt contient les sources d'un manuel de mathématiques bilingue (français-allemand) avec support LaTeX/MathJax pour le rendu web.

## Structure du Projet

```
.
├── chapters/                  # Contenu des chapitres
│   └── parallelperp/         # Chapitre sur les droites parallèles et perpendiculaires
│       ├── lesson/           # Contenu de la leçon
│       ├── exercises/        # Exercices du chapitre
│       └── translations.json # Traductions FR/DE
├── config/
│   └── latex/
│       └── preamble.tex      # Configuration LaTeX
├── scripts/
│   ├── generate_books.py     # Script de génération bilingue
│   └── build_books.sh        # Script de compilation
├── web/                      # Version web avec MathJax
└── output/                   # Fichiers générés (FR/DE)
```

## Prérequis

- Python 3.x
- LaTeX (TeXLive ou similaire)
- Packages LaTeX requis :
  - babel (support multilingue)
  - pstricks (figures géométriques)
  - amsmath, amssymb (symboles mathématiques)
  - Et autres packages listés dans preamble.tex

## Génération des Manuels

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/votre-nom/math-exercises-bilingual.git
   cd math-exercises-bilingual
   ```

2. Rendre le script de compilation exécutable :
   ```bash
   chmod +x scripts/build_books.sh
   ```

3. Générer les versions française et allemande :
   ```bash
   ./scripts/build_books.sh
   ```

Les PDF générés seront disponibles à la racine du projet :
- `math_book_fr.pdf` (version française)
- `math_book_de.pdf` (version allemande)

## Test du Rendu Web

Pour tester le rendu MathJax :
1. Ouvrir `web/index.html` dans un navigateur
2. Vérifier que les équations mathématiques s'affichent correctement

## Contribuer

1. Pour ajouter un nouveau chapitre :
   - Créer un nouveau dossier dans `chapters/`
   - Suivre la structure du chapitre exemple
   - Ajouter les traductions dans un fichier `translations.json`

2. Pour modifier un chapitre existant :
   - Modifier les fichiers .tex correspondants
   - Mettre à jour les traductions si nécessaire
   - Régénérer les manuels

## Licence

Ce projet est sous licence [à définir].
