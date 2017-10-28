
# -*- coding: utf-8 -*-

"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Draw the hyperbolic tiling of the Poincare upper plane
by fundamental domains of the modular group PSL_2(Z).
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A short introduction to the math behind this script:

PSL_2(Z) is an infinite group acts discretely on the upper plane by
fractional linear transformations:

              az + b
PSL_2(Z) = {  ------ , a,b,c,d in Z, ad-bc=1 }
              cz + d

This group has three generators A, B, C, where
A: z --> z+1
B: z --> z-1
C: z --> -1/z

Each element g in this group can be written as a word in ["A", "B", "C"],
for example "AAAAAC", "ACBBB", ...
To draw the hyperbolic tiling, one just starts from any fundamental domain D
(usually there is a classical choice of this domain), map it to g(D) for each
element g in the group (up to a given length), then draw all these g(D)s.
The main problem here is the word representation of g is generally not unique,
so it's not obvious how to traverse each element only once without omitting any.

Here is the deep math: the modular group is an automatic group, i.e.
there exists a DFA such that the words accepted by the DFA are eactly
the elements of the group under the shortest-lex-order representation,
thus finding all elements in this group amounts to traversing a finite
directed graph, which is a much easier job. (we will use breadth-first search here)
"""

import collections
import cmath,math
import cairocffi as cairo


# None means 'infinity'
def A(z):
    return None if z is None else z+1

def B(z):
    return None if z is None else z-1

def C(z):
    if z is None:
        return 0j
    elif z == 0j:
        return None
    else:
        return -1/z


def transform(symbol, domain):
    # A domain is specified by a list of comlex numbers on its boundary.
    func = {'A': A, 'B': B, 'C': C}[symbol]
    return [func(z) for z in domain]


def transformFull(word,domain):
    temp = domain
    for symbol in word:
        temp = transform(symbol,temp)

    return temp


# The automaton that generates all words in the modular group,
# 0 is the starting state.
# Each element g correspondes to a unique path starts from 0.
# for example the path
# 0 --> 1 --> 3 -- > 4 --> 8
# correspondes to the element "ACAA" because the first step takes 0 to 1 is
# labelled by "A", the second step takes 1 to 3 is labelled by "C",
# the third step takes 3 to 4 is labelled by "A", ...
automaton = {0: {'A': 1, 'B': 2, 'C': 3},
             1: {'A': 1, 'C': 3},
             2: {'B': 2, 'C': 3},
             3: {'A': 4, 'B': 5},
             4: {'A': 8},
             5: {'B': 6},
             6: {'B': 2, 'C': 7},
             7: {'A': 4},
             8: {'A': 1, 'C': 9},
             9: {'B': 5}
            }


def traverse(length, start_domain):
    queue = collections.deque([('', 0, start_domain)])
    while queue:
        word, state, domain = queue.popleft()
        yield word, state, domain

        if len(word) < length:
            for symbol, to in automaton[state].items():
                queue.append((word + symbol, to, transform(symbol, domain)))

width = 1600
height = 800

class HyperbolicDrawing(cairo.Context):
    """A quick extension of the `cairo.Context` class for drawing hyperbolic
    objects in the Poincare upper plane.
    """
    def set_axis(self, **kwargs):
        surface = self.get_target()
#        width = surface.width
#        height = surface.height

        xlim = kwargs.get('xlim', [-2, 2])
        x_min, x_max = xlim
        ylim = kwargs.get('ylim', [0, 2])
        y_min, y_max = ylim

        self.scale(width * 1.0 / (x_max - x_min),
                   height * 1.0 / (y_min - y_max))
        self.translate(abs(x_min), -y_max)

        bg_color = kwargs.get('background_color', (1, 1, 1))
        self.set_source_rgb(*bg_color)
        self.paint()

    def arc_to(self, x1, y1):
        x0, y0 = self.get_current_point()
        dx, dy = x1 - x0, y1 - y0

        if abs(dx) < 1e-8:
            self.line_to(x1, y1)

        else:
            center = 0.5 * (x0 + x1) + 0.5 * (y0 + y1) * dy / dx
            theta0 = cmath.phase(x0 - center + y0*1j)
            theta1 = cmath.phase(x1 - center + y1*1j)
            r = abs(x0 - center + y0*1j)

            # we must ensure that the arc ends at (x1, y1)
            if x0 < x1:
                self.arc_negative(center, 0, r, theta0, theta1)
            else:
                self.arc(center, 0, r, theta0, theta1)

    def draw_text(self,position,text,size):
        self.set_font_size(size)
        self.move_to(position.real,position.imag)
        self.show_text(text)

    def render_domain(self, domain, facecolor=None,
                      edgecolor=(0, 0, 0), linewidth=0.01):
        # the points defining the domain may contain the infinity (None).
        # In this program the infinity always appear at the end,
        # we use 10000 as infinity when drawing lines.
        x0, y0 = domain[0].real, domain[0].imag
        if domain[-1] is None:
            x1 = domain[-2].real
            domain = domain[:-1] + [x1 + 10000*1j, x0 + 10000*1j]

        self.move_to(x0, y0)
        for z in domain[1:]:
            self.arc_to(z.real, z.imag)
        self.arc_to(x0, y0)

        if facecolor:
            self.set_source_rgb(*facecolor)
            self.fill_preserve()

        self.set_line_width(linewidth)
        self.set_source_rgb(*edgecolor)
        self.stroke()




length = 15
fund_domain = [cmath.exp(cmath.pi*1j/3), cmath.exp(cmath.pi*2j/3), None]

surface = cairo.PDFSurface("modulargroup.pdf", width, height)
ctx = HyperbolicDrawing(surface)
ctx.set_axis(xlim=[-2, 2], ylim=[0, 2], background_color=(1, 1, 1))
ctx.set_line_join(2)
# draw the x-axis
ctx.move_to(-2, 0)
#ctx.line_to(2, 0)
ctx.set_source_rgb(0, 0, 0)
ctx.set_line_width(0.03)
ctx.stroke()

for word, state, triangle in traverse(length, fund_domain):
    #if word:
    if True:
#        if word[0] == 'C':
        if ((word.count('A') - word.count('B')) % 2 == 0):
            fc_color = (0.8, 0.8, 0.8)
        else:
            fc_color = None
    else:
        fc_color = (0.5, 0.5, 0.5)

    ctx.render_domain(triangle, facecolor=fc_color, linewidth=0.01*math.exp(-0.5*word.count('C')))

    if(len(word) < 0):
        domain_middle = transformFull(word,[1j])[0]
        ctx.draw_text(domain_middle,word,0.3)

#surface.write_to_png('modulargroup.png')
