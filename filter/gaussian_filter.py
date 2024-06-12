# import cv2
# import cv2 as cv
# import sys
# import numpy as np
# #img_as_float
# from skimage import io
# from matplotlib import pyplot as plt
#
# image=cv.imread('images/imgsample5.jpg')	# 영상 읽기
# #image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# if image is None:
#     sys.exit('파일을 찾을 수 없습니다.')
# bilateral_using_cv2 = cv2.bilateralFilter(image, 12, 150, 6, borderType=cv2.BORDER_CONSTANT)
# #kernel = np.ones((3,3), np.float32)/
# #gaussian_kernel = np.array([[1/16, 1/8, 1/16],[1/8, 1/4, 1/8],[1/16, 1/8, 1/16]])
# #conv_using_cv2 = cv2.filter2D(image, -1, gaussian_kernel, borderType=cv2.BORDER_CONSTANT)
# conv_using_cv2 = cv2.GaussianBlur(image, (13,13),3)
# #plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB)) # Convert BGR to RGB
# #plt.axis('off') # Don't show axes
# #plt.show()
#
# #cv2.imshow("Original", image)
# #cv2.imshow("cv2 bilateral", bilateral_using_cv2)
# #cv2.imshow("cv2 gaussian", conv_using_cv2)
# #cv2.imwrite('images//gaussianImage3_13133.png',conv_using_cv2)
# cv2.imwrite('images//bilateralImage-5-121506.png',bilateral_using_cv2)
# #cv2.waitKey(0)
# #cv2.destroyAllWindows()

import cv2

# YUV 파일을 읽어옵니다.
yuv_image = cv2.imread('images/D_BasketballPass_416x240_50.yuv', cv2.IMREAD_COLOR)

# # YUV 이미지를 YUV 채널로 분리합니다.
# Y_channel, U_channel, V_channel = cv2.split(yuv_image)
#
# # Bilateral filter 적용
# # 각 채널에 대해 필터를 적용합니다.
# Y_filtered = cv2.bilateralFilter(Y_channel, d = -1, sigmaColor = 100, sigmaSpace = 6)
# U_filtered = cv2.bilateralFilter(U_channel, d = -1, sigmaColor = 100, sigmaSpace = 6)
# V_filtered = cv2.bilateralFilter(V_channel, d = -1, sigmaColor = 100, sigmaSpace = 6)
#
# # 필터가 적용된 YUV 채널을 다시 결합합니다.
# filtered_image = cv2.merge([Y_filtered, U_filtered, V_filtered])

# 필터가 적용된 이미지를 저장합니다.
cv2.imwrite('filtered_yuv_image.yuv',yuv_image)