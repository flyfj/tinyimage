import os
import unittest

from img_obj import DeepImage


class DeepImageTester(unittest.TestCase):
  def test_img_from_file(self):
    img = DeepImage(
        fp=os.path.join(os.path.dirname(__file__), "data", "cat.jpg"))
    with open("base64.txt", "w") as f:
      f.write(img.to_datauri())
      print("image data converted to base64")
    img.show("test image")
    print("base64 sha2 encoding: {}".format(img.get_base64_sha_encoding()))


if __name__ == "__main__":
  unittest.main()
