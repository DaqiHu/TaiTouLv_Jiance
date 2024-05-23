import enum
from math import sqrt
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mplcolors
import pandas as pd
import cv2
from tqdm import tqdm
import config
from rects import *

class DataType(enum.Enum):
    OpencvRect = 0
    YoloTxt = 1
    
class ReturnType(enum.Enum):
    Keep = 0
    Unit = 1
    Scaled = 2
    
def is_rect_unit(rect) -> bool:
    return all([0 <= value <= 1 for value in rect])

def is_rects_unit(rects) -> bool:
    return all([is_rect_unit(rect) for rect in rects])

def get_image_rect(img):
    
    color = (0, 255, 0)

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    classfier = cv2.CascadeClassifier(config.classifier_data)
    faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
    
    # print(faceRects)
        
    return faceRects

def get_image_rect_yolo(txt_path: str) -> list:
    with open(txt_path, encoding="utf-8", mode="r") as f:
        file_lines = f.readlines()
        return_list = []
        
        for line in file_lines:
            
            # "0 0.231226 0.243774 0.0466695 0.119245": str -> [0.231226, 0.243774, 0.0466695, 0.119245]: list[float]
            result = line.split(" ")
            xywh = [float(num) for num in result[1:]]
            
            # add one 
            return_list.append(xywh)
            
        return return_list
    
def format_rect(rect, origin: ReturnType=ReturnType.Keep, to: ReturnType=ReturnType.Keep, resx=0.0, resy=0.0):
    if origin == ReturnType.Keep or to == ReturnType.Keep:
        return rect
    
    if origin == to:
        return rect
    
    if resx <= 0 or resy <= 0:
        raise ValueError(f"rect resolution should be valid value, current value: resx:{resx}, resy:{resy}")
    
    x, y, w, h = rect
    if origin == ReturnType.Unit and to == ReturnType.Scaled:
        return [x * resx, y * resy, w * resx, h * resy]
    elif origin == ReturnType.Scaled and to == ReturnType.Unit:
        return [x / resx, y / resy, w / resx, h / resy]
    else:
        raise ValueError("not valid path")
    
def format_rects(rects, origin: ReturnType=ReturnType.Keep, to: ReturnType=ReturnType.Keep, resx=0.0, resy=0.0):
    return [format_rect(rect, origin, to, resx, resy) for rect in rects]

def inspect_image(image_path: str, data_type: DataType=DataType.OpencvRect, ret_type: ReturnType=ReturnType.Keep, resx=0.0, resy=0.0) -> list:

    image = cv2.imread(image_path)
    
    raw_rects = []
    match data_type:
        case DataType.OpencvRect:
            raw_rects = list(get_image_rect(image))
        case DataType.YoloTxt:
            raw_rects = get_image_rect_yolo(image_path)
        case _:
            return []
    
    match ret_type:
        case ReturnType.Keep:
            return raw_rects
        case ReturnType.Unit:
            if is_rects_unit(raw_rects):
                return raw_rects
            else:
                return format_rects(raw_rects, origin=ReturnType.Scaled, to=ReturnType.Unit, resx=resx, resy=resy)
        case ReturnType.Scaled:
            if is_rects_unit(raw_rects):
                return format_rects(raw_rects, origin=ReturnType.Unit, to=ReturnType.Scaled, resx=resx, resy=resy)
            else:
                return raw_rects
            
def inspect_webcam():
    pass

def inspect_video(video_path, fps: float = 15.0, data_type: DataType=DataType.OpencvRect) -> list:
    
    return_result = []
    
    capture = cv2.VideoCapture(video_path)

    # Use local variable of tqdm in while-loop. Get total frame count from fixed-length video (not webcam).
    
    video_fps = capture.get(cv2.CAP_PROP_FPS)
    
    process_fps = fps if fps <= video_fps else video_fps
    
    # this should be a float number greater than 1.0. We won't use integer to indicate the skip frame because special frame rate (e.g. 29.97 FPS) will difficult to handle.
    frames_to_skip: float = video_fps / process_fps
    
    frames_to_process = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    
    # This is an approximate, minor objection to real state won't affect the meaning of tqdm progress bar.
    progress_bar = tqdm(total=int(frames_to_process / frames_to_skip))
    
    # Real counter for actual frames. We won't convert video to avoid re encoding.
    skip_counter = 0
    
    if capture.isOpened():
        while True:
            success, img = capture.read()
            
            # Exit while meet end of video
            if not success:
                break
            
            if skip_counter == 0:
            
                rect = get_image_rect(img)
                # print(list(rect))
                
                return_result += list(rect)
                progress_bar.update()
            
            skip_counter += 1
            
            if skip_counter >= frames_to_skip:
                skip_counter = 0
                
    else:
        print(f"Failed to open video {video_path}.")
    
    return return_result

# get xywh and true resolution x and y
def get_object_xywh_yolo(file_name: str) -> list[list[float]]:
    with open(file_name, encoding="utf-8", mode="r") as f:
        file_lines = f.readlines()
        return_list = []
        
        for line in file_lines:
            result = line.split(" ")
            return_list.append([float(num) for num in result[1:]])
            
        return return_list

def get_objects_xywh_yolo(directory: str) -> list[list[float]]:
    return_list = []
    
    for root, dirs, files in os.walk(directory):

        for file in files:
            return_list += get_object_xywh_yolo(f"{root}/{file}")
    
    return return_list

def get_object_center_yolo(xywh_list: list[list[float]]) -> list[tuple[float, float]]:
    return_list = []
    
    for xywh in xywh_list:
        x = xywh[0]
        y = xywh[1]
        w = xywh[2]
        h = xywh[3]
        
        center_x = x + w / 2
        center_y = y + h / 2
        
        return_list.append((center_x, center_y))
    
    return return_list

def get_object_center_scaled(xywh_list) -> list[tuple[int, int]]:
    return_list = []
    
    if xywh_list is None or len(xywh_list) == 0:
        return return_list
    
    for xywh in xywh_list:
        x = xywh[0]
        y = xywh[1]
        w = xywh[2]
        h = xywh[3]
        
        center_x = x + w / 2
        center_y = y + h / 2
        
        return_list.append((int(center_x), int(center_y)))
    
    return return_list

def scaled_locations_to_unit(locations: list[tuple[int, int]] | list[tuple[float, float]],
                             width: int | float,
                             height: int | float) -> list[tuple[float, float]]:
    output_locations_unit = []
    
    for location in locations:
        scaled_x, scaled_y = location
        
        unit_x = scaled_x / width
        unit_y = scaled_y / height
        
        output_locations_unit.append((unit_x, unit_y))
        
    return output_locations_unit

def is_locations_unit(locations: list[tuple[float, float]]) -> bool:
    for location in locations:
        x, y = location
        if x > 1 or y > 1:
            return False
    
    return True

def get_distance(location1: tuple[float, float], location2: tuple[float, float]) -> float:
        x1, y1 = location1
        x2, y2 = location2
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    
def get_median_location(location1: tuple[float, float], location2: tuple[float, float]) -> tuple[float, float]:
    x1, y1 = location1
    x2, y2 = location2
    return ((x1 + x2) / 2, (y1 + y2) / 2)

def merge_locations(unit_locations1: list[tuple[float, float]], 
                    unit_locations2: list[tuple[float, float]],
                    label1: str,
                    label2: str,
                    threshold: float=0.1,
                    label_method=lambda x, y: x + y) -> list[tuple[float, float, str]]:
    """Merge two locations together. Helps combine and show the final result of multiple detection outputs.

    Args:
        unit_locations1 (list[tuple[float, float]]): Unit (0~1) x, y list, the first one
        unit_locations2 (list[tuple[float, float]]): Unit (0~1) x, y list, the second one
        label1 (str): lablel of first list, how to describe the first list?
        label2 (str): lablel of first list, how to describe the first list?
        threshold (float): Merge condition (unit length), when the distance of two locations is lower than this, they will be merged.
        label_method (function): how the label should be if the location is merged? Default is "label1" + "label2", e.g. for "red" and "green" labels, the result is "redgreen".

    Returns:
        list[tuple[float, float, str]]: The final locations and their labels
    """
    output_locations_with_labels = []
    
    # Keep a set of merged indices, when iterate again the whole list of locations, skip them.
    merged_indices_loc1 = set()
    merged_indices_loc2 = set()
    
    for index1, location1 in enumerate(unit_locations1):
        for index2, location2 in enumerate(unit_locations2):
            if get_distance(location1, location2) <= threshold:
                final_x, final_y = get_median_location(location1, location2)
                
                # Only add merged locations at this point.
                output_locations_with_labels.append((final_x, final_y, label_method(label1, label2)))
                
                # Mark the index merged.
                merged_indices_loc1.add(index1)
                merged_indices_loc2.add(index2)
    
    # Iterate list1 again.
    for index1, location1 in enumerate(unit_locations1):
        if index1 in merged_indices_loc1:
            continue
        
        output_locations_with_labels.append((location1[0], location1[1], label1))
    
    # Iterate list2 again.
    for index2, location2 in enumerate(unit_locations2):
        if index2 in merged_indices_loc2:
            continue
        
        output_locations_with_labels.append((location2[0], location2[1], label2))
            
    return output_locations_with_labels

def get_video_xy(path: str) -> tuple[float, float]:
    capture = cv2.VideoCapture(path)
    return (capture.get(cv2.CAP_PROP_FRAME_WIDTH), capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

def main():
    video_folder = config.faces_folder
    video_name = 'video.mp4'
    video_path = f"{video_folder}/{video_name}"
    
    # ---------------------- head up ----------------------------
    cv2_rects = inspect_video(video_path, fps=5)
    video_width, video_height = get_video_xy(video_path)
    head_up_locations_scaled = get_object_center_scaled(cv2_rects)
    
    head_up_locations_unit = scaled_locations_to_unit(head_up_locations_scaled, video_width, video_height)
    print("head-up students: \n", head_up_locations_unit)
    
    # ---------------------- all students ----------------------------
    yolo_result_folder = config.yolo_detect_folder
    yolo_result_phase = 12
    
    # "\\wsl.localhost\Ubuntu\home\dantalion\GitHub\yolov7\runs\detect\exp12\labels\snapshot.txt"
    yolo_xywh = get_objects_xywh_yolo(f"{yolo_result_folder}/exp{yolo_result_phase}/labels/snapshot.txt")
    
    all_student_locations_unit = get_object_center_yolo(yolo_xywh)
    print("all student locations: \n", all_student_locations_unit)
    
    # merge locations
    final_locations_with_label = merge_locations(head_up_locations_unit, all_student_locations_unit, "head-up", "attend", threshold=0.1, label_method=lambda x, y: "both")
    print("Final Locations: \n", final_locations_with_label)
    final_locations = [(loc[0], loc[1]) for loc in final_locations_with_label]

    
    # Define custom colormap
    colors = [mplcolors.to_rgb(hex_color) for hex_color in ["#b5e3ce", "#1c4a35"]] # a better looking green color rather than default green (0, 1, 0)
    cmap = sns.blend_palette(colors, as_cmap=True)
    
    # mcolors.to_rgb(cm)
    
    g = sns.jointplot(data=head_up_locations_unit, kind="scatter", x="res-x", y="res-y", xlim=(0, 3840), ylim=(2160, 0))
    g.plot_joint(sns.kdeplot, zorder=0, levels=6, cmap=cmap)
    
    # Set aspect ratio to 16:9
    # plt.gca().set_aspect(16/9, adjustable='box')

    # Show the plot
    plt.show()
    
if __name__ == "__main__":
    main()
