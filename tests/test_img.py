import os

from tinyimage import TinyImage


class TestTinyImage(object):
  def test_load_file(self):
    img = TinyImage(
        file=os.path.join(os.path.dirname(__file__), "data", "cat.jpg"))
    assert (img.img_arr.size == 700 * 1000 * 3)

  def test_load_binary(self):
    pass

  # def test_img_from_file(self):
  #   img = TinyImage(
  #       file=os.path.join(os.path.dirname(__file__), "data", "cat.jpg"))
  #   with open("base64.txt", "w") as f:
  #     f.write(img.to_datauri())
  #     print("image data converted to base64")
  #   # img.show("test image")
  #   print("base64 sha2 encoding: {}".format(img.get_base64_sha_encoding()))
  #   img.resize(max_dim=400)
  #   img.show("resize image")
