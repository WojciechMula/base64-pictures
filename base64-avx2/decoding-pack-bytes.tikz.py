print "\\begin{tikzpicture}"

w = 0.4
h = 0.6
step = 1.4


def get_color_from_label(label):
    if label == "0":
        return "gray"
    else:
        return "white"


# mark word and byte boundaries across all steps

for i in xrange(32/4 + 1):
    if i % 4 == 0:
        style = "dashed"
    else:
        style = "dotted"

    x  = i*4*w
    y0 = 0
    y1 = -3*step - 0.4
    print "\\draw [%s] (%0.2f, %0.2f) -- (%0.2f, %0.2f);" % (style, x, y0, x, y1)


# input 32 bytes


def four_6bit_words(N):
    return ["\\small $%s_3$" % N, "\\small $%s_2$" % N, "\\small $%s_1$" % N, "\\small $%s_0$" % N]


input = four_6bit_words('h') + four_6bit_words('g') + four_6bit_words('f') + four_6bit_words('e') + \
        four_6bit_words('d') + four_6bit_words('c') + four_6bit_words('b') + four_6bit_words('a')

y_in = 0 * step
i = 0
for byte in [input]:
    for label in byte:
        x  = i * w
        y  = y_in
        i += 1

        style = "thin"
        if label != '0':
            color = get_color_from_label(label)
            style += ",fill=%s" % color

        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)
        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)

print "\\node [above right, fill=white] at (%0.2f, %0.2f) {%s};" % (0, y + h, "AVX2 register: 32 input 6-bit values stored in  separate bytes")

# step 1: pack into 24-bit


def packed_indices(N):
    return ["0", "\\tiny $%s_2$" % N, "\\tiny $%s_1$" % N, "\\tiny $%s_0$" % N]


input = packed_indices('H') + packed_indices('G') + packed_indices('F') + packed_indices('E') + \
        packed_indices('D') + packed_indices('C') + packed_indices('B') + packed_indices('A')

y_step1 = -1 * step
i = 0
for byte in [input]:
    for label in byte:
        x  = i * w
        y  = y_step1
        i += 1

        style = "thin,fill=%s" % get_color_from_label(label)

        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)

        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)

print "\\node [above right, fill=white] at (%0.2f, %0.2f) {%s};" % (0, y + h, "step 1: pack 6-bit indices into 24-bit words")


# step 2: shuffle bytes within indices

def indices(N):
    return ["\\tiny $%s_2$" % N, "\\tiny $%s_1$" % N, "\\tiny $%s_0$" % N]


input = ["0"]*4 + indices('H') + indices('G') + indices('F') + indices('E') + \
        ["0"]*4 + indices('D') + indices('C') + indices('B') + indices('A')

y_step2 = -2 * step
i = 0
for byte in [input]:
    for label in byte:
        x  = i * w
        y  = y_step2
        i += 1

        style = "thin,fill=%s" % get_color_from_label(label)

        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)
        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)

print "\\node [above right, fill=white] at (%0.2f, %0.2f) {%s};" % (0, y + h, "step 2: pack 24-bit words within 128-bit lanes (\\texttt{vpshufb})")


# step 3: shuffle dwords across lanes

input = ["0"]*8 + indices('H') + indices('G') + indices('F') + indices('E') + \
                  indices('D') + indices('C') + indices('B') + indices('A')

y_step3 = -3 * step
i = 0
for byte in [input]:
    for label in byte:
        x  = i * w
        y  = y_step3
        i += 1

        style = "thin,fill=%s" % get_color_from_label(label)

        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)
        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)

        bit = 31 - (i - 1)
        print '\\node [below] at (%0.2f, %0.2f) {\\footnotesize %d};' % (x + w/2, y, bit)

print "\\node [above right, fill=white] at (%0.2f, %0.2f) {%s};" % (0, y + h, "step 3: move 32-bit words across lanes (\\texttt{vpermd})")

print "\\end{tikzpicture}"
