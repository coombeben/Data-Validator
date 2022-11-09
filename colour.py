from __future__ import annotations

from math import acos, degrees, sqrt


class ColourRGB:
    def __init__(self, r: int, g: int, b: int):
        if not all(0 <= x <= 255 for x in [r, g, b]):
            raise ValueError

        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return f'RGB({self.r}, {self.g}, {self.b})'

    def hex(self) -> str:
        return f'#{self.r:02x}{self.g:02x}{self.b:02x}'

    def tuple(self) -> (int, int, int):
        return self.r, self.g, self.b
        
    def to_hsl(self) -> ColourHSL:
        M = max(self.r, self.g, self.b)
        m = min(self.r, self.g, self.b)
        d = (M - m) / 255

        l = (M + m) / 510
        if l == 0:
            s = 0
        else:
            s = d / (1 - abs(2 * l - 1))

        H = int(degrees(acos((self.r - 0.5 * self.g - 0.5 * self.b) /
                             sqrt(self.r * self.r + self.g * self.g + self.b * self.b -
                                  self.r * self.g - self.g * self.b - self.b * self.r))))
        if self.g >= self.b:
            h = H
        else:
            h = 360 - H

        return ColourHSL(h, s, l)


class ColourHSL:
    def __init__(self, h: int, s: float, l: float):
        if not all([0 <= h <= 255, 0 <= s <= 1, 0 <= l <= 1]):
            raise ValueError

        self.h = h
        self.s = s
        self.l = l

    def __repr__(self):
        return f'HSL({self.h}, {self.s:.4f}, {self.l:.4f})'

    def tuple(self) -> (int, float, float):
        return self.h, self.s, self.l
        
    def to_rgb(self) -> ColourRGB:
        d = self.s * (1 - abs(2 * self.l - 1))
        m = 255 * (self.l - 0.5 * d)
        x = d * (1 - abs((self.h / 60) % 2 - 1))

        if 0 <= self.h < 60:
            r, g, b = (255 * d + m, 255 * x + m, m)
        elif 60 <= self.h < 120:
            r, g, b = (255 * x + m, 255 * d + m, m)
        elif 120 <= self.h < 180:
            r, g, b = (m, 255 * d + m, 255 * x + m)
        elif 180 <= self.h < 240:
            r, g, b = (m, 255 * x + m, 255 * x + m)
        elif 240 <= self.h < 300:
            r, g, b = (255 * x + m, m, 255 * d + m)
        else:
            r, g, b = (255 * d + m, m, 255 * x + m)

        return ColourRGB(int(r), int(g), int(b))

    
def gradient(prop: float, left_rgb: ColourRGB, right_rgb: ColourRGB) -> ColourRGB:
    """Returns the proportional colour between left and right"""
    prop = max(min(prop, 1), 0)

    left_hsl = left_rgb.to_hsl()
    right_hsl = right_rgb.to_hsl()

    mid_hsl = ColourHSL(
        int((right_hsl.h - left_hsl.h) * prop + left_hsl.h),
        (right_hsl.s - left_hsl.s) * prop + left_hsl.s,
        (right_hsl.l - left_hsl.l) * prop + left_hsl.l
    )

    return mid_hsl.to_rgb()
