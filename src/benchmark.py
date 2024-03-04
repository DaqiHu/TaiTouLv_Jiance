import timeit
import cv2
import config

classifier = cv2.CascadeClassifier(config.classifier_data)

def inspect_benchmark(classifier):
    path = config.faces_folder
    pic_path = r"N105Monday_1_2.jpg"
    p = path + '/' + pic_path
    img = cv2.imread(p)
    color = (0, 255, 0)

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faceRects = classifier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
    # a = len(faceRects)
    # global face
    # face = a
    # str3 = str(a)
    # var.set(class_room_chosen.get() + str1 + course_time.get() + str2 + str3)


def benchmark():
    # Replace the following code with the function or code snippet you want to benchmark
    inspect_benchmark(classifier)


def main():
    """
    """

    

    loops = 1000

    # Measure the execution time

    execution_time = timeit.timeit(benchmark, number=loops)

    # Calculate the average time per loop
    average_time_per_loop = execution_time / loops

    print(f"Average time per loop: {average_time_per_loop:.10f} seconds")
    print(f"Total execution time for {loops} loops: {execution_time:.6f} seconds")


if __name__ == "__main__":
    main()
