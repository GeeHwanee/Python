import glob
import platform
import os
import CaptchaCracker as cc

# 운영체제별 기본 경로 생성
def get_default_directories(base_name='captchaCracker'):
    os_name = platform.system().lower()
    if os_name == 'windows':
        base_dir = f'D:/python/{base_name}'
    elif os_name == 'darwin':
        home_directory = os.path.expanduser("~")
        base_dir = os.path.join(home_directory, 'python', base_name)
    else:
        raise Exception("Unsupported OS")

    return {
        'img_save': os.path.join(base_dir, 'dataset'),
        'weights': os.path.join(base_dir, 'weights'),
        'target': os.path.join(base_dir, 'target')
    }

# 학습 함수
def learn_img(img_dir, weights_path, img_width=150, img_height=50, epochs=200):
    """
    img_dir: 학습 이미지 폴더
    weights_path: 학습 결과 가중치 저장 경로
    img_width, img_height: 학습 이미지 크기
    epochs: 학습 반복 횟수
    """
    img_path_list = glob.glob(os.path.join(img_dir, '*.png'))
    cm = cc.CreateModel(img_path_list, img_width, img_height)
    model = cm.train_model(epochs=epochs)
    model.summary()
    model.save_weights(weights_path)
    print(f"학습 완료. 가중치 저장: {weights_path}")

# 예측 함수
def predict_img(target_img_path, weights_path, img_width=150, img_height=50, img_length=6, img_char=None):
    """
    target_img_path: 예측할 타겟 이미지
    weights_path: 학습 가중치 경로
    img_width, img_height: 이미지 크기
    img_length: 이미지에 포함된 문자 수
    img_char: 이미지에 포함된 문자 집합
    """
    if img_char is None:
        img_char = {'0','1','2','3','4','5','6','7','8','9'}

    am = cc.ApplyModel(weights_path, img_width, img_height, img_length, img_char)
    pred = am.predict(target_img_path)
    print(f"예측 결과: {pred}")
    return pred

# ======= 사용 예시 =======
dirs = get_default_directories()

# 학습 (처음 한번만)
# learn_img(dirs['img_save'], os.path.join(dirs['weights'], 'weights_test.h5'), epochs=1000)
# loss: 학습용 데이터에서의 손실 값(loss)
# 모델이 실제 정답과 예측값 사이에서 얼마나 오차가 있는지를 나타냄
# 낮을수록 좋음 → 예측이 실제값과 가까움
# 예: 9.1990 → 아직 오차가 좀 있음

#val_loss: 검증용 데이터(validation set)에서의 손실 값
#학습 데이터가 아닌 새로운 데이터에서 모델 성능을 측정
#낮을수록 좋음
#loss < val_loss → 학습 데이터에 비해 검증 데이터 성능이 떨어짐 → 과적합 가능성 시사

# 예측
#predict_img(os.path.join(dirs['target'], 'target.png'), os.path.join(dirs['weights'], 'weights.h5'))
