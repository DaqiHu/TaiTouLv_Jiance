from rects import *
from inference import *
from helper import *
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mplcolors
import pandas as pd
import config

def merge_rects(main_rects, branch_rects, label1: str, label2: str, threshold: float=0.0, label_method=lambda x, y: x + y):
    """This is a project-specific merge function that handle the head-up case and default person case.
    """
    
    assert(isinstance(main_rects, list))
    assert(isinstance(branch_rects, list))
    
    output_rects_with_labels = []
    
    merged_indices_rect1 = set()
    merged_indices_rect2 = set()
    
    for index1, rect1 in enumerate(main_rects):
        for index2, rect2 in enumerate(branch_rects):
            assert(isinstance(rect1, RectBase))
            assert(isinstance(rect2, RectBase))
            
            if rect2.isCoveredBy(rect1, threshold):
                
                # Unlike `merge_points`, we don't need to append the merged result now. 
                # That's because if a rect is a `person` in `main_rects` and covers `head-up` in `branch_rects`, 
                # we only need to keep the ones in `branch_rects`. i.e. a `head-up` is always a `person`.
                merged_indices_rect1.add(index1)

    # Iterate main_rects again.
    for index1, rect1 in enumerate(main_rects):
        assert(isinstance(rect1, RectBase))
        
        if index1 in merged_indices_rect1:
            continue
        
        output_rects_with_labels.append((rect1, label1))
        
    # Iterate branch_rects again.
    for index2, rect2 in enumerate(branch_rects):
        assert(isinstance(rect2, RectBase))
        
        # Just add all of them to output.
        output_rects_with_labels.append((rect2, label2))
        
    return output_rects_with_labels

def interp_cmap(green_cmap, blue_cmap, red_cmap, x):
    if x < 0.2:
        return green_cmap(x / 0.2)
    elif x < 0.8:
        return blue_cmap((x - 0.2) / (0.8 - 0.2))
    else:
        return red_cmap((x - 0.8) / (1 - 0.8))
        

def main_image():
    # 1. get head-up image and rects with opencv format, scaled
    head_up_rects: list[RectScaled] = inference_image_rects_cv2(f"{config.faces_folder}/classroom.jpg")
    
    # 2. get normal student image and rects with yolo txt format, unit
    student_rects: list[RectUnit] = inference_image_rects_yolo(r"E:\GitHub\head-up-rate-detect\runs\detect\predict6\labels\image0.txt")
    
    # 3. merge rects
    final_rects = merge_rects(student_rects, head_up_rects, "person", "headup")
    final_centers: list[tuple[float, float, float]] = [(rect.getUnitCenter().x, rect.getUnitCenter().y, 1 if label == "headup" else 0) for rect, label in final_rects]
    
    # Draw Rect
    img = cv2.imread(f"{config.faces_folder}/classroom.jpg")
    height, width, channel = img.shape
    for rect, label in final_rects:
        draw_rectangle_unit(rect, width, height, img, label=label)

    cv2.imwrite(f"output/test2.jpg", img)

    # 4. create DataFrame for display
    data = pd.DataFrame(final_centers, columns=["x", "y", "value"])
    print(data)
    
    # 6. initialize seaborn parameters
    
    # # Define custom colormap
    
    # # light to dark
    # red_colors = [mplcolors.to_rgb(hex_color) for hex_color in ["#fad6d9", "#e63946"]]
    # green_colors = [mplcolors.to_rgb(hex_color) for hex_color in ["#b5e3ce", "#1c4a35"]] # a better looking green color rather than default green (0, 1, 0)
    # blue_colors = [mplcolors.to_rgb(hex_color) for hex_color in ["#d8e6ee", "#457b9d"]] # a better looking blue color rather than default blue (0, 0, 1)
    # cmap = sns.blend_palette(green_colors, as_cmap=True)
    
    # # mcolors.to_rgb(cm)
    
    # # g = sns.jointplot(data=data, kind="scatter", x="res-x", y="res-y", xlim=(0, 3840), ylim=(2160, 0))
    # # g.plot_joint(sns.kdeplot, zorder=0, levels=6, cmap=cmap)
    
    
    # fig, ax = plt.subplots()
    
    # # 设置颜色映射
    # cmap = sns.diverging_palette(220, 20, n=7, as_cmap=True)

    # # 绘制等高线图
    # contour = sns.kdeplot(data=data, x='x', y='y', fill=True, cmap=cmap, levels=[0, 0.2, 0.8, 1.0])

    # # 添加颜色条
    # cbar = plt.colorbar(contour, ax=ax, label='value')

    # # 7. show plot
    # plt.show()

def main_video():
    pass

def main():
    
    main_image()
    main_video()
        

if __name__ == "__main__":
    main()
