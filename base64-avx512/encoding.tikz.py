print "\\begin{tikzpicture}"

w = 0.4
h = 0.6
H = 1.4

def draw(X, Y, items):
    x = float(X)
    y = float(Y)
    default_style = 'thin'
    for item in reversed(items):
        try:
            label, style = item
            if style is None:
                style = default_style
        except ValueError:
            label = item
            style = default_style
            
        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)
        if label:
            print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)
        
        x += w


def label(X, Y, label):
    x = float(X)
    y = float(Y)
    print '\\node [below, right, fill=white] at (%0.2f, %0.2f) {%s};' % (x, y, label)


def horiz_brace(x0, x1, y, label):
    print "\\draw [decorate,decoration={brace,amplitude=10pt}] (%0.2f, %0.2f) -- (%0.2f, %0.2f) node [midway,above,yshift=10pt] {%s};" % (x0, y, x1, y, label)


field_A = ['$a_0$', '$a_1$', '$a_2$', '$a_3$', '$a_4$', '$a_5$']
field_B = ['$b_0$', '$b_1$', '$b_2$', '$b_3$', '$b_4$', '$b_5$']
field_C = ['$c_0$', '$c_1$', '$c_2$', '$c_3$', '$c_4$', '$c_5$']
field_D = ['$d_0$', '$d_1$', '$d_2$', '$d_3$', '$d_4$', '$d_5$']

byte0 = field_B[4:6] + field_A[0:6]
byte1 = field_C[2:6] + field_B[0:4]
byte2 = field_D[0:6] + field_C[0:2]

color_a = 'red!25'
color_b = 'green!25'
color_c = 'blue!25'
color_d = 'yellow!25'

def input_style(label):
    def get_color_from_label(label):
        if 'a' in label:
            return color_a
        if 'b' in label:
            return color_b
        if 'c' in label:
            return color_c
        if 'd' in label:
            return color_d

    color = get_color_from_label(label)
    if color:
        return 'fill=%s' % color

def apply_style(L, style):
    return [(label, style(label)) for label in L]

# drawing
##################################################

# 1. input 24-bit word

y = 0
 
chunk24 = byte0 + byte1 + byte2
label(0.0, y, r"input 24-bit word consisting 6-bit values \texttt{a}, \texttt{b}, \texttt{c} and \texttt{d}")

draw (0.0, y + 0.3, apply_style(chunk24, input_style))
byte_width = w*8
for i in xrange(3):
    x0 = i * byte_width
    x1 = x0 + byte_width
    horiz_brace(x0, x1, y + 0.3 + h, r"\footnotesize byte %d" % (2 - i))

y -= H + 0.5 # extra space for braces

# 2. vertical lines marking bytes boundaries
for i in xrange(5):
    style = 'dotted'
    x  = i * byte_width
    y0 = y + 0.5
    y1 = y - 2.5*H
    print "\\draw [%s] (%0.2f, %0.2f) -- (%0.2f, %0.2f);" % (style, x, y0, x, y1)


# 3. shuffled bytes

shuffled = byte1 + byte0 + byte2 + byte1
label(0.0, y, r"intermediate 32-bit word (result of \texttt{vpermb})")
draw (0.0, y + 0.3, apply_style(shuffled, input_style))
for i, byte in enumerate(reversed([1, 0, 2, 1])):
    x0 = i * byte_width
    x1 = x0 + byte_width
    horiz_brace(x0, x1, y + 0.3 + h, r"\footnotesize byte %d" % (byte,))


# 4. shifted fields

y -= H

shifted = []
for shift in [10, 4, 22, 16]:
    shifted.extend(shuffled[shift:shift+8])

label(0.0, y, r"values \texttt{a}, \texttt{b}, \texttt{c} and \texttt{d} moved to separate bytes (result of \texttt{vpmultishiftqb})")
draw (0.0, y + 0.3, apply_style(shifted, input_style))

# 5. masked inputs

y -= H

shifted_masked = []
for i, bit in enumerate(shifted):
    if i % 8 < 6:
        shifted_masked.append(bit)
    else:
        shifted_masked.append('')
label(0.0, y, r"six lower bits of each byte used by the subsequent \texttt{vpermb}")
draw (0.0, y + 0.3, apply_style(shifted_masked, input_style))

# 6. result 

y -= H

w = w*8
label(0.0, y, r"values \texttt{a}, \texttt{b}, \texttt{c} and \texttt{d} converted to ASCII characters (result of \texttt{vpermb})")
draw (0.0, y + 0.3, apply_style([r"$\textrm{ASCII}(\texttt{%s})$" % f for f in "abcd"], input_style))

print "\\end{tikzpicture}"
