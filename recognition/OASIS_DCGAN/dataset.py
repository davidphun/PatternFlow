import os
import PIL
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from recognition.OASIS_DCGAN.config import Config


def read_dataset(switch='train'):
    if switch == 'test':
        image_list = os.listdir(Config.test_dir)
        prefix = Config.test_dir + '/'
    elif switch == 'valid':
        image_list = os.listdir(Config.val_dir)
        prefix = Config.val_dir + '/'
    else:  # switch == 'train
        image_list = os.listdir(Config.train_dir)
        prefix = Config.train_dir + '/'
    print('Maximum images size:', len(image_list), 'and Expected images size:', Config.BUFFER_SIZE)

    x = np.empty([min(Config.BUFFER_SIZE, len(image_list)), Config.IMG_SIZE[0], Config.IMG_SIZE[1], 1])

    for i in range(min(Config.BUFFER_SIZE, len(image_list))):
        print('Progress: [%d / %d]' % (i + 1, Config.BUFFER_SIZE), end='\r')
        image_path = prefix + image_list[i]

        # img = tf.image.decode_and_crop_jpeg(tf.io.read_file(image_path), crop_window=[0, 0, 128, 128], channels=1)
        img = tf.image.decode_png(tf.io.read_file(image_path), dtype=tf.dtypes.uint8, channels=1)
        img = tf.image.resize(img, Config.IMG_SIZE, method='nearest')

        # # plot image
        # plt.imshow(img, cmap=plt.cm.gray)
        # plt.show()

        x[i] = img.numpy()

    images = x.reshape(x.shape[0], Config.IMG_SIZE[0], Config.IMG_SIZE[1], 1).astype('float32')
    images = images * (2.0 / 255) - 1.0

    # Set batch
    print('\'%s\' Dataset has been loaded' % switch)
    dataset = tf.data.Dataset.from_tensor_slices(images)
    return dataset if switch == 'test' or switch == 'valid' else dataset.batch(Config.BATCH_SIZE)
