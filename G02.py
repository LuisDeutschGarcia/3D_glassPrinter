import numpy as np

# x1, x2, y1, y2 = 10,110,45,60
# Rinput = 55
# resolution = 80

def arcInterpolation(x1, x2, y1, y2, Rinput, resolution=15, G02=True):
    Xchord = (x2 + x1) / 2
    Ychord = (y2 + y1) / 2

    Rmin = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / 2
    slope = np.sqrt(Rinput ** 2 - Rmin ** 2)
    Run = (np.abs(x1 - x2) / 2 * slope) / Rmin
    Rise = (np.abs(y2 - y1) / 2 * Run) / (np.abs(x1 - x2) / 2)
    theta = np.arccos(slope / Rinput)
    alfa = theta * 2
    beta = alfa / resolution

    Xc = 0
    Yc = 0
    if G02:
        if x1 < x2 and y1 < y2:
            Xc = Xchord + Rise
            Yc = Ychord - Run
        if x1 < x2 and y1 > y2:
            Xc = Xchord - Rise
            Yc = Ychord - Run
        if x1 > x2 and y1 > y2:
            Xc = Xchord - Rise
            Yc = Ychord + Run
        if x1 > x2 and y1 < y2:
            Xc = Xchord + Rise
            Yc = Ychord + Run
        if x1 == x2 and y1 < y2:
            Xc = Xchord + slope
            Yc = Ychord
        if x1 == x2 and y1 > y2:
            Xc = Xchord - slope
            Yc = Ychord
        if x1 < x2 and y1 == y2:
            Xc = Xchord
            Yc = Ychord - slope
        if x1 > x2 and y1 == y2:
            Xc = Xchord
            Yc = Ychord + slope
    else:
        if x1 < x2 and y1 < y2:
            Xc = Xchord - Rise
            Yc = Ychord + Run
        if x1 < x2 and y1 > y2:
            Xc = Xchord + Rise
            Yc = Ychord + Run
        if x1 > x2 and y1 > y2:
            Xc = Xchord + Rise
            Yc = Ychord - Run
        if x1 > x2 and y1 < y2:
            Xc = Xchord - Rise
            Yc = Ychord - Run
        if x1 == x2 and y1 < y2:
            Xc = Xchord - slope
            Yc = Ychord
        if x1 == x2 and y1 > y2:
            Xc = Xchord + slope
            Yc = Ychord
        if x1 < x2 and y1 == y2:
            Xc = Xchord
            Yc = Ychord + slope
        if x1 > x2 and y1 == y2:
            Xc = Xchord
            Yc = Ychord - slope

    Xdiff = x1 - Xc
    Ydiff = y1 - Yc
    w = np.pi - np.arcsin(Ydiff / Rinput) if Xdiff >= 0 else np.arcsin(Ydiff / Rinput)

    if G02:
        arc = np.array([[Xc - Rinput * np.cos(w + (beta * n)),
                         Yc + Rinput * np.sin(w + (beta * n))] for n in range(0, resolution + 1)])
    else:
        arc = np.array([[Xc - Rinput * np.cos(w - (beta * n)),
                         Yc + Rinput * np.sin(w - (beta * n))] for n in range(0, resolution + 1)])

    return arc[:, 0], arc[:, 1]
