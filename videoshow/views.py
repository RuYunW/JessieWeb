from django.shortcuts import render
import cv2
import numpy as np


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
            video_process()


            error_message = "视频上传成功"
            return render(request,
                          "index.html",
                          {"upload": False, "error_message": error_message})

        else:  # 不是视频文件
            error_message = "请上传 .mp4 视频文件"
            return render(request,
                          "index.html",
                          {"upload": False, "error_message": error_message})
    return render(request, "index.html")


def eclosion(pic, top=25, bottom=25, left=25, right=25, delta=100):
    # print(pic.shape)  # (20, 40, 3)
    for i in range(top):  # row
        for j in range(pic.shape[1]):  # pixel
            v = int(delta-i*delta/top)
            r = pic[i][j][0]
            g = pic[i][j][1]
            b = pic[i][j][2]

            r = (r+v) if (r+v)<255 else 255
            g = (g+v) if (g+v)<255 else 255
            b = (b+v) if (b+v)<255 else 255

            pic[i][j][0] = r
            pic[i][j][1] = g
            pic[i][j][2] = b

    for i in range(bottom):  # row
        for j in range(pic.shape[1]):  # pixel
            v = int(delta-i*delta/bottom)
            r = pic[pic.shape[0]-1-i][j][0]
            g = pic[pic.shape[0]-1-i][j][1]
            b = pic[pic.shape[0]-1-i][j][2]

            r = (r+v) if (r+v)<255 else 255
            g = (g+v) if (g+v)<255 else 255
            b = (b+v) if (b+v)<255 else 255

            pic[pic.shape[0]-1-i][j][0] = r
            pic[pic.shape[0]-1-i][j][1] = g
            pic[pic.shape[0]-1-i][j][2] = b

    for i in range(pic.shape[0]):
        for j in range(left):  # cow
            v = int(delta-j*delta/left)
            r = pic[i][j][0]
            g = pic[i][j][1]
            b = pic[i][j][2]

            r = (r+v) if (r+v)<255 else 255
            g = (g+v) if (g+v)<255 else 255
            b = (b+v) if (b+v)<255 else 255

            pic[i][j][0] = r
            pic[i][j][1] = g
            pic[i][j][2] = b

    for i in range(pic.shape[0]):  # pixel_line
        for j in range(right):  # cow
            v = int(delta-j*delta/right)
            r = pic[i][pic.shape[1]-1-j][0]
            g = pic[i][pic.shape[1]-1-j][1]
            b = pic[i][pic.shape[1]-1-j][2]

            r = (r+v) if (r+v)<255 else 255
            g = (g+v) if (g+v)<255 else 255
            b = (b+v) if (b+v)<255 else 255

            pic[i][pic.shape[1]-1-j][0] = r
            pic[i][pic.shape[1]-1-j][1] = g
            pic[i][pic.shape[1]-1-j][2] = b

    return pic

    # print(pic)


def video_process():

    cap = cv2.VideoCapture('/media/new.mp4')  # 定义视频
    # 获得码率及尺寸
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('/media/out.mp4', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)

    success, frame = cap.read()

    xmlfile_face = r'D:\Code from VS\Graduation-Project-for-Jessie\haarcascade_frontalface_default.xml'
    xmlfile_eye = r'D:\Code from VS\Graduation-Project-for-Jessie\haarcascade_eye.xml'
    xmlfile_mouth = r'C:\Users\yunyu\Desktop\cascades\haarcascade_mcs_mouth.xml'

    face_cascade = cv2.CascadeClassifier(xmlfile_face)
    eye_cascade = cv2.CascadeClassifier(xmlfile_eye)
    mouth_cascade = cv2.CascadeClassifier(xmlfile_mouth)

    window_size = 50
    while success:

        # cv2.imshow("Oto Video", frame)  # 显示
        cv2.waitKey(1000 / int(fps))  # 延迟
        out.write(frame)  # 写视频帧
        print(666)
        success, frame = cap.read()  # 获取下一帧
        ori_frame = frame

        # 检测人脸
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.15, minNeighbors=8, minSize=(50, 50),
                                              maxSize=(200, 200))

        eye_xyz = []
        mouth_xyz = []
        if len(faces) > 0:  # 检测到人脸
            for face in faces:
                x, y, w, h = face
                face_pic = frame[y:y + h, x:x + w]  # 脸部区域
                upper_face = frame[y:int(y + h * 0.6), x:x + w]  # 脸上半部分
                lower_face = frame[int(y + h * 0.4):y + h, x:x + w]  # 脸下半部分

                eyes = eye_cascade.detectMultiScale(upper_face, scaleFactor=1.15, minNeighbors=8, minSize=(50, 50),
                                                    maxSize=(300, 300))
                for (ex, ey, ew, eh) in eyes:  # 框出每个眼睛
                    # img = cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (255, 255, 0), 2)  # 在帧上绘制
                    eye_xyz.append(eclosion(
                        cv2.resize(ori_frame[y + ey:y + ey + eh, x + ex:x + ex + ew], (window_size, window_size),
                                   interpolation=cv2.INTER_AREA), top=int(window_size / 4), bottom=int(window_size / 4),
                        left=int(window_size / 4), right=int(window_size / 4)))

                mouths = mouth_cascade.detectMultiScale(lower_face, scaleFactor=1.15, minNeighbors=3, minSize=(50, 50),
                                                        maxSize=(400, 400))
                for (mx, my, mw, mh) in mouths:  # 框出每个嘴巴
                    # img = cv2.rectangle(frame, (x+mx, int(y+h*0.4+my)), (x+mx+mw, int(y+h*0.4+my+mh)), (0, 0, 255), 2)
                    mouth_xyz.append(eclosion(
                        cv2.resize(ori_frame[int(y + h * 0.4 + my):int(y + h * 0.4 + my + mh), x + mx:x + mx + mw],
                                   (2 * window_size, window_size), interpolation=cv2.INTER_AREA),
                        top=int(window_size / 4), bottom=int(window_size / 4), left=int(window_size / 2),
                        right=int(window_size / 2)))

        else:  # 未检测到人脸
            eye_xyz.append(
                eclosion(ori_frame[0:window_size, 0:window_size], top=int(window_size / 4), bottom=int(window_size / 4),
                         left=int(window_size / 4), right=int(window_size / 4)))
            eye_xyz.append(eclosion(ori_frame[0:window_size, window_size:2 * window_size], top=int(window_size / 4),
                                    bottom=int(window_size / 4), left=int(window_size / 4), right=int(window_size / 4)))
            mouth_xyz.append(eclosion(ori_frame[window_size:2 * window_size, 0:window_size], top=int(window_size / 4),
                                      bottom=int(window_size / 4), left=int(window_size / 2),
                                      right=int(window_size / 2)))

        if len(eye_xyz) >= 2:
            eye_1 = eye_xyz[0]
            eye_pic = np.concatenate((eye_xyz[0], eye_xyz[1]), axis=1)
        elif len(eye_xyz) == 1:
            eye_pic = np.concatenate((eye_xyz[0], eye_xyz[0]), axis=1)
        else:
            placeholder_pic = cv2.resize(ori_frame[235:235 + 66, 255:255 + 66], (window_size, window_size),
                                         interpolation=cv2.INTER_AREA)
            eye_pic = np.concatenate((placeholder_pic, placeholder_pic), axis=1)

        if len(mouth_xyz) >= 1:
            mouth_pic = mouth_xyz[0]
        else:
            mouth_pic = eye_pic

        eye_pic = cv2.resize(eye_pic, (window_size * 2, window_size), interpolation=cv2.INTER_AREA)
        mouth_pic = cv2.resize(mouth_pic, (window_size * 2, window_size), interpolation=cv2.INTER_AREA)
        t = np.concatenate((eye_pic, mouth_pic))

        for i in range(2):
            zdy_pic = np.concatenate(((np.concatenate((t, t), axis=1), (np.concatenate((t, t), axis=1)))))
            t = zdy_pic
    cap.release()
    out.release()

    # while(True):
    #     ret, frame = cap.read()  # 读取每一帧
    #     ori_frame = frame  # 另存原始帧
    #
    #     face_cascade = cv2.CascadeClassifier(xmlfile_face)
    #     eye_cascade = cv2.CascadeClassifier(xmlfile_eye)
    #     mouth_cascade = cv2.CascadeClassifier(xmlfile_mouth)
    #
    #     # 检测人脸
    #     faces = face_cascade.detectMultiScale(frame, scaleFactor=1.15, minNeighbors=8, minSize=(50, 50), maxSize=(200, 200))
    #
    #     eye_xyz = []
    #     mouth_xyz = []
    #     if len(faces) > 0:  # 检测到人脸
    #         for face in faces:
    #             x, y, w, h = face
    #             face_pic = frame[y:y+h, x:x+w]  # 脸部区域
    #             upper_face = frame[y:int(y+h*0.6), x:x+w]  # 脸上半部分
    #             lower_face = frame[int(y+h*0.4):y+h, x:x+w]  # 脸下半部分
    #
    #             eyes = eye_cascade.detectMultiScale(upper_face, scaleFactor=1.15, minNeighbors=8, minSize=(50, 50), maxSize=(300, 300))
    #             for (ex, ey, ew, eh) in eyes:  # 框出每个眼睛
    #                 # img = cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (255, 255, 0), 2)  # 在帧上绘制
    #                 eye_xyz.append(eclosion(cv2.resize(ori_frame[y+ey:y+ey+eh, x+ex:x+ex+ew], (window_size, window_size), interpolation=cv2.INTER_AREA), top=int(window_size/4), bottom=int(window_size/4), left=int(window_size/4), right=int(window_size/4)))
    #
    #             mouths = mouth_cascade.detectMultiScale(lower_face, scaleFactor=1.15, minNeighbors=3, minSize=(50, 50), maxSize=(400, 400))
    #             for (mx, my, mw, mh) in mouths:  # 框出每个嘴巴
    #                 # img = cv2.rectangle(frame, (x+mx, int(y+h*0.4+my)), (x+mx+mw, int(y+h*0.4+my+mh)), (0, 0, 255), 2)
    #                 mouth_xyz.append(eclosion(cv2.resize(ori_frame[int(y+h*0.4+my):int(y+h*0.4+my+mh), x+mx:x+mx+mw], (2*window_size, window_size), interpolation=cv2.INTER_AREA), top=int(window_size/4), bottom=int(window_size/4), left=int(window_size/2), right=int(window_size/2)))
    #
    #     else:  # 未检测到人脸
    #         eye_xyz.append(eclosion(ori_frame[0:window_size, 0:window_size], top=int(window_size/4), bottom=int(window_size/4), left=int(window_size/4), right=int(window_size/4)))
    #         eye_xyz.append(eclosion(ori_frame[0:window_size, window_size:2*window_size], top=int(window_size/4), bottom=int(window_size/4), left=int(window_size/4), right=int(window_size/4)))
    #         mouth_xyz.append(eclosion(ori_frame[window_size:2*window_size, 0:window_size], top=int(window_size/4), bottom=int(window_size/4), left=int(window_size/2), right=int(window_size/2)))
    #
    #     if len(eye_xyz) >= 2:
    #         eye_1 = eye_xyz[0]
    #         eye_pic = np.concatenate((eye_xyz[0], eye_xyz[1]), axis=1)
    #     elif len(eye_xyz) == 1:
    #         eye_pic = np.concatenate((eye_xyz[0], eye_xyz[0]), axis=1)
    #     else:
    #         placeholder_pic = cv2.resize(ori_frame[235:235+66, 255:255+66], (window_size, window_size), interpolation=cv2.INTER_AREA)
    #         eye_pic = np.concatenate((placeholder_pic, placeholder_pic), axis=1)
    #
    #     if len(mouth_xyz) >= 1:
    #         mouth_pic = mouth_xyz[0]
    #     else:
    #         mouth_pic = eye_pic
    #
    #     eye_pic = cv2.resize(eye_pic, (window_size*2, window_size), interpolation=cv2.INTER_AREA)
    #     mouth_pic = cv2.resize(mouth_pic, (window_size*2, window_size), interpolation=cv2.INTER_AREA)
    #     t = np.concatenate((eye_pic, mouth_pic))
    #
    #     for i in range(2):
    #         zdy_pic = np.concatenate(((np.concatenate((t, t), axis = 1),(np.concatenate((t, t), axis = 1)))))
    #         t = zdy_pic
    #
    #     cv2.imshow('cam2', zdy_pic)
    #     cv2.imshow('camera', ori_frame)  # 显示每一帧
    #
    #     if cv2.waitKey(1) & 0xFF == ord(' '):
    #         break
    # cap.release()
    # cv2.destroyAllWindows()

