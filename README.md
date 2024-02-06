# PicoDRO 
Micropython Pi Pico based Digital read out for small lathe etc.

This uses the PICO PIO for quadrature decoding and counting 
option will include
scrolling display for fractions of an inch
setting menu
quadrature output for combined inputs (e.g. for combining the knee and quill scales of a milling machine) 
logic/relay output when at zero


<p>Initial commit -   well that didn't go well! (pico folder structure lost completely on upload)</p>

<p>On the pico you will need:</p>
<p>lib (folder)</p>
<p>... fonts (folder)</p>
<p>... ... UMTruncated12X24.c</p>
<p>... mono_palette.py</p>
<p>... pio_quadrature_counter.py</p>
<p>... ssd1322.py</p>
<P>... xglcd_font.py</P>
<p>AboutScreen.py</p>
<p>ADCkeyboard.py</p>
<p>Inifile.py</p>
<p>MenuScreen.py</p>
<p>MenuSettings.py</p>
<p>OneAxisScreen.py</p>
<p>QuadratureIO.py</p>
<p>ScreenController_SSD1322.py</p>
<p>Screencontrols.py</p>
<p>TwoAxisScreen.py</p>
<p>Main.py (renamed from DRO Vxxx.py)</p>


<p>another file call Settings.JSON will be created on first run.</p>
