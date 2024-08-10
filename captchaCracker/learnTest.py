import glob
import os.path
import CaptchaCracker as cc

# 운영체제에 따라 경로 설정
if os_name == 'windows':
    img_save_directory = 'D:/python/captchaImages'
    weights_directory = 'D:/python/captchaCracker/weights'
    target_directory = 'D:/python/captchaCracker/target'
elif os_name == 'darwin':
    home_directory = os.path.expanduser("~")
    img_save_directory = os.path.join(home_directory, 'python', 'captchaImages')
    weights_directory = os.path.join(home_directory, 'python', 'captchaCracker', 'weights')
    target_directory = os.path.join(home_directory, 'python', 'captchaCracker', 'target')
else:
    raise Exception("Unsupported OS")

#이미지 학습
def learn_img():
    img_path_list = glob.glob(img_save_directory + '/*.png')    #학습 데이터 이미지 경로 (파일명이 숫자와 같아야함)
    img_width = 150 #이미지 넓이
    img_height = 50 #이미지 높이
    CM = cc.CreateModel(img_path_list, img_width, img_height)   #학습모델 생성
    model = CM.train_model(epochs=100)  #반복 학습 시작
    model.save_weights(weights_directory + '/weights.h5')    #학습 결과 가중치 저장


#가중치로 결과 도출
def result_img():
    target_img_path = target_directory + '/target.png'    #타켓 이미지 경로
    img_width = 150 #타켓 이미지 넓이
    img_height = 50 #타켓 이미지 높이
    img_length = 6  #타켓 이미지가 포함한 문자 수
    img_char = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}   #타켓 이미지안에 포함된 문자들
    weights_path = weights_directory + '/weights.h5' #학습 결과 가중치 경로
    AM = cc.ApplyModel(weights_path, img_width, img_height, img_length, img_char)   #결과 가중치를 가지는 모델 생성
    pred = AM.predict(target_img_path)  #결과 도출
    return pred

#learn_img() #최초 가중치 생성을 위한 학습시 주석해제
