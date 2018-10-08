import tensorflow as tf
from keras import backend as K
import numpy as np
from keras.applications import vgg16
from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import decode_predictions
import io
from PIL import Image


class ImagenetModel(object):
    def __init__(self, GPU=True, num_cores=8, initialize_model=True):
        if GPU:
            num_GPU = 1
            num_CPU = 1
        else:
            num_CPU = 1
            num_GPU = 0

        if initialize_model:
            config = tf.ConfigProto(intra_op_parallelism_threads=num_cores,
                                    inter_op_parallelism_threads=num_cores, allow_soft_placement=True,
                                    device_count={'CPU': num_CPU, 'GPU': num_GPU},
                                    gpu_options={'per_process_gpu_memory_fraction': 0.4, 'allow_growth': True})
            session = tf.Session(config=config)
            K.set_session(session)
            self.model = vgg16.VGG16(weights='imagenet')

    def predict(self, image):
        numpy_image = img_to_array(image)
        image_batch = np.expand_dims(numpy_image, axis=0)
        processed_image = vgg16.preprocess_input(image_batch.copy())
        predictions = self.model.predict(processed_image)
        label = decode_predictions(predictions)
        return label

    def message_to_image(self, byte_string, shape=(500, 375), mode='RGB'):
        print(type(byte_string))
        image = Image.open(io.BytesIO(byte_string))#mode, shape, byte_string)
        return image