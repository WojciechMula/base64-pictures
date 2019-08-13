print "\\begin{tikzpicture}"

w = 0.4
h = 0.6

byte0 = [
    "$a_5$", "$a_4$", "$a_3$", "$a_2$", "$a_1$", "$a_0$",
    "$b_5$", "$b_4$"
]

byte1 = [
    "$b_3$", "$b_2$", "$b_1$", "$b_0$", 
    "$c_5$", "$c_4$", "$c_3$", "$c_2$", 
]

byte2 = [
    "$c_1$", "$c_0$",
    "$d_5$", "$d_4$", "$d_3$", "$d_2$", "$d_1$", "$d_0$", 
]

# input triplet

y_in = 0
i = 0
for byte in [byte2, byte1, byte0]:
    for label in byte:
        x  = i * w
        i += 1

        style = "thin"
        if 'b' in label:
            style += ",fill=lightgray"
        elif 'c' in label:
            style += ",fill=gray"

        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y_in, x + w, y_in + h)

        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y_in + h/2, label)

for i in xrange(3):
    x = i*8*w
    print "\\draw [decorate,decoration={brace,amplitude=10pt}] (%0.2f, %0.2f) -- (%0.2f, %0.2f) node [midway,above,yshift=10pt] {\\footnotesize byte %d};" % (x, y_in + h, x + 8*w, y_in + h, 2 - i)


# shuffled 32-bit word

y_out = -2.0
i = 0
for byte in [byte1, byte2, byte0, byte1]:
    for label in byte:
        x  = i * w
        y  = y_out
        i += 1

        style = "thin"

        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)
        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)

for i, label in [(4, 'c'), (10, 'd'), (16, 'a'), (22, 'b')]:
    x = i*w
    y = y_out + h
    print "\\draw [decorate,decoration={brace,amplitude=10pt}] (%0.2f, %0.2f) -- (%0.2f, %0.2f) node [midway,above,yshift=10pt] {\\footnotesize field $%c$};" % (x, y, x + 6*w, y, label)

for i, byte in enumerate([1, 2, 0, 1]):
    x = i*8*w
    y = y_out
    print "\\draw [decorate,decoration={brace,mirror,amplitude=10pt}] (%0.2f, %0.2f) -- (%0.2f, %0.2f) node [midway,below,yshift=-10pt] {\\footnotesize byte %d};" % (x, y, x + 8*w, y, byte)

# final notes

print "\\node [below, fill=white] at (%0.2f, %0.2f) {24-bit chunk};" % (0, y_in)
print "\\node [above, fill=white] at (%0.2f, %0.2f) {shuffled word};" % (0, y_out + h)

print "\\end{tikzpicture}"
