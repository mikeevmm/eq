# eq

## Install

**Consider using [`pipx`][pipx].**

```bash
pipx install git+https://github.com/mikeevmm/eq/
```

Otherwise, if you are using `pip`:

```bash
pip install git+https://github.com/mikeevmm/eq/
```

## Requirements

`eq` requires `xclip`, `imagemagick`, and `latexmk` (**Linux**) or `nircmd`, `imagemagick`, `latexmk`, and `ghostscript` (**Windows**). 

## How to Use

```
eq [--density=<n>]
```

`eq` will launch your default editor (and fallback on `$VISUAL`, `$EDITOR`, `vim`, `nano`, in that order). Write your equation (and edit the LaTeX file as required), and quit. Your equation will be compiled and copied to your clipboard.

If `eq` detects that you did not change your file, it quits.

The `--density` option determines the quality of your PDF to PNG conversion. Set a higher number for a crisper image. (Default value is 300.)

## Details

### ImageMagick Error

```
...: attempt to perform an operation not allowed by the securiy policy `PDF' @...
```

If you see the above message, then ImageMagick is blocking the conversion from PDF to PNG due to a security vulnerability in Ghostscript. However, this vulnerability was patched in Ghostscript 9.24, so if your software is up-to-date, you can safely unblock this conversion.

[See this StackOverflow answer for a fix.](https://stackoverflow.com/a/59193253)

## Contributing

Pull requests are welcome. Issues are not guaranteed to be addressed. `eq` is
built primarily for self-use, provided to you for free, and not my primary
occupation. Please respect this.

## Licence

`eq` is licenced under a GNU General Public License, version 2. This
[**informally**][GPLv2] means that:

> You may copy, distribute and modify the software as long as you track
> changes/dates in source files. Any modifications to or software including
> (via compiler) GPL-licensed code must also be made available under the GPL
> along with build & install instructions.

You can find a copy of the licence under `LICENCE`.

## Support

💕 If you like and use `eq`, consider
[buying me a coffee](https://www.paypal.me/miguelmurca/2.50).

[pipx]: https://github.com/pypa/pipx
[GPLv2]: https://tldrlegal.com/license/gnu-general-public-license-v2
