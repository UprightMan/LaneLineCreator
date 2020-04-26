import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

vid = cv2.VideoCapture(
    'D:\\CarND-LaneLines-P1\\test_videos\\solidYellowLeft.mp4')
current_frame = 0
img_array = []
while(True):
    ret, frame = vid.read()
    if ret:
        image = frame
        height, width, layers = image.shape
        size = (width, height)
        current_frame += 1
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        kernel_size = 5
        blur_gray = cv2.GaussianBlur(
            grayscale_image, (kernel_size, kernel_size), 0)

        low_threshold = 50
        high_threshold = 150
        image_edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

        mask = np.zeros_like(image_edges)
        ignore_mask_color = 255

        imshape = image.shape
        vertices = np.array([[(0, height), (450, 320), (500, 320),
                              (width, height)]], dtype=np.int32)
        cv2.fillPoly(mask, vertices, ignore_mask_color)
        masked_edges = cv2.bitwise_and(image_edges, mask)

        rho = 1
        theta = np.pi/180
        threshold = 10
        min_line_length = 10
        max_line_gap = 1
        image_lines = np.copy(image)*0

        lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold,
                                np.array([]), min_line_length, max_line_gap)
        # find slopes
        slope_threshold = 0.5
        slopes = []
        new_lines = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # calculate slope
            if x2 - x1 == 0.:  # avoiding division by 0
                slope = 0
            else:
                slope = (y2 - y1) / (x2 - x1)
            if abs(slope) > slope_threshold:
                slopes.append(slope)
                new_lines.append(line)
        # split lines into left and right lane
        right_lines = []
        left_lines = []
        for i, line in enumerate(new_lines):
            x1, y1, x2, y2 = line[0]
            x_center = width / 2
            if slopes[i] > 0 and x1 > x_center and x2 > x_center:
                right_lines.append(line)
            elif slopes[i] < 0 and x1 < x_center and x2 < x_center:
                left_lines.append(line)

        right_lines_x = []
        right_lines_y = []

        for line in right_lines:
            x1, y1, x2, y2 = line[0]

            right_lines_x.append(x1)
            right_lines_x.append(x2)

            right_lines_y.append(y1)
            right_lines_y.append(y2)
        # sometimes the right_lines_x is empty so this is necessary
        if len(right_lines_x) > 0:
            right_mid, right_b = np.polyfit(right_lines_x, right_lines_y, 1)

        left_lines_x = []
        left_lines_y = []
        for line in left_lines:
            x1, y1, x2, y2 = line[0]

            left_lines_x.append(x1)
            left_lines_x.append(x2)

            left_lines_y.append(y1)
            left_lines_y.append(y2)
        if len(left_lines_x) > 0:
            left_mid, left_b = np.polyfit(left_lines_x, left_lines_y, 1)
        # get endpoints for the final lines
        y1 = height
        y2 = height * 0.65

        right_x1 = (y1 - right_b) / right_mid
        right_x2 = (y2 - right_b) / right_mid

        left_x1 = (y1 - left_b) / left_mid
        left_x2 = (y2 - left_b) / left_mid

        # cast to int
        y1 = int(y1)
        y2 = int(y2)
        right_x1 = int(right_x1)
        right_x2 = int(right_x2)
        left_x1 = int(left_x1)
        left_x2 = int(left_x2)

        # draw lines
        cv2.line(image_lines, (right_x1, y1), (right_x2, y2), (0, 0, 255), 10)
        cv2.line(image_lines, (left_x1, y1), (left_x2, y2), (0, 0, 255), 10)

        combo = cv2.addWeighted(image, 1, image_lines, 1, 0)

        img_array.append(combo)
    else:
        break
vid.release()
vid_out = cv2.VideoWriter(
    'D:\\CarND-LaneLines-P1\\Output\\output.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
for i in range(len(img_array)):
    vid_out.write(img_array[i])
vid_out.release()
