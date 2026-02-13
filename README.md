[![Download InkRanker](https://img.shields.io/github/v/release/din0o0o/ink_ranker?label=Download&{color=ffeb3b&labelColor=2d2d2d&style=for-the-badge)](https://github.com/din0o0o/ink_ranker/releases/latest)

> # $\color{#ffeb3b}\{\textbf{InkRanker}}$ 
</br>

## $\color{#adf137}\textbf{File Structure}$ </br>

```
src/
├── main.py                    ¤ GUI, threading.
├── engine.py                  ¤ Parsing fonts, rendering, counting dark pixels.
├── config.ini                 ¤ User settings.
├── sample_text.txt            ¤ Text for rendering.
├── fonts.txt                  ¤ List of >300 fonts.
└── (output)                   ¤ Folder for scan ouput (.JSON, .docx)
```

#### $\color{#fff8dc}\text{Build from source:}$
```bash
pyinstaller InkRanker.spec
```

</br></br>
## $\color{#adf137}\text{Configuration}$ </br>
<code>config.ini</code> $\color{#fff8dc}\text{user configuration with default values:}$               
```
dpi                            ¤ Render resolution (300)
font_size                      ¤ Point size (12)
darkness_threshold             ¤ Dark pixel cutoff 0-255 (200)
baseline_font                  ¤ Reference font for indexing (Arial)
fonts_dir                      ¤ Path to user fonts (C:\Windows\Fonts)
line_spacing_factor            ¤ Line height (1.15)
sample_text                    ¤ Text for rendering (\sample_text.txt)
fonts_list                     ¤ Font list (\fonts.txt)
output_dir                     ¤ Output directory (\output)
```

</br></br>
## $\color{#adf137}\text{Procedure}$ </br>
<ol>
1. Reads user font directory, matches with <code>fonts.txt</code> </br>
2. Renders JPEG with <code>sample.txt</code> for each item found, using Pillow. </br>
3. Counts dark pixels in image using histogram. </br>
4. Font name, dark pixel value and index against baseline font in <code>output/results.JSON</code>, ranked table in <code>output/results.docx</code>. </br>
</ol> </br></br></br>

