print "\\begin{tikzpicture}"

w = 0.4
h = 0.6
step = 1.4

null = ["0", "0", "0", "0", "0", "0", "0", "0"]

bare_a = ["$a_5$", "$a_4$", "$a_3$", "$a_2$", "$a_1$", "$a_0$"]
bare_b = ["$b_5$", "$b_4$", "$b_3$", "$b_2$", "$b_1$", "$b_0$"]
bare_c = ["$c_5$", "$c_4$", "$c_3$", "$c_2$", "$c_1$", "$c_0$"]
bare_d = ["$d_5$", "$d_4$", "$d_3$", "$d_2$", "$d_1$", "$d_0$"]

field_a = ["0", "0"] + bare_a
field_b = ["0", "0"] + bare_b
field_c = ["0", "0"] + bare_c
field_d = ["0", "0"] + bare_d

fields_cd = ["0", "0", "0", "0"] + bare_c + bare_d
fields_ab = ["0", "0", "0", "0"] + bare_a + bare_b

all_fields = null + bare_a + bare_b + bare_c + bare_d

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
    y1 = -2*step - 0.4
    print "\\draw [%s] (%0.2f, %0.2f) -- (%0.2f, %0.2f);" % (style, x, y0, x, y1)


# shuffled 32-bit word

y_in = 0 * step
i = 0
for byte in [field_d, field_c, field_b, field_a]:
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

print "\\node [above right, fill=white] at (%0.2f, %0.2f) {%s};" % (0, y + h, "four input indices")

# step 1: merge and swap adjacent fields

y_step1 = -1 * step
i = 0
for byte in [fields_cd, fields_ab]:
    for label in byte:
        x  = i * w
        y  = y_step1
        i += 1

        style = "thin"
        if label != '0':
            color = get_color_from_label(label)
            style += ",fill=%s" % color

        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)

        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)

print "\\node [above right, fill=white] at (%0.2f, %0.2f) {%s};" % (0, y + h, "step 1: swap and merge adjacent 6-bit fields (\\texttt{vpmaddubsw})")

# step 2: merge 12-bit fields into a 24-bit word

y_step2 = -2 * step
i = 0
for byte in [all_fields]:
    for label in byte:
        x  = i * w
        y  = y_step2
        i += 1

        style = "thin"
        if label != '0':
            style += ",fill=%s" % get_color_from_label(label)

        print '\\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' % (style, x, y, x + w, y + h)
        print '\\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, label)

        bit = 31 - (i - 1)
        print '\\node [below] at (%0.2f, %0.2f) {\\footnotesize %d};' % (x + w/2, y, bit)

print "\\node [above right, fill=white] at (%0.2f, %0.2f) {%s};" % (0, y + h, "step 2: swap and merge 12-bit words into a 24-bit word (\\texttt{vpmaddbw})")

print "\\end{tikzpicture}"
