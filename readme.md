# TinyImage

TinyImage is a lightweight image object library.

Given there are various image processing and computer vision libraries out there, TinyImage can serve as a high level interface for image data
to easily enable exchange between different formats.

Only python 3 is tested now.

## Installation

```
pip install tinyimage
```

For development, use pipenv to configure environment.

## Usage

TinyImage object contains many handy method to export different formats of the image data and perform operations on image.

```python
from tinyimage import TinyImage

# create images from different sources.
img_from_file = TinyImage(file="path/to/image")
img_from_url = TinyImage(url="https://somedomain/eg.jpg")
img_from_binary = TinyImage(img_bin=img_binary_bytes)
img_from_base64 = TinyImage(img_base64=base64_encoded_string)

# save image to file.
img_obj.write_to_file("/path/to/file")

# export to different formats.
img_obj.to_array()
img_obj.to_datauri()
img_obj.to_opencv_img()
img_obj.to_pil_img()
img_obj.to_binary()
img_obj.to_gray()

# resize.
img_obj.resize(new_sz=(new_height, new_width))
img_obj.resize(max_dim=400)

# visualization.
img_obj.show("image window")
new_img = img_obj.draw_boxes([box1, box2])
```

## Development

To set up for development, do
```python
pip install -e .
```

To run tests, do
```python
python setup.py test
```

## Contributing

If you have questions, comments, bug reports or adding new data sources, please create an issue.

## License

[MIT License](./LICENSE)