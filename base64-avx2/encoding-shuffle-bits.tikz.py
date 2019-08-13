print "\\begin{tikzpicture}"

w = 0.4
h = 0.6
step = 1.4

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

null = ["0", "0", "0", "0", "0", "0", "0", "0"]

field_a = ["0", "0", "$a_5$", "$a_4$", "$a_3$", "$a_2$", "$a_1$", "$a_0$"]
field_b = ["0", "0", "$b_5$", "$b_4$", "$b_3$", "$b_2$", "$b_1$", "$b_0$"]
field_c = ["0", "0", "$c_5$", "$c_4$", "$c_3$", "$c_2$", "$c_1$", "$c_0$"]
field_d = ["0", "0", "$d_5$", "$d_4$", "$d_3$", "$d_2$", "$d_1$", "$d_0$"]

color_a = 'red!30'
color_b = 'green!30'
color_c = 'blue!30'
color_d = 'magenta!30'

def get_color_from_label(label):
    if 'a' in label:
        return color_a
    if 'b' in label:
        return color_b
    if 'c' in label:
        return color_c
    if 'd' in label:
        return color_d


# mark word and byte boundaries across all steps

for i in xrange(5):
    if i % 2 == 0:
        style = "dashed"
    else:
        style = "dotted"

    x  = i*8*w
    y0 = 0
    y1 = -5*step - 0.4
    print "\\draw [%s] (%0.2f, %0.2f) -- (%0.2f, %0.2f);" % (style, x, y0, x, y1)


# shuffled 32-bit word

y_in = 0 * step
i = 0
for byte in [byte1, byte2, byte0, byte1]:
    for label in byte:
        x  = i * w
        y  = y_in
        i += 1

        style = "thin"
        if not (i > 4 and i <= 28):
            color = 'gray'
        else:
            color = get_color_from_label(label)

        style += ",fill=%s" % color
        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)
        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)

print "\\node [above right, fill=white] at (%0.2f, %0.2f) {%s};" % (0, y + h, "input 32-bit word")

# step 1: mask c and a

y_step1 = -1 * step
i = 0
for byte in [byte1, byte2, byte0, byte1]:
    for label in byte:
        x  = i * w
        y  = y_step1
        i += 1

        style = "thin"
        if (i > 4 and i <= 10) or (i > 16 and i <= 22):
            style += ",fill=%s" % get_color_from_label(label)
        else:
            label = '0'

        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)

        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)

print "\\node [above right, fill=white] at (%0.2f, %0.2f) {%s};" % (0, y + h, "step 1a: mask fields $c$ and $a$ (\\texttt{vpand})")

# step 2: shift c and a

y_step2 = -2 * step
i = 0
for byte in [null, field_c, null, field_a]:
    for label in byte:
        x  = i * w
        y  = y_step2
        i += 1

        style = "thin"
        if label != '0':
            style += ",fill=%s" % get_color_from_label(label)

        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)
        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)

print "\\node [above right, fill=white] at (%0.2f, %0.2f) {%s};" % (0, y + h, "step 1b: shift right $c$ by 6 and $a$ by 10 bits (\\texttt{vpmulhuw})")


# step 3: mask d and b

y_step3 = -3 * step
i = 0
for byte in [byte1, byte2, byte0, byte1]:
    for label in byte:
        x  = i * w
        y  = y_step3
        i += 1

        style = "thin"
        if (i > 10 and i <= 16) or (i > 22 and i <= 28):
            style += ",fill=%s" % get_color_from_label(label)
        else:
            label = '0'

        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)

        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)

print "\\node [above right, fill=white] at (%0.2f, %0.2f) {%s};" % (0, y + h, "step 2a: mask fields $d$ and $b$ (\\texttt{vpand})")


# step 4: shift d and b left

y_step4 = -4 * step
i = 0
for byte in [field_d, null, field_b, null]:
    for label in byte:
        x  = i * w
        y  = y_step4
        i += 1

        style = "thin"
        if label != '0':
            style += ",fill=%s" % get_color_from_label(label)

        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)

        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)

print "\\node [above right, fill=white] at (%0.2f, %0.2f) {%s};" % (0, y + h, "step 2b: shift left $d$ by 8 bits, and $b$ by 4 bits (\\texttt{vpmullw})")


# step 5: merge steps 2 and 4

y_step5 = -5 * step
i = 0
for byte in [field_d, field_c, field_b, field_a]:
    for label in byte:
        x  = i * w
        y  = y_step5
        i += 1

        style = "thin"
        if label != '0':
            color = get_color_from_label(label)

            style += ",fill=%s" % color

        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)
        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)

        bit = 31 - (i - 1)
        print '\\node [below] at (%0.2f, %0.2f) {\\footnotesize %d};' % (x + w/2, y, bit)

print "\\node [above right, fill=white] at (%0.2f, %0.2f) {%s};" % (0, y + h, "step 3: merge results from step 1b and 2b (\\texttt{vpor})")

print "\\end{tikzpicture}"
