from math import sqrt
from typing import override


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        
    def __str__(self) -> str:
        return f"Point: x={self.x}, y={self.y}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def distanceTo(self, other) -> float:
        assert(isinstance(other, Point))
        x1 = self.x
        y1 = self.y
        x2 = other.x
        y2 = other.y
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    
    def __isInRectInternal(self, x, y, w, h, threshold: float=0.0) -> bool:
        return x - threshold <= self.x <= x + w + threshold and y - threshold <= self.y <= y + h + threshold
        
    
    def isInRect(self, other, threshold: float=0.0) -> bool:
        """return true if this point is in given rectangle. Note that this point should in the same scale with rect (unit or scaled).

        Args:
            other (RectBase): rectangle given
        """
        assert(isinstance(other, RectBase))
        
        if isinstance(other, RectUnit):
            x, y, w, h = other.getUnitXYWH()
            return self.__isInRectInternal(x, y, w, h, threshold)
        elif isinstance(other, RectScaled):
            x, y, w, h = other.getScaledXYWH()
            return self.__isInRectInternal(x, y, w, h, threshold)
        else:
            raise ValueError("no matching rects")
    
    
    @staticmethod
    def getMedianPoint(point1, point2):
        assert(isinstance(point1, Point))
        assert(isinstance(point2, Point))
        x1 = point1.x
        y1 = point1.y
        x2 = point2.x
        y2 = point2.y
        return Point((x1 + x2) / 2, (y1 + y2) / 2)
    
    @staticmethod
    def merge_points(point_list1, 
                     point_list2, 
                     label1: str, 
                     label2: str, 
                     threshold: float=0.1, 
                     label_method=lambda x, y: x + y
                     ) -> list[tuple]:
        """Merge two locations together. Helps combine and show the final result of multiple detection outputs.

        Args:
            point1 (Point): Unit (0~1) x, y list, the first one
            point2 (Point): Unit (0~1) x, y list, the second one
            label1 (str): lablel of first list, how to describe the first list?
            label2 (str): lablel of first list, how to describe the first list?
            threshold (float): Merge condition (unit length), when the distance of two locations is lower than this, they will be merged.
            label_method (function): how the label should be if the location is merged? Default is "label1" + "label2", e.g. for "red" and "green" labels, the result is "redgreen".

        Returns:
            list[tuple[Point, str]]: The final locations and their labels
        """
    
        assert(isinstance(point_list1, list))
        assert(isinstance(point_list2, list))

        output_points_with_labels = []
        
        # Keep a set of merged indices, when iterate again the whole list of locations, skip them.
        merged_indices_loc1 = set()
        merged_indices_loc2 = set()
        
        for index1, point1 in enumerate(point_list1):
            for index2, point2 in enumerate(point_list2):
                assert(isinstance(point1, Point))
                assert(isinstance(point2, Point))
                
                if point1.distanceTo(point2) <= threshold:
                    final_point = Point.getMedianPoint(point1, point2)
                    
                    # Only add merged locations at this point.
                    output_points_with_labels.append((final_point, label_method(label1, label2)))
                    
                    # Mark the index merged.
                    merged_indices_loc1.add(index1)
                    merged_indices_loc2.add(index2)
            
        # Iterate list1 again.
        for index1, point1 in enumerate(point_list1):
            if index1 in merged_indices_loc1:
                continue
            
            assert(isinstance(point1, Point))
            
            output_points_with_labels.append((point1, label1))
            
        # Iterate list2 again.
        for index2, point2 in enumerate(point_list2):
            if index2 in merged_indices_loc2:
                continue
            
            assert(isinstance(point1, Point))
            
            output_points_with_labels.append((point2, label2))
            
        return output_points_with_labels
        

class RectBase:
    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def __str__(self) -> str:
        return f"x={self.x}, y={self.y}, w={self.w}, h={self.h}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def getUnitXYWH(self):
        pass
    
    def getScaledXYWH(self, resx, resy):
        pass
    
    def getUnitCenter(self):
        pass
    
    def getScaledCenter(self, resx, resy):
        pass
    
    def getBoundingPoints(self):
        pass
    
    def isCoveredBy(self, other, threshold: float=0) -> bool:
        assert(isinstance(other, RectBase))
        
        self_p1, self_p2 = Point(self.x, self.y),            Point(self.x + self.w, self.y)
        self_p3, self_p4 = Point(self.x, self.y + self.h),   Point(self.x + self.w, self.y + self.h)
        
        return all([point.isInRect(other) for point in [self_p1, self_p2, self_p3, self_p4]])
    
class RectUnit(RectBase):
    def __init__(self, x, y, w, h) -> None:
        super().__init__(x, y, w, h)
        
    def __str__(self) -> str:
        return "RectUnit: " + super().__str__()
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @override
    def getUnitXYWH(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.w, self.h)
    
    @override
    def getScaledXYWH(self, resx, resy) -> tuple[float, float, float, float]:
        return (self.x * resx, self.y * resy, self.w * resx, self.h * resy)
    
    @override
    def getUnitCenter(self) -> Point:
        return Point(self.x + self.w / 2, self.y + self.h / 2)
    
    @override
    def getScaledCenter(self, resx, resy) -> Point:
        scaled_x, scaled_y, scaled_w, scaled_h = self.getScaledXYWH(resx, resy)
        return Point(scaled_x + scaled_w / 2, scaled_y + scaled_h / 2)
    
    @override
    def getBoundingPoints(self) -> list[Point]:
        return [Point(x, y) for x, y in [
            (self.x, self.y),
            (self.x + self.w, self.y),
            (self.x, self.y + self.h),
            (self.x + self.w, self.y + self.h)
        ]]

class RectScaled(RectBase):
    def __init__(self, x, y, w, h, resx, resy) -> None:
        unit_x, unit_y, unit_w, unit_h = x / resx, y / resy, w / resx, h / resy
        super().__init__(unit_x, unit_y, unit_w, unit_h)
        
        self.frameWidth = resx
        self.frameHeight = resy
        
    def __str__(self) -> str:
        return "RectScaled: " + super().__str__() + f", resx={self.frameWidth}, resy={self.frameHeight}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @override
    def getUnitXYWH(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.w, self.h)
    
    @override
    def getScaledXYWH(self, resx=0, resy=0) -> tuple[float, float, float, float]:
        return (self.x * self.frameWidth, self.y * self.frameHeight, self.w * self.frameWidth, self.h * self.frameHeight)
    
    @override
    def getUnitCenter(self) -> Point:
        return Point(self.x + self.w / 2, self.y + self.h / 2)
    
    @override
    def getScaledCenter(self, resx=0, resy=0) -> Point:
        scaled_x, scaled_y, scaled_w, scaled_h = self.getScaledXYWH()
        return Point(scaled_x + scaled_w / 2, scaled_y + scaled_h / 2)
    
    @override
    def getBoundingPoints(self) -> list[Point]:
        return [Point(x * self.frameWidth, y * self.frameHeight) for x, y in [
            (self.x, self.y),
            (self.x + self.w, self.y),
            (self.x, self.y + self.h),
            (self.x + self.w, self.y + self.h)
        ]]
