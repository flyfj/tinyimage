import os

from tinyimage import TinyImage


class TestTinyImage(object):
  def test_load_file(self):
    img = TinyImage(
        path=os.path.join(os.path.dirname(__file__), "data", "cat.jpg"))
    assert img.img_arr.size == 700 * 1000 * 3

  def test_load_url(self):
    img = TinyImage(
        url="https://www.readersdigest.ca/wp-content/uploads/sites/14/2011/01/4-ways-cheer-up-depressed-cat.jpg"
    )
    assert img.img_arr.size == 700 * 1000 * 3

  def test_load_base64(self):
    with open("./data/base64_sample.txt", "r") as f:
      base64_data = f.read()
    img = TinyImage(img_base64=base64_data)
    assert img.img_arr.size == 700 * 1000 * 3
    base64_export = img.to_base64()
    new_img = TinyImage(img_base64=base64_export)
    # assert new_img.img_arr.size == 700 * 1000 * 3
    assert base64_export == base64_data

  def test_save_file(self):
    img = TinyImage(
        path=os.path.join(os.path.dirname(__file__), "data", "cat.jpg"))
    img.save_to_file("./data/save.png")
    assert os.path.exists("./data/save.png")

  def test_array(self):
    img = TinyImage(
        path=os.path.join(os.path.dirname(__file__), "data", "cat.jpg"))
    assert img.to_array().shape == (700, 1000, 3)

  def test_resize(self):
    img = TinyImage(
        path=os.path.join(os.path.dirname(__file__), "data", "cat.jpg"))
    img.resize(new_sz=(350, 500))
    assert img.to_array().shape == (350, 500, 3)
    img.resize(max_dim=1000)
    assert img.to_array().shape == (700, 1000, 3)
