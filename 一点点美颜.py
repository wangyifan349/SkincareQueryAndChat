# 导入必要的库
import cv2
import dlib
import numpy as np

# 初始化dlib的人脸检测器和特征点预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# 获取人脸特征点函数
def get_landmarks(gray, rect):
    """
    从灰度图像中获取指定人脸区域的68个特征点。

    参数：
        gray: 灰度图像
        rect: dlib检测到的人脸矩形区域

    返回：
        landmarks_points: 包含68个特征点的numpy数组
    """
    # 获取人脸特征点
    landmarks = predictor(gray, rect)
    # 将特征点存储为列表
    landmarks_points = []
    for i in range(0, 68):
        x = landmarks.part(i).x
        y = landmarks.part(i).y
        landmarks_points.append((x, y))
    # 转换为numpy数组
    landmarks_points = np.array(landmarks_points, np.int32)
    return landmarks_points

# 瘦脸函数
def face_thinning(img, landmarks, strength=15):
    """
    对人脸进行瘦脸处理。

    参数：
        img: 原始图像
        landmarks: 人脸特征点
        strength: 瘦脸强度

    返回：
        img_output: 瘦脸处理后的图像
    """
    # 创建图像副本
    img_output = img.copy()
    # 定义左侧脸部需要移动的特征点索引
    left_points = [3, 4, 5, 6, 7]
    # 定义右侧脸部需要移动的特征点索引
    right_points = [13, 12, 11, 10, 9]
    # 左侧瘦脸处理
    for i in range(len(left_points)):
        start_point = landmarks[left_points[i]]
        # 计算新的终点，向内移动
        end_point = (start_point[0] + strength, start_point[1])
        # 调用局部平移变形函数
        img_output = local_translation_warp(img_output, start_point, end_point, radius=20)
    # 右侧瘦脸处理
    for i in range(len(right_points)):
        start_point = landmarks[right_points[i]]
        # 计算新的终点，向内移动
        end_point = (start_point[0] - strength, start_point[1])
        # 调用局部平移变形函数
        img_output = local_translation_warp(img_output, start_point, end_point, radius=20)
    return img_output

# 大眼函数
def eye_enlarge(img, landmarks, strength=1.2):
    """
    对人脸进行大眼处理。

    参数：
        img: 原始图像
        landmarks: 人脸特征点
        strength: 大眼强度

    返回：
        img_output: 大眼处理后的图像
    """
    # 创建图像副本
    img_output = img.copy()
    # 获取左眼和右眼区域的特征点
    left_eye_points = landmarks[36:42]
    right_eye_points = landmarks[42:48]
    # 左眼放大
    img_output = local_scale_warp(img_output, left_eye_points, strength)
    # 右眼放大
    img_output = local_scale_warp(img_output, right_eye_points, strength)
    return img_output

# 局部平移变形函数（用于瘦脸）
def local_translation_warp(img, start_point, end_point, radius):
    """
    对图像的局部区域进行平移变形，用于瘦脸处理。

    参数：
        img: 原始图像
        start_point: 变形起始点（需要移动的特征点）
        end_point: 变形终止点（移动后的目标位置）
        radius: 影响半径（控制变形区域的大小）

    返回：
        img_output: 变形处理后的图像
    """
    # 创建图像副本
    img_output = img.copy()
    # 获取图像的高度和宽度
    height, width = img.shape[:2]
    # 创建坐标网格
    X, Y = np.meshgrid(np.arange(width), np.arange(height))
    # 转换为浮点型
    X = X.astype(np.float32)
    Y = Y.astype(np.float32)
    # 计算每个像素到起始点的平方距离
    distances = (X - start_point[0]) ** 2 + (Y - start_point[1]) ** 2
    # 计算平方半径
    radius_square = radius ** 2
    # 创建范围内的掩模
    mask = distances < radius_square
    # 计算权重因子
    weight = (radius_square - distances) / (radius_square - distances + 0.0001)
    weight = weight ** 2
    # 将超出范围的权重置为0
    weight[~mask] = 0
    # 计算位移量
    dx = (end_point[0] - start_point[0]) * weight
    dy = (end_point[1] - start_point[1]) * weight
    # 计算新的映射坐标
    map_x = X + dx
    map_y = Y + dy
    # 限制坐标范围防止越界
    map_x = np.clip(map_x, 0, width - 1)
    map_y = np.clip(map_y, 0, height - 1)
    # 进行图像重映射
    img_output = cv2.remap(img_output, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    return img_output

# 局部缩放变形函数（用于大眼）
def local_scale_warp(img, points, strength):
    """
    对图像的局部区域进行缩放变形，用于大眼处理。

    参数：
        img: 原始图像
        points: 需要变形的区域特征点
        strength: 缩放强度

    返回：
        img_output: 变形处理后的图像
    """
    # 创建图像副本
    img_output = img.copy()
    # 计算包含特征点的矩形区域
    x, y, w, h = cv2.boundingRect(points)
    # 计算中心点和半径
    center_x = x + w // 2
    center_y = y + h // 2
    radius = max(w, h) // 2
    # 获取图像的高度和宽度
    height, width = img.shape[:2]
    # 创建坐标网格
    X, Y = np.meshgrid(np.arange(width), np.arange(height))
    # 转换为浮点型
    X = X.astype(np.float32)
    Y = Y.astype(np.float32)
    # 计算每个像素到中心点的距离
    distances = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)
    # 创建范围内的掩模
    mask = distances < radius
    # 计算缩放因子
    r = distances / radius
    r = np.clip(r, 0, 1)
    beta = 1 - strength * (1 - r ** 2)
    # 防止beta值过小导致变形过度
    beta = np.clip(beta, 0.1, 1)
    # 将超出范围的beta置为1
    beta[~mask] = 1
    # 计算新的映射坐标
    map_x = beta * (X - center_x) + center_x
    map_y = beta * (Y - center_y) + center_y
    # 限制坐标范围防止越界
    map_x = np.clip(map_x, 0, width - 1)
    map_y = np.clip(map_y, 0, height - 1)
    # 进行图像重映射
    img_output = cv2.remap(img_output, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    return img_output

# 亮眼函数
def eye_brightening(img, landmarks, alpha=1.2, beta=0):
    """
    对人眼区域进行亮度增强。

    参数：
        img: 原始图像
        landmarks: 人脸特征点
        alpha: 对比度系数
        beta: 亮度增量

    返回：
        img_output: 亮眼处理后的图像
    """
    # 创建图像副本
    img_output = img.copy()
    # 获取左眼和右眼区域的特征点
    left_eye = landmarks[36:42]
    right_eye = landmarks[42:48]
    # 创建掩模
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    # 填充左眼区域
    cv2.fillConvexPoly(mask, left_eye, 255)
    # 填充右眼区域
    cv2.fillConvexPoly(mask, right_eye, 255)
    # 对眼睛区域进行亮度和对比度调整
    img_eye = cv2.addWeighted(img_output, alpha, img_output, 0, beta)
    # 将调整后的区域合并到原图
    img_output[mask == 255] = img_eye[mask == 255]
    return img_output

# 磨皮函数
def skin_smooth(img):
    """
    对图像进行磨皮处理。

    参数：
        img: 原始图像

    返回：
        img_smooth: 磨皮处理后的图像
    """
    # 创建图像副本
    img_output = img.copy()
    # 转换到YCrCb颜色空间
    img_ycrcb = cv2.cvtColor(img_output, cv2.COLOR_BGR2YCrCb)
    # 拆分通道
    y_channel, cr_channel, cb_channel = cv2.split(img_ycrcb)
    # 对亮度通道进行双边滤波
    y_filtered = cv2.bilateralFilter(y_channel, d=0, sigmaColor=75, sigmaSpace=15)
    # 合并通道
    img_filtered = cv2.merge([y_filtered, cr_channel, cb_channel])
    # 转换回BGR颜色空间
    img_smooth = cv2.cvtColor(img_filtered, cv2.COLOR_YCrCb2BGR)
    return img_smooth

# 去除瑕疵函数
def remove_blemishes(img):
    """
    对图像进行去除瑕疵处理。

    参数：
        img: 原始图像

    返回：
        img_result: 去除瑕疵后的图像
    """
    # 创建图像副本
    img_output = img.copy()
    # 转换到Lab颜色空间
    img_lab = cv2.cvtColor(img_output, cv2.COLOR_BGR2Lab)
    # 拆分通道
    l_channel, a_channel, b_channel = cv2.split(img_lab)
    # 创建CLAHE对象（自适应直方图均衡化）
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # 对L通道进行均衡化
    l_clahe = clahe.apply(l_channel)
    # 合并通道
    img_clahe = cv2.merge([l_clahe, a_channel, b_channel])
    # 转换回BGR颜色空间
    img_result = cv2.cvtColor(img_clahe, cv2.COLOR_Lab2BGR)
    return img_result

# 主函数
def beautify_image(img_path):
    """
    对输入的图像进行美颜处理。

    参数：
        img_path: 输入图像的路径

    返回：
        img_output: 美颜处理后的图像
    """
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
    # 对每张检测到的人脸进行处理
    for face in faces:
        # 获取特征点
        landmarks = get_landmarks(gray, face)
        # 瘦脸处理
        img_output = face_thinning(img_output, landmarks, strength=15)
        # 大眼处理
        img_output = eye_enlarge(img_output, landmarks, strength=1.2)
        # 亮眼处理
        img_output = eye_brightening(img_output, landmarks, alpha=1.5, beta=0)
    # 去除瑕疵
    img_output = remove_blemishes(img_output)
    # 磨皮处理
    img_output = skin_smooth(img_output)
    return img_output

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
