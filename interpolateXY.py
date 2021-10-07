"""Abaqus CAE plugin to interpolate values on current xy plot

Carl Osterwisch, October 2021
"""

from __future__ import print_function
import numpy as np

def interp_roots(xy):
    """Linear interpolation to estimate all x where y=0

    >>> x = np.array(range(20))

    These roots are exactly at provided points:
    >>> interp_roots(np.transpose( [x, (x - 10.)*(x - 12)] ))
    array([ 10.,  12.])

    Some loss of accuracy between points of nonlinear function:
    >>> np.set_printoptions(precision=3)
    >>> interp_roots(np.transpose( [x, (x - 8.5)*(x - 18.2)] ))
    array([  8.526,  18.184])
    """

    xy = np.asarray(xy)
    i = (( xy[1:]*xy[:-1] )[:,1] <= 0).nonzero()[0] # indices where y crosses zero
    roots = []
    for (x0, y0), (x1, y1) in zip(xy[i], xy[i + 1]):
        if y0 == y1:
            roots.append( x0 )
        else:
            roots.append( x0 - y0/(y1 - y0)*(x1 - x0) ) # linear interpolation
    return np.unique(roots)


def interp(xy, x):
    """Interpolate to find y values within xy array at coordinate x

    Example on top of an existing point:
    >>> xy = np.array([[0, 10], [10, 11]])
    >>> interp(xy, x=10)
    array([ 11.])

    Example between two points:
    >>> interp(xy, x=5)
    array([ 10.5])

    Note that this method does not extrapolate:
    >>> interp(xy, x=12)
    array([], dtype=float64)
    """

    yx = np.asarray(xy, dtype=np.float64)[:, [1, 0]] # swap x and y
    return interp_roots(yx - [0, x])


def fromViewer(x):
    """Called by Abaqus CAE to interpolate data in current xyPlot
    """

    from abaqus import session, getWarningReply, YES, YES_TO_ALL, CANCEL
    vp = session.viewports[session.currentViewportName]
    xyPlot = vp.displayedObject
    if not hasattr(xyPlot, 'charts'):
        return CANCEL != getWarningReply(
                'You must display an XY Plot in the current viewport',
                (CANCEL, )
                )
    chart = xyPlot.charts.values()[0]
    print('Interpolating values at x =', x)
    for curve in chart.curves.values():
        values = interp(curve.data.data, x)
        print(*([curve.legendLabel] + list(values)), sep='\t')
    return len(chart.curves.values())


def pointsFromViewer(points):
    "Accept an array of points from Viewer"
    for point in points:
        if not fromViewer(point[0]):
            break


if __name__ == '__main__':
    import doctest
    doctest.testmod()
