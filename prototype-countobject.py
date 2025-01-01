import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"    #logicoolのWEBカメラの起動が遅い問題対応
import cv2
import torch
from ultralytics import YOLO
import subfunc

#----------------------------------------
# !!! Setup for the webcam to be used !!!
#----------------------------------------
# Device ID: Also assigned to virtual cameras and other devices, so please try in order from 0
# デバイスID: 仮想カメラなどにも割り振られるので、0から順番に試してください
WEBCUM_DEVICE_ID = 0        # 0, 1, ...
# Video size: 1920,1080 for FullHD, 1280,720 for HD, etc., depending on the webcam used.
# 映像幅: FullHDなら1920,1080、HDなら1280,720など利用するWebカメラに合わせてください
WEBCUM_WIDTH = 1920
WEBCUM_HEIGHT = 1080
# Frame rate: 60fps, 30fps, 24fps, etc., depending on the webcam used
# フレームレート: 60fps、30fps、24fpsなど利用するWebカメラに合わせてください
WEBCUM_FPS = 30

subfunc.dbgprint("prg start.")
#----------------------------------------
# model load
#----------------------------------------
# Below is a pre-trained model file
# To determine something independently, it is necessary to collect images, tag them, and replace them with a proprietary learning model
# 以下は事前学習済みのモデルファイル
# 独自に何かを判定するには画像を集めて、タグ付けし、独自学習モデルに置き換える必要あり
# https://github.com/ultralytics/yolov5
model = YOLO("yolov5s.pt")
# Corresponding object with pre-trained model
# 事前学習済みのモデルで対応するオブジェクト
"""
person (人)、bicycle (自転車)、car (車)、motorcycle (オートバイ)、airplane (飛行機)、bus (バス)、
train (電車)、truck (トラック)、boat (ボート)、traffic light (信号)、fire hydrant (消火栓)、
stop sign (一時停止標識)、parking meter (駐車料金計)、bench (ベンチ)、
bird (鳥)、cat (猫)、dog (犬)、horse (馬)、sheep (羊)、cow (牛)、elephant (ゾウ)、bear (クマ)、
zebra (シマウマ)、giraffe (キリン)、backpack (リュックサック)、umbrella (傘)、handbag (ハンドバッグ)、
tie (ネクタイ)、suitcase (スーツケース)、frisbee (フリスビー)、skis (スキー板)、snowboard (スノーボード)、
sports ball (スポーツボール)、kite (凧)、baseball bat (野球バット)、baseball glove (野球グローブ)、
skateboard (スケートボード)、surfboard (サーフボード)、tennis racket (テニスラケット)、bottle (ボトル)、
wine glass (ワイングラス)、cup (カップ)、fork (フォーク)、knife (ナイフ)、spoon (スプーン)、bowl (ボウル)、
banana (バナナ)、apple (りんご)、sandwich (サンドイッチ)、orange (オレンジ)、broccoli (ブロッコリー)、
carrot (ニンジン)、hot dog (ホットドッグ)、pizza (ピザ)、donut (ドーナツ)、cake (ケーキ)、chair (椅子)、
couch (ソファ)、potted plant (植木鉢)、bed (ベッド)、dining table (ダイニングテーブル)、toilet (トイレ)、
TV (テレビ)、laptop (ノートパソコン)、mouse (マウス)、remote (リモコン)、keyboard (キーボード)、
cell phone (携帯電話)、microwave (電子レンジ)、oven (オーブン)、toaster (トースター)、sink (流し台)、
refrigerator (冷蔵庫)、book (本)、clock (時計)、vase (花瓶)、scissors (ハサミ)、teddy bear (テディベア)、
hair drier (ヘアドライヤー)、toothbrush (歯ブラシ)
"""
target_classes = ["cup", "cell phone"]

def main():
    #----------------------------------------
    # variable
    #----------------------------------------
    isReverse = False # reverse video
    isDrawWebCam = True # Camera image on/off
    isVerbose = False # Camera image on/off

    # init
    cap = cv2.VideoCapture(WEBCUM_DEVICE_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WEBCUM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WEBCUM_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, WEBCUM_FPS)
    if not cap.isOpened():
        print("error : open web camera")
        return

    # main loop
    while True:
        ret, img = cap.read()
        if isReverse:
            img = cv2.flip(img, 1)

        # detect object
        model(img, verbose=isVerbose)
        results = model(img)
        detections = results[0]

        # filtering
        target_detections = [
            det for det in detections.boxes.data.cpu().numpy()
            if model.names[int(det[-1])] in target_classes
        ]

        if not isDrawWebCam:
            iw = (int)(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            ih = (int)(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cv2.rectangle(img, (0,0), (iw,ih), (20, 20, 20), cv2.FILLED)

        # draw detect object
        for det in target_detections:
            x1, y1, x2, y2, conf, cls = det
            cls_name = model.names[int(cls)]
            label = f"{cls_name} {conf:.2f}"
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(img, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # count object
        count = len(target_detections)
        cv2.putText(img, f"Count: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # frame
        cv2.imshow("count objects", img)

        # key check
        key = cv2.waitKey(1)
        prop_val = cv2.getWindowProperty('count objects', cv2.WND_PROP_ASPECT_RATIO)
        if key != -1:
            subfunc.dbgprint(f"key pushed. keyid : {key}")
        if key in (27, 113): break  # esc, q
        if prop_val < 0: break      # close button
        if key == 114:              # r
            isReverse = not isReverse
        if key == 99:               # c
            isDrawWebCam = not isDrawWebCam
        if key == 118:              # v
            isVerbose = not isVerbose

    cap.release()
    cv2.destroyAllWindows()
    subfunc.dbgprint("LOOP end.")

if __name__ == "__main__":
    main()
