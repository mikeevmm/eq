#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""eq

Usage:
    eq [--density=<n>]
    eq (-h | --help)
    eq --version

Options:
    --density=<n>  PDF to PNG conversion image density [default: 300].
    -h --help      Show this screen.
    --version      Show version.
"""

import shutil
import os
import tempfile
import subprocess as sp
from docopt import docopt
import eq.template
from eq.version import __version__
from eq.log import log, error

def main():
    arguments = docopt(__doc__, version=f'eq v{__version__}')

    # Determine presence of and default executables

    pdflatex = shutil.which('pdflatex')
    if pdflatex is None:
        error('The pdflatex executable cannot be found.\n'
              'eq needs pdflatex to compile your equation, '
              'please make sure you have a LaTeX distribution installed and '
              'available to run.')
        exit(1)

    if shutil.which('convert') is None:
        # convert could not be found; imagemagick may still exist, as newer
        # versions rely on the "magick" command.
        if shutil.which('magick') is None:
            error('The imagemagick executable (magick or convert) could not '
                  'be found.\n'
                  'eq needs imagemagick to process your equation, '
                  'please make sure you have imagemagick installed and '
                  'available to run.')
            exit(1)
        # else:
        # The `magick` command was found.
        magick = ['magick', 'convert']
    else:
        # (imagemagick) `convert` was found.
        magick = ['convert']

    first = lambda x: next((y for y in x if y is not None), None)
    editor = first([shutil.which('editor'),
                    os.environ.get('VISUAL'),
                    os.environ.get('EDITOR'),
                    shutil.which('vim'),
                    shutil.which('nano')])
    if editor is None:
        error('Could not find an editor to edit the equation with.\n'
              'Tried `editor`, $VISUAL, $EDITOR, `vim`, `nano`, in that order. '
              'Please ensure one of these exists, or set $VISUAL/$EDITOR to '
              'your preferred editor.')
        exit(1)

    xclip = shutil.which('xclip')
    if xclip is None:
            error('The xclip executable could not be found.\n'
                  'eq needs xclip to copy the equation image into your '
                  'clipboard. Please ensure it is installed and available.')
            exit(1)

    # Create a temporary LaTeX project.
    # This is done at the EQ_PROJ_DIR location.
    # If none is set, /tmp is used.
    proj_parent_dir = os.path.abspath(os.environ.get('EQ_PROJ_DIR', '/tmp'))

    if not os.path.exists(proj_parent_dir):
        error('Specified project directory',
              f'"{proj_parent_dir}"', ' does not exist.')
        exit(1)

    with tempfile.TemporaryDirectory(prefix=proj_parent_dir + '/') as proj_dir:
        # Put default template into template directory
        file_name = eq.template.put(proj_dir)
        
        # Loop while the content changes on write
        with open(file_name, 'r') as old_file:
            old_content = old_file.read()
        
        while True:
            # Open template with editor
            sp.run([editor, file_name])

            # Compare with new content
            with open(file_name, 'r') as new_file:
                new_content = new_file.read()

            if new_content == old_content:
                break # out of edition loop
            # else:
            old_content = new_content

            # Do the rendering, and copy to the clipboard
            # Run pdflatex thrice, just for good measure
            failed = False
            for _ in range(3):
                result = sp.run(
                    [pdflatex, '-output-directory', proj_dir, file_name])
                if result.returncode != 0:
                    # Something went wrong with the compilation (user error?)
                    # Loop back to edition.
                    failed = True
                    break
            if failed:
                continue # to another edition pass.
            
            # Finished producing a PDF.
            # Now convert it to a white background PNG with imagemagick.
            pdf_name = os.path.splitext(file_name)[0] + '.pdf'
            png_name = os.path.splitext(file_name)[0] + '.png'
            density = arguments.get('--density', 300)
            result = sp.run(magick + ['-flatten', '-background', 'white',
                                '-density', density, pdf_name, png_name])

            if result.returncode != 0:
                error('Something went wrong with converting the PDF to a PNG.')
                log('Press any key to go back to edition.')
                input()
                continue # to another edition pass.
            # else: success

            # Copy the PNG into the clipboard
            result = sp.run([xclip, '-in', '-selection', 'clipboard',
                                '-target', 'image/png', png_name])
            if result.returncode != 0:
                error('Something went wrong with copying the PNG to your '
                      'clipboard.')
                log('Press any key to go back to edition.')
                input()
                continue # to another edition pass.

            # loop to another edition pass

