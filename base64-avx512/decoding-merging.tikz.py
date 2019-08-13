print "\\begin{tikzpicture}"

w = 0.4
h = 0.6
H = 1.4
byte_width = 8*w

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


one = '$1$'
zero = '$0$'

def bin(x):
    assert x >= 0 and x < 256
    result = []
    for i in xrange(8):
        if x & (1 << i):
            result.append(one)
        else:
            result.append(zero)

    return result


color_a = 'red!25'
color_b = 'green!25'
color_c = 'blue!25'
color_d = 'yellow!25'
color_e = 'gray!15'

field_A = ['$a_0$', '$a_1$', '$a_2$', '$a_3$', '$a_4$', '$a_5$']
field_B = ['$b_0$', '$b_1$', '$b_2$', '$b_3$', '$b_4$', '$b_5$']
field_C = ['$c_0$', '$c_1$', '$c_2$', '$c_3$', '$c_4$', '$c_5$']
field_D = ['$d_0$', '$d_1$', '$d_2$', '$d_3$', '$d_4$', '$d_5$']

def input_style(index, label):
    def get_color_from_label(label):
        if 'a' in label:
            return color_a
        if 'b' in label:
            return color_b
        if 'c' in label:
            return color_c
        if 'd' in label:
            return color_d
        if 'e' in label or 'f' in label:
            return color_e

    color = get_color_from_label(label)
    if color:
        return 'fill=%s' % color

def apply_style(L, style):
    return [(label, style(index, label)) for index, label in enumerate(L)]

# drawing
##################################################

y = 0

# 1. vertical lines marking bytes boundaries
for i in xrange(5):
    style = 'dotted'
    x  = i * byte_width
    y0 = y + 0.5
    y1 = y - 2.5*H
    print "\\draw [%s] (%0.2f, %0.2f) -- (%0.2f, %0.2f);" % (style, x, y0, x, y1)

# 2. input four 6-bit words

label(0.0, y, r"input --- 32-bit lane: four six-bit values \texttt{a}, \texttt{b}, \texttt{c} and \texttt{d} stored on separate bytes")

for i in xrange(4):
    x0 = i * byte_width
    x1 = x0 + byte_width
    horiz_brace(x0, x1, y + 0.3 + h, r"\footnotesize byte %d" % (3 - i))

byte0 = field_A + [zero] * 2
byte1 = field_B + [zero] * 2
byte2 = field_C + [zero] * 2
byte3 = field_D + [zero] * 2
input = byte0 + byte1 + byte2 + byte3

draw (0.0, y + 0.3, apply_style(input, input_style))

y -= H

# 3. joined 1

label(0.0, y, r"join and swap pairs of fields: \texttt{a} \& \texttt{b} and \texttt{c} \& \texttt{d} (result of \texttt{vpmaddubsw})")

word0 = field_B + field_A + [zero] * 4
word1 = field_D + field_C + [zero] * 4
join1 = word0 + word1
draw (0.0, y + 0.3, apply_style(join1, input_style))

y -= H

# 4. joined 2

label(0.0, y, r"join and swap 12-bit subfields (result of \texttt{vpmaddwd})")

join2 = field_D + field_C + field_B + field_A + [zero] * 8
draw (0.0, y + 0.3, apply_style(join2, input_style))

y -= H

# 5. merged

label(0.0, y, r"fixup order of bytes and omit 4th bytes from each lane (result of \texttt{vpermb})")
byte0 = join2[0:8]
byte1 = join2[8:16]
byte2 = join2[16:24]
byte3 = ['$f_4$', '$f_5$', '$e_0$', '$e_1$', '$e_2$', '$e_3$', '$e_4$', '$e_5$']
merged = byte2 + byte1 + byte0 + byte3
draw (0.0, y + 0.3, apply_style(merged, input_style))

print "\\end{tikzpicture}"
