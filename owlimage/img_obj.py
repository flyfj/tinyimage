"""Image object representation for owl.
"""

from PIL import Image, ImageDraw
import numpy as np

import img_tools


class OwlImage(object):
  """Image object for owl.

  This class should be the interface to operate on images.
  """
  # internal image as numpy array: <height, width, channels>.
  # in RGB order.
  img_arr = None
  # reference to the image, file or url.
  img_ref = None

  def __init__(self,
               fp=None,
               url=None,
               img_bin=None,
               img_base64=None,
               img_arr=None):
    """Create an image object from a file path or url.

    Args:
      fp: filepath.
      url: url path.
      img_base64: base64 string of image data.
      img_arr: numpy array of image.
    """
    assert not fp or not url or not img_base64 or not img_arr, "you need to provide either file path or url."
    if fp:
      self.img_arr = img_tools.read_img_arr(fp)
      self.img_ref = fp
    if url:
      self.img_arr = img_tools.read_img_arr_from_url(url)
      self.img_ref = url
    if img_bin:
      self.img_arr = img_tools.img_bin_to_img_arr(img_bin)
      self.img_ref = self.to_datauri()
    if img_base64:
      self.img_arr = img_tools.base64_to_img_arr(img_base64)
      self.img_ref = img_tools.base64_to_data_uri(img_base64)
    if img_arr is not None:
      self.img_arr = img_arr
      self.img_ref = self.to_datauri()

  def clone(self):
    new_img = OwlImage(img_arr=np.copy(self.img_arr))
    return new_img

  def width(self):
    return self.img_arr.shape[1]

  def height(self):
    return self.img_arr.shape[0]

  def write_to_file(self, save_fn):
    """Write the image to file.
    """
    img_tools.write_img_arr(self.img_arr, save_fn)

  def to_base64(self):
    img_base64 = img_tools.img_arr_to_base64(self.img_arr)
    return img_base64

  def to_datauri(self):
    img_base64 = self.to_base64()
    img_datauri = img_tools.base64_to_data_uri(img_base64)
    return img_datauri

  def to_binary(self):
    img_base64 = self.to_base64()
    img_bin = img_tools.base64_to_img_bin(img_base64)
    return img_bin

  def to_array(self):
    return self.img_arr

  def get_base64_sha_encoding(self):
    """Encode base64 of the image.

    SHA2 is used.
    """
    img_base64 = img_tools.img_arr_to_base64(self.img_arr)
    return img_tools.base64_to_sha256(img_base64)

  def get_pil_img(self):
    """Convert to pil image.
    """
    pil_img = img_tools.img_arr_to_pil_img(self.img_arr)
    return pil_img

  def draw_boxes(self,
                 boxes,
                 line_colors=None,
                 line_width=1,
                 to_fill=False,
                 texts=[]):
    """Draw a box on image.

    Args:
      boxes: [(xmin, ymin, width, height)].
      line_colors: [(r, g, b)].
      line_width: rectangle width.
      to_fill: if fill the box.
      texts: texts to show on the top left corner of each box.
    
    Returns:
      new owlimg object with drawn image.
    """
    num_box = len(boxes)
    num_text = len(texts)
    assert num_text == 0 or num_text == num_box
    cur_img = self.get_pil_img()
    draw_cxt = ImageDraw.Draw(cur_img)
    for idx, box in enumerate(boxes):
      new_box = [box[0], box[1], box[0] + box[2] - 1, box[1] + box[3] - 1]
      if line_colors is None:
        cur_color = (255, 0, 0)
      elif len(line_colors) == 1:
        cur_color = line_colors[0]
      else:
        assert len(line_colors) == num_box
        cur_color = line_colors[idx]
      draw_cxt.rectangle(new_box, outline=cur_color)
      # draw box lines.
      draw_cxt.line(
          [(new_box[0], new_box[1]), (new_box[0], new_box[3]),
           (new_box[2], new_box[3]), (new_box[2], new_box[1]),
           (new_box[0], new_box[1])],
          width=line_width,
          fill=cur_color)
      if num_text > 0:
        draw_cxt.text(
            (new_box[0] + 5, new_box[1] + 5), texts[idx], fill=cur_color)
    return OwlImage(img_arr=np.copy(img_tools.pil_img_to_img_arr(cur_img)))

  def show(self, fig_title):
    """Display image in a titled window.
    """
    img_tools.show_img_arr(self.img_arr, fig_title)

  def resize(self, new_sz):
    """Resize image.

    Args:
      new_sz: (new_height, new_width).
    """
    self.img_arr = self.img_arr.resize((new_sz[1], new_sz[0]))
