import cv2
import dlib
import numpy as np
from scipy.spatial import Delaunay

# 初始化dlib的人脸检测器和特征点预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# 获取人脸特征点函数
def get_landmarks(img_gray, rect):
    landmarks = predictor(img_gray, rect)
    points = []
    for p in landmarks.parts():
        points.append([p.x, p.y])
    return np.array(points, np.int32)

# 瘦脸功能
def face_thinning(img, landmarks, k=0.15):
    """
    瘦脸函数
    img: 输入图像
    landmarks: 特征点
    k: 瘦脸强度系数
    """
    img_cp = img.copy()
    left_points = [3, 4, 5, 6, 7]
    right_points = [13, 12, 11, 10, 9]
    for i in range(len(left_points)):
        # 获取左侧和右侧点的位置
        p_left = landmarks[left_points[i]]
        p_right = landmarks[right_points[i]]
        # 瘦脸操作
        img_cp = local_translation_warp(img_cp, p_left, p_right, k)
    return img_cp

# 局部平移变换函数
def local_translation_warp(img, start_point, end_point, radius):
    ddradius = radius * radius
    img_cp = img.copy()
    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.float32)
    cv2.circle(mask, tuple(start_point), radius, 1, -1)
    dx = end_point[0] - start_point[0]
    dy = end_point[1] - start_point[1]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if mask[i, j] > 0:
                tx = j - start_point[0]
                ty = i - start_point[1]
                dist = tx * tx + ty * ty
                weight = (ddradius - dist) / (ddradius - dist + 0.0001)
                weight = weight * weight
                nx = int(j + weight * dx)
                ny = int(i + weight * dy)
                if nx >= img.shape[1]:
                    nx = img.shape[1] - 1
                if ny >= img.shape[0]:
                    ny = img.shape[0] - 1
                img_cp[i, j] = img[ny, nx]
    return img_cp

# 磨皮处理（基于双边滤波和细节层融合）
def skin_smooth(img):
    # 转换到HSV色彩空间
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v1 = cv2.split(img_hsv)

    # 对亮度通道进行处理
    v2 = cv2.bilateralFilter(v1, d=0, sigmaColor=75, sigmaSpace=15)
    v3 = cv2.subtract(v2, v1)
    v3 = cv2.addWeighted(v1, 1.0, v3, 0.5, 0)

    # 合并通道
    img_hsv = cv2.merge([h, s, v3])
    img_smooth = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
    return img_smooth

# 去除瑕疵功能
def remove_blemishes(img):
    """
    去除皮肤瑕疵
    """
    # 转换到YCbCr色彩空间
    img_ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(img_ycc)

    # 对皮肤区域进行阈值分割
    skin_mask = cv2.inRange(img_ycc, (0, 135, 85), (255, 180, 135))

    # 使用形态学操作去除噪声
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel, iterations=2)
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=1)

    # 找到瑕疵区域（暗斑和亮斑）
    blemish_mask = cv2.adaptiveThreshold(y, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                         cv2.THRESH_BINARY_INV, 11, 2)
    blemish_mask = cv2.bitwise_and(blemish_mask, skin_mask)

    # 使用修补算法去除瑕疵
    img_result = cv2.inpaint(img, blemish_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    return img_result

# 主函数
def beautify_image(img_path):
    img = cv2.imread(img_path)
    img_result = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 人脸检测
    faces = detector(gray)
    if len(faces) == 0:
        print("未检测到人脸！")
        return img

    for face in faces:
        # 特征点检测
        landmarks = get_landmarks(gray, face)

        # 瘦脸处理
        img_result = face_thinning(img_result, landmarks, k=15)

    # 磨皮处理
    img_result = skin_smooth(img_result)

    # 去除瑕疵
    img_result = remove_blemishes(img_result)

    return img_result

# 测试函数
if __name__ == "__main__":
    input_image = "input.jpg"  # 输入图像路径
    output_image = "output.jpg"  # 输出图像路径

    result = beautify_image(input_image)

    cv2.imshow("Result", result)
    cv2.imwrite(output_image, result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
