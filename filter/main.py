from dataload import data_load
import sys
import argparse
import cv2
import os

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

    ### bilateralfilter 적용 example
    y_channel_bilateral = cv2.bilateralFilter(y_channel, -1, 10, 8)
    u_channel_bilateral = cv2.bilateralFilter(u_channel, -1, 10, 8)
    v_channel_bilateral = cv2.bilateralFilter(v_channel, -1, 10, 8)

    ### Outpuf file directory 생성 후 값을 쓰기
    os.makedirs(f"{args.output}", exist_ok=True)
    output_file = os.path.join(f"{args.output}", f"{args.name}.yuv")
    with open(output_file, "wb") as file:
        file.write(y_channel_bilateral.tobytes())
        file.write(u_channel_bilateral.tobytes())
        file.write(v_channel_bilateral.tobytes())

if __name__ == "__main__":
    main(sys.argv[1:])
