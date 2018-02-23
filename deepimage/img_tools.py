"""Image processing code.

NOTE: all base64 string is encoded from binary data.
"""

import base64
import hashlib
import mimetypes
import PIL.Image

import io
from cStringIO import StringIO
import urllib2

import numpy as np
""" IO """


def read_img_bin(img_fn):
  """Get image binary from an image file.

  Args:
    img_fn: image file path.
  Returns:
    image binary data.
  """
  with open(img_fn, "rb") as f:
    img_bin_data = f.read()
    return img_bin_data


def read_img_arr(img_fn):
  """Read image file to get ndarray.
  """
  img_bin = read_img_bin(img_fn)
  img_arr = img_bin_to_img_arr(img_bin)
  return img_arr


def read_img_base64(img_fn):
  """Read image file to get base64 string.
  """
  img_bin = read_img_bin(img_fn)
  img_base64 = img_bin_to_base64(img_bin)
  return img_base64


def write_img_arr(img_arr, save_fn):
  """Write image array to file.

  Args:
    img_arr: numpy array of image.
    save_fn: file to save image.
  """
  pil_img = img_arr_to_pil_img(img_arr)
  pil_img.save(save_fn)


def download_img_from_url(img_url):
  """Download image data from url.

  Args:
    img_url: url of the image.
  Returns:
    binary string of image, image format.
  """
  # print "Downloading image..."
  try:
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
    header = {'User-agent': user_agent}
    req_obj = urllib2.Request(img_url, None, header)
    res_fh = urllib2.urlopen(req_obj, timeout=10)
    img_bin = res_fh.read()
    content_type = res_fh.headers["content-type"]
    mimetypes.init()
    img_ext = mimetypes.guess_extension(content_type)
    if img_ext:
      # remove dot prefix.
      img_ext = img_ext[1:]
      if img_ext == "jpe":
        img_ext = "jpg"
    return img_bin, img_ext
  except Exception as ex:
    print "error downloading image from: {}. error: {}".format(img_url, ex)
    raise ex


def read_img_arr_from_url(img_url):
  """Read image data from url into array.
  """
  img_bin, _ = download_img_from_url(img_url)
  img_arr = img_bin_to_img_arr(img_bin)
  return img_arr


""" Type conversion """


def img_bin_to_base64(img_bin):
  """Convert image binary data to base64.

  Args:
    img_bin: binary image data/string.

  Returns:
    base64 of image data.
  """
  img_base64 = base64.b64encode(img_bin)
  return img_base64


def img_bin_to_img_arr(img_bin, use_grayscale=False):
  """Convert image binary data to numpy array.

  Args:
    img_bin: binary image data.
    use_grayscale: convert to grayscale.

  Returns:
    numpy array: (height, width, chs).
  """
  pil_img = PIL.Image.open(StringIO(img_bin))
  if use_grayscale:
    new_img = pil_img.convert("L")
  else:
    new_img = pil_img.convert("RGB")
  return np.array(new_img)


def img_bin_to_sha1(img_bin):
  """Hash image binary data to sha1.

  Args:
    img_bin: binary string of image.
  Returns:
    sha1 of the image.
  """
  img_sha1 = hashlib.sha1(img_bin).hexdigest()
  return img_sha1


def base64_to_img_bin(img_base64):
  """Decode base64 image to binary string.

  Args:
    img_base64: base64 image string.
  Returns:
    binary image data.
  """
  img_bin = base64.b64decode(img_base64)
  # or: img_bin = img_base64.decode("base64")
  return img_bin


def base64_to_sha256(img_base64):
  """Hash base64 image to sha256.

  Args:
    img_base64: base64 string of image.
  Returns:
    sha1 of the image.
  """
  img_sha = hashlib.sha256(img_base64).hexdigest()
  return img_sha


def base64_to_img_arr(img_base64, use_grayscale=False):
  """Convert base64 image to rgb numpy array.

  Args:
    img_base64: base64 image string.
    use_grayscale: convert to grayscale.
  Returns:
    numpy array: (height, width, chs)
  """
  img_bin_str = base64_to_img_bin(img_base64)
  return img_bin_to_img_arr(img_bin_str, use_grayscale)


def base64_to_data_uri(img_base64):
  """For display in html.
  """
  datauri = "data:image/jpg;base64," + img_base64
  return datauri


def img_arr_to_base64(img_arr):
  """Convert numpy array image to base64.
  """
  # arr to bin
  pil_img = img_arr_to_pil_img(img_arr)
  img_bin = pil_img_to_img_bin(pil_img)
  # bin to base64
  img_base64 = img_bin_to_base64(img_bin)
  return img_base64


def img_arr_to_pil_img(img_arr):
  """Convert numpy array image to pil image.
  """
  pil_img = PIL.Image.fromarray(img_arr)
  return pil_img


def pil_img_to_img_arr(pil_img, use_grayscale=False):
  """Convert pil image to numpy array.
  """
  if use_grayscale:
    new_img = pil_img.convert("L")
  else:
    new_img = pil_img.convert("RGB")
  return np.asarray(new_img)


def pil_img_to_img_bin(pil_img):
  """Convert pil image to binary string.
  """
  output = io.BytesIO()
  pil_img.save(output, format="JPEG")
  img_bin = output.getvalue()
  return img_bin


def show_img_arr(img_arr, title):
  """Display image array.

  Args:
    img_arr: numpy array of image.
    title: title name of the display window.
  """
  pil_img = PIL.Image.fromarray(img_arr)
  pil_img.show(title=title)


""" data processing. """


def get_new_dim(imgw, imgh, max_dim=400):
  """Get new image dimension with maximum constraint.

  Args:
    imgw: image width.
    imgh: image height.
    max_dim: maximum image dimension after.
  Returns:
    new img width and height.
  """
  new_imgw = imgw
  new_imgh = imgh
  if imgw > imgh:
    new_imgw = max_dim
    new_imgh = imgh * max_dim / imgw
  if imgh > imgw:
    new_imgh = max_dim
    new_imgw = imgw * max_dim / imgh
  return new_imgw, new_imgh
