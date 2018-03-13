# DeepImage

DeepImage is a lightweight image object library (despite it's called 'deep').

Given there are various image processing and computer vision libraries out there, DeepImage can serve as a unifed interface for image data
to easily enable exchange between different formats.

## Installation

```
pip install deepimage
```

## Usage

DeepImage object contains many handy method to export different formats of the image data and perform operations on image.

```python
from deepimage import DeepImage

# create images from different sources.
img_from_file = DeepImage(fp="path/to/image")
img_from_url = DeepImage(url="https://somedomain/eg.jpg")
img_from_binary = DeepImage(img_bin=img_binary_bytes)
img_from_base64 = DeepImage(img_base64=base64_encoded_string)

# export to different formats.
img_obj.to_array()
img_obj.to_datauri()
img_obj.to_opencv_img()
img_obj.to_pil_img()
img_obj.show("image window")
img_obj.resize((new_height, new_width))
img_obj.write_to_file("/path/to/file")
new_img = img_obj.draw_boxes([box1, box2])
```

## Contributing

If you have questions, comments, bug reports or adding new data sources, please create an issue or send an [email](mailto:jiefengdev@gmail.com).

## License

[MIT License](./LICENSE)