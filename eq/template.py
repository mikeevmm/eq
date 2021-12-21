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

\begin{document}

\(\displaystyle
    % Your equation here
\)

\end{document}''')

def put(folder, file_name='eq.tex'):
    file_name = os.path.join(folder, file_name)
    with open(file_name, 'w') as outfile:
        outfile.write(_LATEX_DEFAULT)
    return file_name
