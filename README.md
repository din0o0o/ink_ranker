[![Download InkRanker](https://img.shields.io/github/v/release/din0o0o/ink_ranker?label=Download&color=ffeb3b&labelColor=2d2d2d&style=for-the-badge)](https://github.com/din0o0o/ink_ranker/releases/latest)

> # $\color{#ffeb3b}\{\textbf{InkRanker}}$ 
</br>

## $\color{#adf137}\textbf{File Structure}$ </br>

```
src/
├── main.py                    ¤ GUI, threading.
├── engine.py                  ¤ Parsing fonts, rendering, counting dark pixels.
├── sample.txt                 ¤ Text for rendering.
├── fonts.txt                  ¤ List of >300 fonts.
└── settings.py                ¤ Configurations called before compiling.
```

#### $\color{#fff8dc}\text{Build from source:}$
```bash
pyinstaller InkRanker.spec
```

</br></br>
## $\color{#adf137}\text{Configuration}$ </br>
<code>settings.py</code> $\color{#fff8dc}\text{for modifying values before compiling:}$               
```
DPI = 300                           # render resolution
FONT_SIZE = 12                      # point size for all fonts
DARKNESS_THRESHOLD = 200            # greyscale cutoff 0-255
BASELINE_FONT = "Arial"             # reference font for relative %
FONTS_DIR = r"C:\Windows\Fonts"     # system fonts directory
LINE_SPACING_FACTOR = 1.15          # line height multiplier
```

</br></br>
## $\color{#adf137}\text{Procedure}$ </br>
<ol>
1. Reads user font directory, matches with <code>fonts.txt</code> </br>
2. Renders greyscale image with <code>sample.txt</code> for each item found, using Pillow. </br>
3. Counts dark pixels in image using histogram. </br>
4. Outputs results in <code>results.JSON</code> and <code>results.docx</code>. </br>
</ol> </br></br></br>

