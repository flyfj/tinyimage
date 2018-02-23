import unittest

from owlimage import OwlImage


class OwlImageTester(unittest.TestCase):
  def test_img_from_file(self):
    img = OwlImage(
        fp="/home/jiefeng/Pictures/628bc1f5baba49fed675368f1483b0d6.jpg")
    img.show("test image")


if __name__ == "__main__":
  unittest.main()
