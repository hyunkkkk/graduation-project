from dataload import data_load
import sys
import argparse 
import cv2
import os
import numpy as np

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Example training script.")
    parser.add_argument("--btd", type=int, default=8, help="bit depth")
    parser.add_argument("--w", type=int, default=1920, help="width")
    parser.add_argument("--h", type=int, default=1080, help="height")
    parser.add_argument("--data", type=str, default='project/code/image_yuv/BasketballDrive.yuv', help="dataset path")
    parser.add_argument("--output", type=str, default='project/code/image_yuv',help="output directory")
    parser.add_argument("--name", type=str, default='Cactus2',help="output yuv name")
    args = parser.parse_args(argv)
    return args

def main(argv):
    args = parse_args(argv)

    ### YUV Image File 읽기 y, u, v 각각을 읽음.
    sample = data_load(args.data, args.btd, args.w, args.h)
    y_channel, u_channel, v_channel = sample.read()

    ### bilateralfilter 적용
    y_channel_bilateral = cv2.bilateralFilter(y_channel, -1, 10, 8)
    u_channel_bilateral = cv2.bilateralFilter(u_channel, -1, 10, 8)
    v_channel_bilateral = cv2.bilateralFilter(v_channel, -1, 10, 8)

    ### canny edge 적용
    y_channel_mask = cv2.Canny(y_channel,198, 200)

    kernel = np.ones((10,10), np.uint8)
    y_channel_mask = cv2.dilate(y_channel_mask, kernel, iterations =1)

    ### edge 는 1, 그외는 0 mask 생성
    y_channel_mask_positive = np.where(y_channel_mask == 255, 1, y_channel_mask)
    ### edge 는 0, 그외는 1 mask 생성
    y_channel_mask_negative = np.where(y_channel_mask == 255, 0, np.where(y_channel_mask == 0, 1, y_channel_mask))

    ### alpha array 생성 
    ### -- 만약 alpha 를 0.5 외 다양한 값을 쓰려면 두 개의 numpy 배열을 생성해서 따로 곱해주면 될 것 같아요. 
    alpha = np.full(y_channel.shape, 0.5)

    print(y_channel.shape)

    ### 원본과 edge 를 곱하여, 원본에서 edge 정보만을 추출    
    y_channel_masked = np.multiply(y_channel, y_channel_mask_positive)

    ### bilatered 이미지와 edge 를 곱하여, bilatered 이미지의 edge 정보만을 추출    
    y_channel_bilateral_masked = np.multiply(y_channel_bilateral, y_channel_mask_positive)

    ### 원본 edge 정보와 bilatered 이미지 edge 정보를 alpha 로 가중합
    y_channel_summation_masked = np.uint8(np.multiply(alpha, y_channel_bilateral_masked) + np.multiply(alpha,y_channel_masked))

    ### 원본에 edge 있는 곳은 0 으로 처리
    y_channel_negative = np.multiply(y_channel, y_channel_mask_negative)

    ### 원본에 edge 가 0 으로 처리되었으므로, 새롭게 만든 edge 정보와 더하면 final output
    ### -- 참고! 이 때, dtype 이 다르면 결과가 이상하게 나옴. 따라서 위에서 np.uint8 로 처리하였음.
    y_channel_final = y_channel_negative + y_channel_summation_masked
    
    ### Outpuf file directory 생성 후 값을 쓰기
    os.makedirs(f"{args.output}", exist_ok=True)
    output_file = os.path.join(f"{args.output}", f"{args.name}.yuv")
    with open(output_file, "wb") as file:
        file.write(y_channel_final.tobytes())
        #file.write(y_channel_summation_masked.tobytes())
        file.write(u_channel_bilateral.tobytes())
        file.write(v_channel_bilateral.tobytes())

if __name__ == "__main__":
    main(sys.argv[1:]) 
