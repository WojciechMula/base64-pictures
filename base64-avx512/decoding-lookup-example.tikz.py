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


val0  = ord('d')
char0 = 'ASCII "d"'
byte0 = bin(val0)

val1  = ord('6')
char1 = 'ASCII "6"'
byte1 = bin(val1)

val2  = 0xff
char2 = r'\texttt{0xff}'
byte2 = bin(val2)

val3  = ord("C") | 0x80
char3 = r'\texttt{0x%02x}' % val3
byte3 = bin(val3)

val = [char0, char1, char2, char3]

color_a = 'red!25'
color_b = 'green!25'
color_c = 'blue!25'
color_d = 'yellow!25'

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

    color = get_color_from_label(label)
    if color:
        return 'fill=%s' % color

def apply_style(L, style):
    return [(label, style(index, label)) for index, label in enumerate(L)]

# drawing
##################################################

# 1. input four chars

y = 0
def mark_MSB(index, label):
    if index in [7, 15, 23, 31] and label == one:
        return 'fill=red'
    else:
        return 'thin'
 
chunk24 = byte0 + byte1 + byte2 + byte3
label(0.0, y, r"input --- four bytes")

draw (0.0, y + 0.3, apply_style(chunk24, mark_MSB))
byte_width = w*8
for i in xrange(4):
    x0 = i * byte_width
    x1 = x0 + byte_width
    horiz_brace(x0, x1, y + 0.3 + h, r"\footnotesize %s (byte %d)" % (val[3 - i], 3 - i))

y -= H + 0.5

# 2. translated vector

decoded0 = 29
decoded1 = 58
decoded2 = 0x80
decoded3 = 2 # "C"

decoded = bin(decoded0) + bin(decoded1) + bin(decoded2) + bin(decoded3)

label(0.0, y, r"translated input (result of \texttt{vpermi2b})")

byte_width = w*8
labels = [('a', decoded0), ('b', decoded1), ('c', decoded2 & 0x3f), ('d', decoded3 & 0x3f)]
for i, (l, v) in enumerate(reversed(labels)):
    x0 = i * byte_width + 2 * w
    x1 = x0 + 6 * w
    horiz_brace(x0, x1, y + 0.3 + h, r"\footnotesize field \texttt{%s} = \texttt{0x%02x}" % (l, v))

def style(index, label):
    if index in [7, 15, 23, 31] and label == one:
        return 'fill=red'
    elif index % 8 < 6:
        color = [color_a, color_b, color_c, color_d]
        return 'fill=%s' % color[index / 8]
    else:
        return 'thin'

draw (0.0, y + 0.3, apply_style(decoded, style))

# 2. error vector

y -= H

label(0.0, y, r"error = input \texttt{OR} translated input \texttt{OR} previous error (result of \texttt{vpternlogd})")
def mark_MSB(index, label):
    if index in [7, 15, 23, 31]:
        if label == zero:
            return 'fill=gray'
        else:
            return 'fill=red'
    else:
        return 'thin'

byte_ok    = ["--"] * 7 + [zero]
byte_error = ["--"] * 7 + [one]
error = byte_ok + byte_ok + byte_error + byte_error
draw (0.0, y + 0.3, apply_style(error, mark_MSB))

print "\\end{tikzpicture}"
