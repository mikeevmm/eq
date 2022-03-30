# -*- coding: utf-8 -*-

import os

_LATEX_DEFAULT = (
r'''\documentclass[border=5pt]{standalone}
\usepackage[english]{babel}
\usepackage[utf8x]{inputenc}
\usepackage{lmodern}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{microtype}
\usepackage{graphicx}
\usepackage{cleveref}
\usepackage{placeins}
\usepackage{physics}

% \gather* in standalone; see tex.stackexchange.com/146699
\newcommand{\diff}{\mathop{}\!d}
\renewenvironment{gather*}{$\gathered}{\endgathered$}

\begin{document}

\begin{gather*}
    % Your equations here
\end{gather*}

\end{document}''')

def put(folder, file_name='eq.tex'):
    file_name = os.path.join(folder, file_name)
    with open(file_name, 'w') as outfile:
        outfile.write(_LATEX_DEFAULT)
    return file_name
