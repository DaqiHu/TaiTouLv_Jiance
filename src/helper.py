import cv2
import random
from rects import Point, RectBase, RectScaled, RectUnit

def get_image_size(image_path: str) -> tuple[float, float]:
    image = cv2.imread(image_path)
    height, width, channel = image.shape
    return (width, height)

def __draw_rectangle__internal(p1: Point, p2: Point, img, label=None, color=None, line_thickness=3):
    """Use cv2 to draw rectangle on given image.

    Args:
        p1 (Point): The top-left corner location
        p2 (Point): The bottom-right corner location
        img (_type_): cv2.image
        color (_type_, optional): Line color. Defaults to None.
        line_thickness (int, optional): Line thickness. Defaults to 3.
    """
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(p1.x), int(p1.y)), (int(p2.x), int(p2.y))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1) # font thickness must be more than 1
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
        

def draw_rectangle_scaled(rect: RectScaled, img, label=None, color=None, line_thickness=3):
    x, y, w, h = rect.getScaledXYWH()
    p1 = Point(x, y)
    p2 = Point(x + w, y + h)
    __draw_rectangle__internal(p1, p2, img, label, color, line_thickness)
    
def draw_rectangle_unit(rect: RectUnit, resx: float, resy: float, img, label=None, color=None, line_thickness=3):
    x, y, w, h = rect.getScaledXYWH(resx, resy)
    p1 = Point(x, y)
    p2 = Point(x + w, y + h)
    __draw_rectangle__internal(p1, p2, img, label, color, line_thickness)
