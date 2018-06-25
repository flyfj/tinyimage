"""Image object representation.
"""

from PIL import Image, ImageDraw
import numpy as np

import cv2

from deepimage import tools


class DeepImage(object):
  """Image object.

  This class should be the interface to operate on images.
  """

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
      img_bin: bytes of image data.
      img_base64: base64 bytes of image data.
      img_arr: numpy array of image.
    """
    # internal image as numpy array: <height, width, channels> in RGB order.
    self.img_arr = None
    # reference to the image, file or url.
    self.img_ref = None
    assert not fp or not url or not img_bin or not img_base64 or not img_arr, "you need to provide either file path or url."
    if fp:
      cv_img = cv2.imread(fp)
      self.img_arr = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    if url:
      self.img_arr = tools.read_img_arr_from_url(url)
    if img_bin:
      self.img_arr = tools.img_bin_to_img_arr(img_bin)
    if img_base64:
      self.img_arr = tools.base64_to_img_arr(img_base64)
    if img_arr is not None:
      # don't directly check img_arr.
      self.img_arr = img_arr
    self.img_ref = self.to_datauri()

  def get_ref(self):
    """Get image reference.
    """
    return self.img_ref

  def clone(self):
    """Create a deep copy of the image.
    """
    new_img = DeepImage(img_arr=np.copy(self.img_arr))
    return new_img

  def width(self):
    return self.img_arr.shape[1]

  def height(self):
    return self.img_arr.shape[0]

  def write_to_file(self, save_fn):
    """Write the image to file.
    """
    tools.write_img_arr(self.img_arr, save_fn)

  def to_base64(self):
    """Export image data as base64 string.
    """
    img_base64 = tools.img_arr_to_base64(self.img_arr)
    return tools.bytes_to_str(img_base64)

  def to_datauri(self):
    """Export datauri string used in html/css.
    """
    img_base64_str = self.to_base64()
    img_datauri = tools.base64_to_data_uri(img_base64_str)
    return img_datauri

  def to_binary(self):
    """Export binary bytes.
    """
    img_base64_str = self.to_base64()
    img_base64 = tools.str_to_bytes(img_base64_str)
    img_bin = tools.base64_to_img_bin(img_base64)
    return img_bin

  def to_array(self):
    """Export numpy array (height, width, channels).
    """
    return self.img_arr

  def to_opencv_img(self):
    """Convert array to bgr format.
    """
    return self.img_arr.copy()[:, :, ::-1]

  def to_gray(self):
    """Convert to grayscale.
    """
    gray_img = cv2.cvtColor(self.img_arr, cv2.COLOR_RGB2GRAY)
    return gray_img

  def get_base64_sha_encoding(self):
    """Encode base64 of the image.

    SHA2 is used.
    """
    img_base64 = tools.img_arr_to_base64(self.img_arr)
    return tools.base64_to_sha256(img_base64)

  def to_pil_img(self):
    """Convert to pil image.
    """
    pil_img = tools.img_arr_to_pil_img(self.img_arr)
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
      new deepimage object with drawn image.
    """
    num_box = len(boxes)
    num_text = len(texts)
    assert num_text == 0 or num_text == num_box
    cur_img = self.to_pil_img()
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
    return DeepImage(img_arr=np.copy(tools.pil_img_to_img_arr(cur_img)))

  def show(self, fig_title):
    """Display image in a titled window.
    """
    tools.show_img_arr(self.img_arr, fig_title)

  def resize(self, new_sz=None, max_dim=None):
    """Resize image.

    Args:
      new_sz: (new_height, new_width).
      max_dim: size of maximum dimension.
    """
    assert new_sz is not None or max_dim is not None, "either new size or max dim has to be provided."
    if max_dim is not None:
      new_sz = tools.get_new_dim(self.width(), self.height(), max_dim)
      new_sz = (new_sz[1], new_sz[0])
    self.img_arr = cv2.resize(self.img_arr, (new_sz[1], new_sz[0]))
