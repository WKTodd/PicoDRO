"""XGLCD Font Utility."""
from math import floor
from framebuf import FrameBuffer, MONO_VLSB  # type: ignore


class XglcdFont(object):
    """Font data in X-GLCD format.

    Attributes:
        letters: A bytearray of letters (columns consist of bytes)
        width: Maximum pixel width of font
        height: Pixel height of font
        start_letter: ASCII number of first letter
        height_bytes: How many bytes comprises letter height

    Note:
        Font files can be generated with the free version of MikroElektronika
        GLCD Font Creator:  www.mikroe.com/glcd-font-creator
        The font file must be in X-GLCD 'C' format.
        To save text files from this font creator program in Win7 or higher
        you must use XP compatibility mode or you can just use the clipboard.
    """

    def __init__(self, path, width, height, start_letter=32, letter_count=96):
        """Constructor for X-GLCD Font object.

        Args:
            path (string): Full path of font file
            width (int): Maximum width in pixels of each letter
            height (int): Height in pixels of each letter
            start_letter (int): First ACII letter.  Default is 32.
            letter_count (int): Total number of letters.  Default is 96.
        """
        self.width = width
        self.height = height
        self.start_letter = start_letter
        self.letter_count = letter_count
        self.bytes_per_letter = (floor(
            (self.height - 1) / 8) + 1) * self.width + 1
        self.__load_xglcd_font(path)

    def __load_xglcd_font(self, path):
        """Load X-GLCD font data from text file.

        Args:
            path (string): Full path of font file.
        """
        bytes_per_letter = self.bytes_per_letter
        # Buffer to hold letter byte values
        self.letters = bytearray(bytes_per_letter * self.letter_count)
        mv = memoryview(self.letters)
        offset = 0
        with open(path, 'r') as f:
            
          line = f.readline()
          while line:
                #print(line)
                # Skip lines that do not start with hex values
                line = line.strip()
                if len(line) == 0 or line[0:2] != '0x':
                    line = f.readline()
                    continue
                # Remove comments
                comment = line.find('//')
                if comment != -1:
                    line = line[0:comment].strip()
                # Remove trailing commas
                if line.endswith(','):
                    line = line[0:len(line) - 1]
                # Convert hex strings to bytearray and insert in to letters
                mv[offset: offset + bytes_per_letter] = bytearray(
                    int(b, 16) for b in line.split(','))
                offset += bytes_per_letter
                
                line = f.readline()

                
    def readbinaryline(self,f):
      s = ""
      while True:        
        b = f.read(1)
        #print(f"{b} ", end="")
        if b:
          b = ord(b)
          if b >= 0x7F : s += "[0x{:02X}]".format(b)
          else         : s += chr(b)
          if b == 0x0A : return s
        else:
          return s
                
    def get_letter(self, letter, rotate=0):
        """Convert letter byte data to pixels.

        Args:
            letter (string): Letter to return (must exist within font).
            rotate (int): rotation (default: 0)
        Returns:
            (FrameBuffer): Pixel data in MONO_VLSB.
            (int, int): Letter width and height.
        """
        # Get index of letter
        letter_ord = ord(letter) - self.start_letter
        # Confirm font contains letter
        if letter_ord >= self.letter_count:
            print('Font does not contain character: ' + letter)
            return b'', 0, 0
        bytes_per_letter = self.bytes_per_letter
        offset = letter_ord * bytes_per_letter
        mv = memoryview(self.letters[offset:offset + bytes_per_letter])

        # Get width of letter (specified by first byte)
        width = mv[0]
        height = self.height
        byte_height = (height - 1) // 8 + 1  # Support fonts up to 5 bytes high
        if byte_height > 6:
            print("Error: maximum font byte height equals 6.")
            return b'', 0, 0
        array_size = width * byte_height
        ba = bytearray(mv[1:array_size + 1])
        # Set inversion and re-order bytes if height > 1 byte
        pos = 0
        ba2 = bytearray(array_size)

        for i in range(0, array_size, byte_height):
            ba2[pos] = ba[i]
            if byte_height > 1:
                ba2[pos + width] = ba[i + 1]
            if byte_height > 2:
                ba2[pos + width * 2] = ba[i + 2]
            if byte_height > 3:
                ba2[pos + width * 3] = ba[i + 3]
            if byte_height > 4:
                ba2[pos + width * 4] = ba[i + 4]
            if byte_height > 5:
                ba2[pos + width * 5] = ba[i + 5]
            pos += 1

        fb = FrameBuffer(ba2, width, height, MONO_VLSB)

        if rotate == 0:  # 0 degrees
            return fb, width, height
        elif rotate == 90:  # 90 degrees
            byte_width = (width - 1) // 8 + 1
            adj_size = height * byte_width
            fb2 = FrameBuffer(bytearray(adj_size), height, width, MONO_VLSB)
            for y in range(height):
                for x in range(width):
                    fb2.pixel(y, x, fb.pixel(x, (height - 1) - y))
            return fb2, height, width
        elif rotate == 180:  # 180 degrees
            fb2 = FrameBuffer(bytearray(array_size), width, height, MONO_VLSB)
            for y in range(height):
                for x in range(width):
                    fb2.pixel(x, y,
                              fb.pixel((width - 1) - x, (height - 1) - y))
            return fb2, width, height
        elif rotate == 270:  # 270 degrees
            byte_width = (width - 1) // 8 + 1
            adj_size = height * byte_width
            fb2 = FrameBuffer(bytearray(adj_size), height, width, MONO_VLSB)
            for y in range(height):
                for x in range(width):
                    fb2.pixel(y, x, fb.pixel((width - 1) - x, y))
            return fb2, height, width

    def measure_text(self, text, spacing=1):
        """Measure length of text string in pixels.

        Args:
            text (string): Text string to measure
            spacing (optional int): Pixel spacing between letters.  Default: 1.
        Returns:
            int: length of text
        """
        length = 0
        for letter in text:
            # Get index of letter
            letter_ord = ord(letter) - self.start_letter
            offset = letter_ord * self.bytes_per_letter
            # Add length of letter and spacing
            length += self.letters[offset] + spacing
        return length

#example
#font = XglcdFont('/lib/fonts/IBMPlexMono12x24.c', 12, 24)
#font = XglcdFont('lib/fonts/Unispace12x24.c', 12, 24)
#font = XglcdFont('lib/fonts/ArcadePix9x11.c', 9, 11)
# font = XglcdFont('lib/fonts/Roboto_18x22.c', 18, 22)
# font = XglcdFont('lib/fonts/IBMPlexMono12x24.c', 12, 24)
# font = XglcdFont('lib/fonts/UbuntuMono12x24.c', 12, 24)
#font = XglcdFont('lib/fonts/UMTruncated12x24.c', 12, 24)
# font = XglcdFont('lib/fonts/PerfectPixel_18x25.c', 18, 25)
# font = XglcdFont('lib/fonts/PerfectPixel_23x32.c', 23, 32)
# font = XglcdFont('lib/fonts/Broadway17x15.c', 17, 15)
# font = XglcdFont('lib/fonts/EspressoDolce18x24.c', 18, 24)
# font = XglcdFont('lib/fonts/Robotron13x21.c', 13, 21)
# font = XglcdFont('lib/fonts/Robotron7x11.c', 7, 11)
# font2 = XglcdFont('lib/fonts/Bally5x8.c', 5, 8)
# font2 = XglcdFont('lib/fonts/Bally7x9.c', 7, 9)
# font2 = XglcdFont('lib/fonts/NeatoReduced5x7.c', 5, 7)
# font2 = XglcdFont('lib/fonts/FixedFont5x8.c', 5, 8)
