from util import ImagenetModel, ThreadedVideoCamera
import PIL


def test_model_predict():
    camera = ThreadedVideoCamera()
    image = PIL.Image.open("test/unit/puppy.jpg")
    image = camera.resize(image)
    model = ImagenetModel()
    result = model.predict(image)
    result_names = [r[1] for r in result[0]]
    assert "Chesapeake_Bay_retriever" in result_names

