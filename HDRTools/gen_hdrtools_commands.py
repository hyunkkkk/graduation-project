"""
Generates HDRTools commands for aribitrary YUVs.

From NNVC CTC Document : 

An example command to calculate both the PSNR and MS-SSIM metrics is:

HDRMetrics -f HDRMetricsYUV.cfg \
    -p Input0File=<original.yuv> \
    -p Input1File=<evaluated.yuv> \
    -p EnableJVETPSNR=1 \
    -p EnableJVETMSSSIM=1 MaxSampleValue=1023 \
    -p EnablePSNR=1

Additional information about the dimensions and bit-depth
of the sequence may need to be provided. 
Please see the HDRMetricsYUV.cfg file for more information, 
which is included in the HDRTools software package.
"""
import os.path as osp


datas = [
    {
        "name": "Cactus", # 임의의 이름
        "orig": "Cactus2.yuv", # 원본 파일 이름
        "recon": "dec_Cactus2.yuv", # 디코딩 된 복원 파일 이름
        "bitdepth": 8,
        "frames": 1, # 총 프레임 수, 이미지의 경우 1
        "framerate": 1, # 초당 프레임 수, 이미지의 경우 1
        "width": 1920,
        "height": 1080,
    }
    # {
    #     "name": "Beach", # 임의의 이름
    #     "orig": "1.yuv", # 원본 파일 이름
    #     "recon": "1_recon.yuv", # 디코딩 된 복원 파일 이름
    #     "bitdepth": 8,
    #     "frames": 1, # 총 프레임 수, 이미지의 경우 1
    #     "framerate": 1, # 초당 프레임 수, 이미지의 경우 1
    #     "width": 1920,
    #     "height": 1080,
    # }
]


orig_root = "orig" # 원본 파일 경로
recon_root = "recon" # 디코딩 된 복원 파일 이름

result_root = "results"
shellscript = "run_hdrtools.bat"

HDRMETRICS = "HDRMetrics.exe"
CONFIG = "HDRMetricsYUV.cfg"

with open(shellscript, "w") as f:
    for data in datas:
        print(data["name"])
        rec_yuv_file = osp.join(
            recon_root,
            data["recon"]
        )
        orig_yuv_file = osp.join(
            orig_root, data["orig"]
        )
        log_file = osp.join(
            result_root,
            data["name"] + ".txt"
        )
        out_file = osp.join(
            result_root,
            data["name"] + ".out"
        )
        frames = data["frames"]
        framerate = data["framerate"]
        bitdepth = data["bitdepth"]
        dim = (data["width"], data["height"])
        command = HDRMETRICS
        command += f" -f {CONFIG}"
        command += " -p EnableJVETPSNR=1"
        command += " -p EnableJVETMSSSIM=1"
        command += " -p EnablePSNR=1"
        command += f" -p NumberOfFrames={frames}"
        command += f" -p MaxSampleValue={2 ** bitdepth -1}"
        command += f" -p Input0File={orig_yuv_file}"
        command += f" -p Input1File={rec_yuv_file}"
        command += f" -p LogFile={log_file}"
        command += f" -p Input0Rate={framerate}"
        command += f" -p Input0Width={dim[0]}"
        command += f" -p Input0Height={dim[1]}"
        command += f" -p Input1Rate={framerate}"
        command += f" -p Input1Width={dim[0]}"
        command += f" -p Input1Height={dim[1]}"              
        command += f" -p Input0BitDepthCmp0={bitdepth}"
        command += f" -p Input0BitDepthCmp1={bitdepth}"
        command += f" -p Input0BitDepthCmp2={bitdepth}"
        command += f" -p Input1BitDepthCmp0={bitdepth}"
        command += f" -p Input1BitDepthCmp1={bitdepth}"
        command += f" -p Input1BitDepthCmp2={bitdepth} > {out_file}\n"
        f.write(command)