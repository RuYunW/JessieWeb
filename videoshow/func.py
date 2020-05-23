from django.shortcuts import render
import cv2
import numpy as np


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


def video_process():

    cap = cv2.VideoCapture('../media/new.mp4')  # 定义视频

    # 获得码率及尺寸
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(size)

    # size = (400, 200)
    size = (540, 250)
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('../media/out.mp4', cv2.VideoWriter_fourcc(*"mp4v"), fps, size)

    success, frame = cap.read()

    xmlfile_face = '../videoshow/cv_model/haarcascade_frontalface_default.xml'
    xmlfile_eye = '../videoshow/cv_model/haarcascade_eye.xml'
    xmlfile_mouth = '../videoshow/cv_model/haarcascade_smile.xml'

    face_cascade = cv2.CascadeClassifier(xmlfile_face)
    eye_cascade = cv2.CascadeClassifier(xmlfile_eye)
    mouth_cascade = cv2.CascadeClassifier(xmlfile_mouth)

    window_size = 50
    while success:
        # print(666)


        # cv2.waitKey(1000 / int(fps))  # 延迟


        success, frame = cap.read()  # 获取下一帧
        # continue
        ori_frame = frame


        # 检测人脸
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.15, minNeighbors=8, minSize=(20, 20),
                                              maxSize=(200, 200))

        eye_xyz = []
        mouth_xyz = []
        if len(faces) > 0:  # 检测到人脸
            for face in faces:
                x, y, w, h = face
                face_pic = frame[y:y + h, x:x + w]  # 脸部区域
                upper_face = frame[y:int(y + h * 0.6), x:x + w]  # 脸上半部分
                lower_face = frame[int(y + h * 0.4):y + h, x:x + w]  # 脸下半部分

                eyes = eye_cascade.detectMultiScale(upper_face, scaleFactor=1.15, minNeighbors=8, minSize=(20, 20),
                                                    maxSize=(300, 300))
                for (ex, ey, ew, eh) in eyes:  # 框出每个眼睛
                    # img = cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (255, 255, 0), 2)  # 在帧上绘制
                    eye_xyz.append(eclosion(
                        cv2.resize(ori_frame[y + ey:y + ey + eh, x + ex:x + ex + ew], (window_size, window_size),
                                   interpolation=cv2.INTER_AREA), top=int(window_size / 4), bottom=int(window_size / 4),
                        left=int(window_size / 4), right=int(window_size / 4)))

                mouths = mouth_cascade.detectMultiScale(lower_face, scaleFactor=1.15, minNeighbors=3, minSize=(20, 20),
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

        # 模拟没有检测到嘴巴，只保留眼睛
        mouth_xyz = []

        if len(mouth_xyz) >= 1:  # 如果检测到嘴巴
            mouth_pic = mouth_xyz[0]
        else:
            mouth_pic = eye_pic

        eye_pic = cv2.resize(eye_pic, (window_size * 2, window_size), interpolation=cv2.INTER_AREA)
        mouth_pic = cv2.resize(mouth_pic, (window_size * 2, window_size), interpolation=cv2.INTER_AREA)
        t = np.concatenate((eye_pic, mouth_pic))

        for i in range(1):
            zdy_pic = np.concatenate(((np.concatenate((t, t), axis=1), (np.concatenate((t, t), axis=1)))))
            t = zdy_pic
        zdy_pic = np.concatenate((zdy_pic, zdy_pic), axis=1)
        zdy_pic = cv2.resize(zdy_pic, (540, 250), interpolation=cv2.INTER_AREA)
        # print(zdy_pic.shape)
        # write_zdy_pic = zdy_pic[0:400, 0:200]
        # print(write_zdy_pic.shape)
        out.write(zdy_pic)  # 写视频帧
        cv2.imshow("Oto Video", zdy_pic)  # 显示
# cap.release()
# out.release()


video_process()