#!/usr/bin/env python
# encoding: utf-8
"""
Transform a YAML file into a LaTeX Beamer presentation.

Usage: yml2tex.py input.yml > output.tex

by Arthur Koziel <arthur@arthurkoziel.com>
"""

import yaml
from sys import argv

def separate(doc):
    """
    Given the parsed document structure, return a separated list where the first 
    value is a key and the second value all its underlying elements. 
    
    For example, the first value might be a section and the second value all 
    its subsections.
        
    Examples:
    
    >>> separate([{'a': [{'b': [{'c': ['d', 'e', 'f']}]}]}])
    [('a', [{'b': [{'c': ['d', 'e', 'f']}]}])]
    
    >>> separate([{'c': ['d', 'e', 'f']}])
    [('c', ['d', 'e', 'f'])]
    """
    return [(k, j[k]) for i, j in enumerate(doc) for k in j]

def section(title):
    """
    Given the section title, return its corresponding LaTeX command.
    """
    return '\n\n\section{%s}' % title

def subsection(title):
    """
    Given the subsection title, return its corresponding LaTeX command.
    """
    return '\n\subsection{%s}' % title

def frame(title, items):
    """
    Given the frame title and corresponding items, delegate to the appropriate 
    function and returns its LaTeX commands.
    """
    if title.startswith('include'):
        out = code(title)
    elif title.startswith('image'):
        out = image(title)
    else:
        out = "\n\\frame {"
        out += "\n\t\\frametitle{%s}" % title
        out += itemize(items)
        out += "\n}"
    return out

def itemize(items):
    """
    Given the items for a frame, returns the LaTeX syntax for an itemized list.
    If an item itself is a dictionary, a nested list will be created.
    
    The script doesn't limit the depth of nested lists. However, LaTeX Beamer 
    class limits lists to be nested up to a depth of 3.
    """
    out = "\n\t\\begin{itemize}[<+-| alert@+>]"
    for item in items:
        if isinstance(item, dict):
            for i in item:
                out += "\n\t\\item %s" % i
                out += itemize(item[i])
        else:
            out += "\n\t\\item %s" % item
    out += "\n\t\end{itemize}"
    return out

def code(title):
    """
    Given a frame title, which starts with "include", return a new frame with a 
    idiopidae (http://www.zedshaw.com/projects/idiopidae/) placeholder for code 
    inclusion.
    """
    filename = title.split(' ')[1]
    
    out = "\n\\begin{frame}[fragile,t]"
    out += "\n\t\\frametitle{Code: \"%s\"}" % filename
    out += "\n\t### @include \"%s\" 1 latex" % filename
    out += "\n\t### @end"
    out += "\n\end{frame}"
    return out

def image(title):
    """
    Given a frame title, which starts with "image" and is followed by the image 
    path, return the LaTeX command to include the image.
    """
    out = "\n\\frame[shrink] {"
    out += "\n\t\\pgfimage{%s}" % title.split(' ')[1]
    out += "\n}"
    return out

def header():
    """
    Return the LaTeX Beamer document header declarations.
    """
    out = "\documentclass[slidestop,red]{beamer}"
    out += "\n\usepackage[utf8]{inputenc}"
    out += "\n\usepackage{fancyvrb,color}"
    
    out += r'''

% pygments "colorful" style definitions
\newcommand\at{@}
\newcommand\lb{[}
\newcommand\rb{]}
\newcommand\PYbg[1]{\textcolor[rgb]{0.00,0.50,0.00}{\textbf{#1}}}
\newcommand\PYbf[1]{\colorbox[rgb]{0.88,0.88,0.88}{#1}}
\newcommand\PYbe[1]{\textcolor[rgb]{0.19,0.19,0.19}{#1}}
\newcommand\PYbd[1]{\colorbox[rgb]{1.00,0.94,0.94}{#1}}
\newcommand\PYbc[1]{\textcolor[rgb]{0.00,0.50,0.00}{\textbf{#1}}}
\newcommand\PYbb[1]{\textcolor[rgb]{0.00,0.00,0.50}{\textbf{#1}}}
\newcommand\PYba[1]{\textcolor[rgb]{0.00,0.44,0.00}{#1}}
\newcommand\PYaJ[1]{\colorbox[rgb]{1.00,0.94,0.94}{#1}}
\newcommand\PYaK[1]{\textcolor[rgb]{0.00,0.38,0.69}{\textbf{#1}}}
\newcommand\PYaH[1]{\colorbox[rgb]{0.94,0.63,0.63}{\textcolor[rgb]{0.94,0.00,0.00}{#1}}}
\newcommand\PYaI[1]{\textcolor[rgb]{0.19,0.19,0.56}{\textbf{#1}}}
\newcommand\PYaN[1]{\textcolor[rgb]{0.69,0.00,0.38}{\textbf{#1}}}
\newcommand\PYaO[1]{\textcolor[rgb]{0.78,0.36,0.04}{\textbf{#1}}}
\newcommand\PYaL[1]{\textcolor[rgb]{0.73,0.73,0.73}{#1}}
\newcommand\PYaM[1]{\textcolor[rgb]{0.31,0.44,0.56}{#1}}
\newcommand\PYaB[1]{\textcolor[rgb]{0.00,0.25,0.82}{#1}}
\newcommand\PYaC[1]{\textcolor[rgb]{0.31,0.31,0.31}{\textbf{#1}}}
\newcommand\PYaA[1]{\textcolor[rgb]{0.00,0.44,0.13}{#1}}
\newcommand\PYaF[1]{\textcolor[rgb]{1.00,0.00,0.00}{#1}}
\newcommand\PYaG[1]{\textcolor[rgb]{0.00,0.50,0.00}{\textbf{#1}}}
\newcommand\PYaD[1]{\textcolor[rgb]{0.50,0.50,0.50}{#1}}
\newcommand\PYaE[1]{\textcolor[rgb]{0.63,0.00,0.00}{#1}}
\newcommand\PYaZ[1]{\colorbox[rgb]{1.00,0.94,0.94}{#1}}
\newcommand\PYaX[1]{\colorbox[rgb]{1.00,0.94,0.94}{#1}}
\newcommand\PYaY[1]{\textcolor[rgb]{0.00,0.44,0.13}{#1}}
\newcommand\PYaR[1]{\textcolor[rgb]{0.19,0.19,0.69}{#1}}
\newcommand\PYaS[1]{\textcolor[rgb]{0.00,0.31,0.50}{\textbf{#1}}}
\newcommand\PYaP[1]{\textcolor[rgb]{0.00,0.00,0.75}{#1}}
\newcommand\PYaQ[1]{\textcolor[rgb]{0.38,0.00,0.88}{\textbf{#1}}}
\newcommand\PYaV[1]{\textcolor[rgb]{0.94,0.00,0.00}{\textbf{#1}}}
\newcommand\PYaW[1]{\textcolor[rgb]{0.05,0.52,0.71}{\textbf{#1}}}
\newcommand\PYaT[1]{\textcolor[rgb]{0.50,0.50,0.50}{#1}}
\newcommand\PYaU[1]{\textcolor[rgb]{0.50,0.00,0.50}{\textbf{#1}}}
\newcommand\PYaj[1]{\textcolor[rgb]{0.00,0.19,0.50}{\textbf{#1}}}
\newcommand\PYak[1]{\colorbox[rgb]{1.00,0.94,1.00}{\textcolor[rgb]{0.00,0.00,0.00}{#1}}}
\newcommand\PYah[1]{\textcolor[rgb]{0.56,0.44,0.00}{\textbf{#1}}}
\newcommand\PYai[1]{\textcolor[rgb]{0.56,0.38,0.19}{#1}}
\newcommand\PYan[1]{\textcolor[rgb]{0.00,0.00,0.00}{\textbf{#1}}}
\newcommand\PYao[1]{\colorbox[rgb]{1.00,0.94,0.94}{\textcolor[rgb]{0.38,0.38,0.38}{\textbf{#1}}}}
\newcommand\PYal[1]{\textcolor[rgb]{0.80,0.00,0.00}{\textbf{#1}}}
\newcommand\PYam[1]{\textbf{#1}}
\newcommand\PYab[1]{\textit{#1}}
\newcommand\PYac[1]{\textcolor[rgb]{0.00,0.25,0.82}{#1}}
\newcommand\PYaa[1]{\textcolor[rgb]{0.50,0.50,0.50}{#1}}
\newcommand\PYaf[1]{\textcolor[rgb]{0.50,0.50,0.50}{#1}}
\newcommand\PYag[1]{\textcolor[rgb]{0.00,0.00,0.82}{\textbf{#1}}}
\newcommand\PYad[1]{\colorbox[rgb]{1.00,0.94,0.94}{#1}}
\newcommand\PYae[1]{\textcolor[rgb]{0.25,0.00,0.88}{\textbf{#1}}}
\newcommand\PYaz[1]{\textcolor[rgb]{0.00,0.63,0.00}{#1}}
\newcommand\PYax[1]{\textcolor[rgb]{0.50,0.00,0.00}{\textbf{#1}}}
\newcommand\PYay[1]{\textcolor[rgb]{0.00,0.50,0.00}{\textbf{#1}}}
\newcommand\PYar[1]{\textcolor[rgb]{0.82,0.44,0.00}{\textbf{#1}}}
\newcommand\PYas[1]{\textcolor[rgb]{0.82,0.25,0.13}{#1}}
\newcommand\PYap[1]{\colorbox[rgb]{1.00,0.94,0.94}{\textcolor[rgb]{0.82,0.13,0.00}{#1}}}
\newcommand\PYaq[1]{\textcolor[rgb]{0.00,0.19,0.38}{\textbf{#1}}}
\newcommand\PYav[1]{\textcolor[rgb]{0.00,0.00,0.82}{\textbf{#1}}}
\newcommand\PYaw[1]{\textcolor[rgb]{0.38,0.00,0.88}{\textbf{#1}}}
\newcommand\PYat[1]{\textcolor[rgb]{0.19,0.38,0.56}{#1}}
\newcommand\PYau[1]{\textcolor[rgb]{0.63,0.38,0.00}{#1}}
% end pygments style definitions'''

    out += "\n\n\usetheme{Antibes}"
    out += "\n\setbeamertemplate{footline}[frame number]"
    out += "\n\usecolortheme{lily}"
    out += "\n\\beamertemplateshadingbackground{blue!5}{yellow!10}"
    
    out += "\n\n\\title{Example Presentation Created with the Beamer Package}"
    out += "\n\\author{Arthur Koziel}"
    out += "\n\date{\\today}"
    out += "\n\n\\begin{document}"
    out += "\n\n\\frame{\\titlepage}"
    
    out += "\n\n\section*{Outline}"
    out += "\n\\frame {"
    out += "\n\t\\frametitle{Outline}"
    out += "\n\t\\tableofcontents"
    out += "\n}"

    out += "\n\n\AtBeginSection[] {"
    out += "\n\t\\frame{"
    out += "\n\t\t\\frametitle{Outline}"
    out += "\n\t\t\\tableofcontents[currentsection]"
    out += "\n\t}"
    out += "\n}"
    return out

def footer():
    """
    Return the LaTeX Beamer document footer.
    """
    out = "\n\end{document}"
    return out

def main():
    """
    Return the final LaTeX presentation after invoking all necessary functions.
    """
    doc = yaml.load(open(argv[1]).read())
    out = header()
    for sections, doc in separate(doc):
        out += section(sections)
        for subsections, doc in separate(doc):
            out += subsection(subsections)
            for frames, items in separate(doc):
                out += frame(frames, items)
    out += footer()
    return out

if __name__ == '__main__':
    if len(argv) != 2:
        print __doc__
    else:
        print main().encode('utf-8')