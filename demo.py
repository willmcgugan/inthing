"""An example of posting a text event to a stream."""

from inthing import Stream


def mandel(xsize=80, ysize=20, max_iteration=50):
    """Render an ascii mandelbrot set!"""
    chars = " .,~:;+*%@##"
    rows = []
    for pixy in xrange(ysize):
        y0 = (float(pixy) / ysize) * 2 - 1
        row = ""
        for pixx in xrange(xsize):
            x0 = (float(pixx) / xsize) * 3 - 2
            x = 0
            y = 0
            iteration = 0
            while (x * x + y * y < 4) and iteration < max_iteration:
                xtemp = x * x - y * y + x0
                y = 2 * x * y + y0
                x = xtemp
                iteration += 1
            row += chars[iteration % 10]
        rows.append(row)
    return "```\n{}\n```\n#mandlebrot".format('\n'.join(rows))


stream = Stream.new()
result = stream.text(mandel(), title="Mandelbrot Set!")
result.browse()
