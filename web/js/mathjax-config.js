window.MathJax = {
    tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']],
        displayMath: [['$$', '$$'], ['\\[', '\\]']],
        processEscapes: true,
        macros: {
            // Définitions de macros LaTeX couramment utilisées
            R: '{\\mathbb{R}}',
            N: '{\\mathbb{N}}',
            Z: '{\\mathbb{Z}}',
            Q: '{\\mathbb{Q}}',
            // Opérateurs mathématiques bilingues
            pgcd: '{\\text{pgcd}}',  // français
            ggT: '{\\text{ggT}}',    // allemand (größter gemeinsamer Teiler)
            ppcm: '{\\text{ppcm}}',  // français
            kgV: '{\\text{kgV}}'     // allemand (kleinstes gemeinsames Vielfaches)
        }
    },
    svg: {
        fontCache: 'global'
    }
};