print "\\begin{tikzpicture}"

w = 0.4
h = 0.6

# input register

def get_input_label(i):
    if i < 4 or i >= 28:
        return

    L = "ABCDEFGH"
    i = i - 4
    letter = L[i/3]
    index  = i % 3

    return '\\tiny $%c_%d$' % (letter, index)

y_in = 0
for i in xrange(32):
    x = i * w
    label = get_input_label(i)
    if label:
        style = "thin"
    else:
        style = "fill=gray"
    print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y_in, x + w, y_in + h)
    if label:
        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y_in + h/2, label)


# shuffled register

def get_shuffled_label(i):
    L = "ABCDEFGH"
    letter = L[i/4]
    t = i % 4
    if t == 0:
        index = 1
    if t == 1:
        index = 0
    if t == 2:
        index = 2
    if t == 3:
        index = 1

    return '\\tiny $%c_%d$' % (letter, index)

y_out = -1.75
for i in xrange(32):
    x = i * w
    print '\\draw [thin] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (x, y_out, x + w, y_out + h)
    label = get_shuffled_label(i)
    print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y_out + h/2, label)


# show how 3-byte words are expanded into 4-byte words

for i in xrange(9):
    x0 = (i*3 + 4)*w
    y0 = y_in

    x1 = (i*4*w)
    y1 = y_out + h
    print '\\draw [dotted] (%0.2f, %0.2f) -- (%0.2f, %0.2f);' % (x0, y0, x1, y1)


# some additional marks

print "\\draw [decorate,decoration={brace,amplitude=10pt}] (%0.2f, %0.2f) -- (%0.2f, %0.2f) node [midway,above,yshift=10pt] {\\footnotesize lower 128-bit lane of AVX2 register};" % (0, y_in + h, 16*w, y_in + h)
print "\\draw [decorate,decoration={brace,amplitude=10pt}] (%0.2f, %0.2f) -- (%0.2f, %0.2f) node [midway,above,yshift=10pt] {\\footnotesize higher 128-bit lane};" % (16*w, y_in + h, 32*w, y_in + h)

print "\\node [fill=white] at (%0.2f, %0.2f) {\\footnotesize shuffle eight 3-byte words using \\texttt{vpshufb}};" % (16*w, (y_in + y_out + h)/1.5)

for i in [0, 15, 16, 31]: # label selected bytes on output register
    print "\\node at (%0.2f, %0.2f) [below] {\\footnotesize {%s}};" % (i*w + w/2, y_in, str(i))

print "\\end{tikzpicture}"
