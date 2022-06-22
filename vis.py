import cv2
import matplotlib.pyplot as plt
import json


def read_json(json_path):
    with open(json_path, 'r') as f:
        content = json.load(f)
    bbx = content['2.jpg44593']['regions'][0]['shape_attributes']
    bbx = [bbx['x'], bbx['y'], bbx['width'], bbx['height']]
    bbx = [int(i) for i in bbx]
    return bbx


def main():
    image = cv2.imread('./2.jpg')
    bbx = read_json('./2.json')
    image_with_bbx = cv2.rectangle(image.copy(), (bbx[0], bbx[1]), (bbx[0] + bbx[2], bbx[1] + bbx[3]), color=(255, 128, 255), thickness=3)
    plt.subplot(1, 2, 1)
    plt.imshow(image[:, :, ::-1])
    plt.subplot(1, 2, 2)
    plt.imshow(image_with_bbx[:, :, ::-1])
    plt.show()

if __name__ == '__main__':
    main()