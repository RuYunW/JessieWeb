from django.shortcuts import render
import cv2
import numpy as np
from videoshow.func import video_process


def index(request):
    if request.method == "POST" and request.POST.getlist('file_button'):
        lines = []
        error_list = []
        myFile = request.FILES.get("myfile", None)
        error_message = ""
        if not myFile:
            error_message = "no files for upload!"
            return render(
                request,
                "index.html",
                {"upload": False, "error_message": error_message})

        if '.mp4' in myFile.name:  # 如果是视频文件
            # 保存用户上传视频
            destination = open('media/new.mp4', 'wb+')

            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()

            # 对视频进行处理与合成
            try:
                video_process('media/', 'videoshow/')
                error_message = "视频处理完成"
                return render(request,
                              "index.html",
                              {"upload": False, "error_message": error_message})
            except:
                error_message = "视频处理完成"
                return render(request,
                              "index.html",
                              {"upload": False, "error_message": error_message})

        else:  # 不是视频文件
            error_message = "请上传 .mp4 视频文件"
            return render(request,
                          "index.html",
                          {"upload": False, "error_message": error_message})
    return render(request, "index.html")


def indax(request):
    error_message = "视频处理完成"
    return render(request,
                  "indax.html",
                  {"upload": False, "error_message": error_message})
