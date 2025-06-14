# 导入必要的库
import cv2
import dlib
import numpy as np
# 初始化dlib的人脸检测器和特征点预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
# ---------------------------------------
# 获取人脸特征点函数
def get_landmarks(gray, rect):
    landmarks = predictor(gray, rect)
    landmarks_points = []
    for i in range(0, 68):
        x = landmarks.part(i).x
        y = landmarks.part(i).y
        landmarks_points.append((x, y))
    landmarks_points = np.array(landmarks_points, np.int32)
    return landmarks_points
# ---------------------------------------
# 瘦脸函数
def face_thinning(img, landmarks, strength=15):
    img_output = img.copy()
    left_points = [3, 4, 5, 6, 7]
    right_points = [13, 12, 11, 10, 9]
    # 左侧瘦脸
    for i in range(len(left_points)):
        start_point = landmarks[left_points[i]]
        end_point = landmarks[left_points[i]]
        end_point = (end_point[0] + strength, end_point[1])
        img_output = local_translation_warp(img_output, start_point, end_point, radius=20)
    # 右侧瘦脸
    for i in range(len(right_points)):
        start_point = landmarks[right_points[i]]
        end_point = landmarks[right_points[i]]
        end_point = (end_point[0] - strength, end_point[1])
        img_output = local_translation_warp(img_output, start_point, end_point, radius=20)
    return img_output
# ---------------------------------------
# 大眼函数
def eye_enlarge(img, landmarks, strength=1.2):
    img_output = img.copy()
    # 左眼区域点集
    left_eye_points = landmarks[36:42]
    # 右眼区域点集
    right_eye_points = landmarks[42:48]
    # 左眼放大
    img_output = local_scale_warp(img_output, left_eye_points, strength)
    # 右眼放大
    img_output = local_scale_warp(img_output, right_eye_points, strength)
    return img_output
# ---------------------------------------
# 局部平移变形函数（用于瘦脸）
def local_translation_warp(img, start_point, end_point, radius):
    img_output = img.copy()
    ddradius = float(radius * radius)
    height, width, channels = img.shape
    mask = np.zeros((height, width), dtype=np.float32)
    cv2.circle(mask, start_point, radius, (1,), -1, cv2.LINE_AA)
    dx = end_point[0] - start_point[0]
    dy = end_point[1] - start_point[1]
    for i in range(height):
        for j in range(width):
            if mask[i, j] > 0:
                tx = j - start_point[0]
                ty = i - start_point[1]
                dist = tx * tx + ty * ty
                if dist < ddradius:
                    weight = (ddradius - dist) / (ddradius - dist + 0.0001)
                    weight = weight * weight
                    offset_x = int(dx * weight)
                    offset_y = int(dy * weight)
                    new_x = j + offset_x
                    new_y = i + offset_y
                    if new_x >= width:
                        new_x = width - 1
                    if new_x < 0:
                        new_x = 0
                    if new_y >= height:
                        new_y = height - 1
                    if new_y < 0:
                        new_y = 0
                    img_output[i, j] = img[new_y, new_x]
    return img_output
# ---------------------------------------
# 局部缩放变形函数（用于大眼）
def local_scale_warp(img, points, strength):
    img_output = img.copy()
    x, y, w, h = cv2.boundingRect(points)
    center_x = x + w // 2
    center_y = y + h // 2
    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    cv2.fillConvexPoly(mask, points, 1)
    radius = max(w, h) // 2
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if mask[i, j]:
                dx = j - center_x
                dy = i - center_y
                distance = np.sqrt(dx * dx + dy * dy)
                if distance < radius:
                    r = distance / radius
                    beta = 1 - strength * (1 - r * r)
                    new_x = int(beta * dx + center_x)
                    new_y = int(beta * dy + center_y)
                    if new_x >= img.shape[1]:
                        new_x = img.shape[1] - 1
                    if new_x < 0:
                        new_x = 0
                    if new_y >= img.shape[0]:
                        new_y = img.shape[0] - 1
                    if new_y < 0:
                        new_y = 0
                    img_output[i, j] = img[new_y, new_x]
    return img_output
# ---------------------------------------
# 亮眼函数
def eye_brightening(img, landmarks, alpha=1.2, beta=0):
    img_output = img.copy()
    # 左眼区域
    left_eye = landmarks[36:42]
    # 右眼区域
    right_eye = landmarks[42:48]
    # 创建掩模
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.fillConvexPoly(mask, left_eye, 255)
    cv2.fillConvexPoly(mask, right_eye, 255)
    # 调整亮度和对比度
    img_eye = cv2.addWeighted(img_output, alpha, img_output, 0, beta)
    img_output[mask == 255] = img_eye[mask == 255]
    return img_output
# ---------------------------------------
# 磨皮函数
def skin_smooth(img):
    img_output = img.copy()
    # 转换到HSV颜色空间
    img_hsv = cv2.cvtColor(img_output, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(img_hsv)
    # 对明度通道进行双边滤波
    v_filtered = cv2.bilateralFilter(v, d=0, sigmaColor=75, sigmaSpace=15)
    # 合并通道
    img_filtered = cv2.merge([h, s, v_filtered])
    img_smooth = cv2.cvtColor(img_filtered, cv2.COLOR_HSV2BGR)
    return img_smooth
# ---------------------------------------
# 去除瑕疵函数
def remove_blemishes(img):
    img_output = img.copy()
    # 转换到Lab颜色空间
    img_lab = cv2.cvtColor(img_output, cv2.COLOR_BGR2Lab)
    l, a, b = cv2.split(img_lab)
    # 对亮度通道进行自适应直方图均衡化
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_clahe = clahe.apply(l)
    # 合并通道
    img_clahe = cv2.merge([l_clahe, a, b])
    img_result = cv2.cvtColor(img_clahe, cv2.COLOR_Lab2BGR)
    return img_result
# ---------------------------------------
# 主函数
def beautify_image(img_path):
    # 读取图像
    img = cv2.imread(img_path)
    if img is None:
        print("无法读取图像！")
        return None
    # 创建副本
    img_output = img.copy()
    # 转换为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 人脸检测
    faces = detector(gray)
    if len(faces) == 0:
        print("未检测到人脸！")
        return img
    for face in faces:
        # 获取特征点
        landmarks = get_landmarks(gray, face)
        # 瘦脸处理
        img_output = face_thinning(img_output, landmarks, strength=15)
        # 大眼处理
        img_output = eye_enlarge(img_output, landmarks, strength=1.2)
        # 亮眼处理
        img_output = eye_brightening(img_output, landmarks, alpha=1.5, beta=0)
    # 磨皮处理
    img_output = skin_smooth(img_output)
    # 去除瑕疵
    img_output = remove_blemishes(img_output)
    return img_output
# ---------------------------------------
# 测试函数
if __name__ == "__main__":
    input_image_path = "input.jpg"    # 输入图像路径
    output_image_path = "output.jpg"  # 输出图像路径
    result = beautify_image(input_image_path)
    if result is not None:
        # 显示结果
        cv2.imshow("Result", result)
        # 保存结果
        cv2.imwrite(output_image_path, result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
