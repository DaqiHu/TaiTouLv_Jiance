import config
from helper import *
import reference.get_heatmap as get_heatmap
from inference import *
from rects import *
# test of get_heatmap.get_video_xy

video_path = f"{config.faces_folder}/video_edited.mp4"
ret = get_heatmap.get_video_xy(video_path)
print(ret)

# test of get_heatmap.scaled_locations_to_unit

int_list = [
    (1000, 2000),
    (2000, 1000)
]
ret = get_heatmap.scaled_locations_to_unit(int_list, 3840, 2160)
print(ret)

# test of get_heatmap.is_locations_unit

scaled_list = [
    (1000, 2000),
    (2000, 1000)
]

unit_list = [
    (0.1, 0.2),
    (0.3, 0.4)
]
ret1 = get_heatmap.is_locations_unit(scaled_list)
ret2 = get_heatmap.is_locations_unit(unit_list)
print(ret1, ret2)

# test of get_heatmap.get_distance
ret = get_heatmap.get_distance((0.1, 0.2), (0.2, 0.1))
print(ret)

# test of merge_locations
locls1 = [
    (0.1, 0.1),
    (0.9, 0.9)
]

locls2 = [
    (0.11, 0.11),
    (1, 1)
]
ret = get_heatmap.merge_locations(locls1, locls2, "red", "green", threshold=0.1, label_method=lambda x, y: "both")
print(ret)
print("\n\n\n\n\n")
# image_path = r""
# ret = get_heatmap.inspect_image(f"{config.yolo_detect_folder}/{image_path}")

ret = inference_image_rects_cv2(f"{config.faces_folder}/classroom.jpg")
test = ret[0]

print(len(ret))

print(test)

print(test.getScaledCenter())
print(test.getScaledXYWH())
print(test.getUnitCenter())
print(test.getUnitXYWH())

# ret = inference_image_rects_yolo(f"{config.yolo_detect_folder}/exp4/labels/snipshot.txt")

# resx, resy = get_image_size(f"{config.yolo_detect_folder}/exp4/snipshot.jpg")
# test = ret[0]

# print(test)

# print(test.getScaledCenter(resx, resy))
# print(test.getScaledXYWH(resx, resy))
# print(test.getUnitCenter())
# print(test.getUnitXYWH())

head_up_rects: list[RectScaled] = inference_image_rects_cv2(f"{config.faces_folder}/classroom.jpg")
img = cv2.imread(f"{config.faces_folder}/classroom.jpg")
for rect in head_up_rects:
    draw_rectangle_scaled(rect, img)

cv2.imwrite(f"output/test2.jpg", img)