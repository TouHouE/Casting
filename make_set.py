import os
import shutil

class Image:
    def __init__(self, image_path):
        self.image_path = image_path
        self.label_path = image_path.replace("img", 'label').replace('png', 'txt')
    def save(self, phase):
        img_list = self.image_path.split('/')
        new_img_path = '/'.join(img_list[:-2])
        new_label_path = new_img_path.replace("img", 'label')
        name = img_list[-1]

        shutil.copy(self.image_path, f'{new_img_path}/{phase}/{name}')
        shutil.copy(self.label_path, f'{new_label_path}/{phase}/{name.split(".")[0]}.txt')

IMAGE_ROOT = './yolo_casting/img'

def get_dataset(current_folder):
    return [Image(f'{IMAGE_ROOT}/{current_folder}/{img_name}') for img_name in os.listdir(f'./yolo_casting/img/{current_folder}')]

def main(whole_dataset):
    random_dataset = whole_dataset
    size = len(whole_dataset)

    train_set = random_dataset[:size * 8 // 10]
    val_set = random_dataset[size * 8 // 10: size * 9 // 10]
    test_set = random_dataset[size * 9 // 10:]
    print(f'Train len: {len(train_set)}\nVal len: {len(val_set)}\nTest len: {len(test_set)}')
    print(f'Must: {size}')

    for train in train_set:
        train.save('train')

    for val in val_set:
        val.save('val')

    for test in test_set:
        test.save('test')



if __name__ == '__main__':
    all_folder = os.listdir('./yolo_casting/img')
    all_folder.remove('train')
    all_folder.remove('test')
    all_folder.remove('val')

    all_data = []
    for folder_name in all_folder:
        all_data.extend(get_dataset(folder_name))
    main(all_data)