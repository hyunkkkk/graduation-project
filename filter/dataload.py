import numpy as np


class data_load():
    def __init__(self, sample, bitdepth=None, w=None, h=None):
        self.sample = sample
        self.bitdepth = bitdepth
        self.w = w
        self.h = h

    def read(self):
        width, height = self.w, self.h
        y_channel, u_channel, v_channel = self.load_yuv420_data(self.sample, width, height, self.bitdepth)
        return y_channel, u_channel, v_channel

    def load_yuv420_data(self, sample, width, height, bitdepth):
        try:
            # Open the YUV420 file in binary mode
            with open(sample, 'rb') as file:
                if bitdepth == 10:
                    # Read the Y component (luma) first
                    w, h = width, height  # Set the dimensions of your YUV420 images
                    y_size = w * h
                    y_data = np.fromfile(file, dtype=np.int16, count=y_size)  # y_size 만큼 뽑고
                    # Read the U and V components (chroma)
                    uv_size = (w * h // 4)  # U and V are half the size of Y
                    uv_data = np.fromfile(file, dtype=np.int16, count=2 * uv_size)  # y_size 이후의 값들을 뽑음
                    y_data = y_data.reshape((h, w))
                    u_data = uv_data[:uv_size].reshape((h // 2, w // 2))
                    v_data = uv_data[uv_size:].reshape((h // 2, w // 2))
                    return y_data, u_data, v_data
                elif bitdepth == 8:
                    w, h = width, height  # Set the dimensions of your YUV420 images
                    y_size = w * h
                    y_data = np.fromfile(file, dtype=np.uint8, count=y_size)  # y_size 만큼 뽑고
                    uv_size = w * h // 4  # U and V are half the size of Y
                    uv_data = np.fromfile(file, dtype=np.uint8, count=2 * uv_size)  # y_size 이후의 값들을 뽑음
                    y_data = y_data.reshape((h, w))
                    u_data = uv_data[:uv_size].reshape((h // 2, w // 2))
                    v_data = uv_data[uv_size:].reshape((h // 2, w // 2))
                    return y_data, u_data, v_data
        except Exception as e:
            # Handle any exceptions that may occur while loading YUV420 data
            print(f"Error loading YUV420 data from {sample}: {str(e)}")
            return None, None, None
