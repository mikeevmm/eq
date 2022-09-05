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
import platform
import subprocess as sp
from docopt import docopt
import eq.template
from eq.version import __version__
from eq.log import log, warn, error

def main():
    arguments = docopt(__doc__, version=f'eq v{__version__}')
    system = platform.system()

    # Determine presence of and default executables

    latexmk = shutil.which('latexmk')
    if latexmk is None:
        error('The latexmk executable cannot be found.\n'
              'eq needs latexmk to compile your equation, '
              'please make sure you have a LaTeX distribution installed and '
              'available to run, and then install latexmk.')
        exit(1)

    if shutil.which('magick') is None:
        # convert could not be found; imagemagick may still exist, as newer
        # versions rely on the "magick" command.
        if system != 'Windows' and shutil.which('convert') is None:
            error('The imagemagick executable (magick or convert) could not '
                  'be found.\n'
                  'eq needs imagemagick to process your equation, '
                  'please make sure you have imagemagick installed and '
                  'available to run.')
            exit(1)
        # else:
        # The `convert` command was found.
        magick = ['convert']
    else:
        # `magick` was found.
        magick = ['magick', 'convert']

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

    if system == 'Windows':
        nircmd = shutil.which('nircmd')
        if nircmd is None:
            error('The nircmdc executable could not be found.\n'
                  'eq needs nircmd to copy the equation image into your '
                  'clipboard. Please ensure it is installed and available.')

        def copy(png_name):
            png_name = os.path.realpath(png_name)
            return sp.run([nircmd, 'clipboard', 'copyimage', png_name])
    else:
        if system != 'Linux':
            warn('Treating system as Linux')
        xclip = shutil.which('xclip')
        if xclip is None:
            error('The xclip executable could not be found.\n'
                  'eq needs xclip to copy the equation image into your '
                  'clipboard. Please ensure it is installed and available.')
            exit(1)

        def copy(png_name):
            return sp.run([xclip, '-in', '-selection', 'clipboard',
                            '-target', 'image/png', png_name])


    # Create a temporary LaTeX project.
    with tempfile.TemporaryDirectory() as proj_dir:
        # Fix needed for Windows:
        # The default temporary directory has a ~ in it, and LaTeX really hates
        # that.
        proj_dir = os.path.realpath(proj_dir)
        
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
            result = sp.run(
                [latexmk, '-pdf', f'-output-directory="{proj_dir}"', file_name])
            if result.returncode != 0:
                # Something went wrong with the compilation (user error?)
                # Loop back to edition.
                error('Something went wrong with compiling the project.')
                failed = True
                break
            if failed:
                continue # to another edition pass.
            
            # Finished producing a PDF.
            # Now convert it to a white background PNG with imagemagick.
            pdf_name = os.path.splitext(file_name)[0] + '.pdf'
            png_name = os.path.splitext(file_name)[0] + '.png'
            density = arguments.get('--density', 300)
            result = sp.run([*magick, '-flatten', '-colorspace', 'RGB',
                '-background', 'white', '-density', density, pdf_name,
                png_name])

            if result.returncode != 0:
                error('Something went wrong with converting the PDF to a PNG.')
                log('Press any key to go back to edition.')
                input()
                failed = True
                continue # to another edition pass.
            # else: success

            # Copy the PNG into the clipboard
            result = copy(png_name)
            if result.returncode != 0:
                error('Something went wrong with copying the PNG to your '
                      'clipboard.')
                log('Press any key to go back to edition.')
                input()
                failed = True
                continue # to another edition pass.

            # loop to another edition pass

