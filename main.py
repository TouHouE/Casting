import scipy.io as sio
import cv2
import os
CASTING_ROOT = r"C:\Users\daskv\Desktop\DataBase\Castings"


class Image:
    def __init__(self, image, name):
        self.org = image
        self.bbx_img = image.copy()
        self.name = name
        self.bbx_exist = False
        self.bbx = []

    def set_bbx(self, bbx):
        self.bbx_exist = True
        yolo_bbx = convert2yolo(bbx, self.org.shape)
        yolo_bbx = [abs(info) for info in yolo_bbx]
        self.bbx.append(yolo_bbx)

    def save(self):
        folder, name = self.name.split('_')
        if not os.path.exists(f'./yolo_casting/img/{folder}'):
            os.mkdir(f'./yolo_casting/img/{folder}')
        if not os.path.exists(f'./yolo_casting/label/{folder}'):
            os.mkdir(f'./yolo_casting/label/{folder}')

        with open(f'./yolo_casting/label/{folder}/{self.name.split(".")[0]}.txt', 'w+') as fout:
            for line in self.bbx:
                fout.write('0 ')
                for info in line:
                    fout.write(f'{info} ')
                fout.write('\n')

        cv2.imwrite(f'./yolo_casting/img/{folder}/{self.name}', self.org)


def convert2yolo(org_format, img_shape):
    x_min, x_max, y_min, y_max = org_format
    img_h, img_w = img_shape
    yolo_x = ((x_max + x_min) / 2 - 1) / img_w
    yolo_y = ((y_max + y_min) / 2 - 1) / img_h
    yolo_w = (x_max - x_min) / img_w
    yolo_h = (y_max - y_min) / img_h
    results = [yolo_x, yolo_y, yolo_w, yolo_h]
    return results


def get_bbx(root):
    if os.path.exists(f'{root}/BoundingBox.mat'):
        mat = sio.loadmat(f'{root}/BoundingBox.mat')
        return mat['bb']
    if os.path.exists(f'{root}/ground_truth.txt'):
        with open(f'{root}/ground_truth.txt', 'r') as fin:
            all_line = fin.readlines()
        all_line = [line.replace("\n", '') for line in all_line]
        all_line = [list(filter(lambda x: 'e' in x, line.split(' '))) for line in all_line]
        all_line = [map(int, map(float, line)) for line in all_line]
        return all_line
    return None


def main(C_series):
    C_series_folder = f'{CASTING_ROOT}/{C_series}'

    all_bbx = get_bbx(C_series_folder)
    if all_bbx is None:
        print(f"The bbx of {C_series} doesn't exist")
        return None
    all_img = [Image(cv2.imread(f'{C_series_folder}/{name}', 0), name) for name in list(filter(lambda x: '.png' in x, os.listdir(C_series_folder)))]

    for bbx in all_bbx:
        bbx = [int(tmp) for tmp in bbx]
        img_series, bbx = bbx[:1], bbx[1:]

        target = all_img[img_series[0] - 1]
        target.set_bbx(bbx)

    for img in all_img:
        if not img.bbx_exist:
            continue
        img.save()

if __name__ == '__main__':
    ALL_C = os.listdir(f'{CASTING_ROOT}')

    for c in ALL_C:
        main(c)