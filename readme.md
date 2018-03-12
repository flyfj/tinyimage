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
img_from_binary = DeepImage(img_bin=img_binary_string)
img_from_base64 = DeepImage(img_base64=base64_encoded_string)

# export to different formats.

```

## Contributing

If you have questions, comments, bug reports or adding new data sources, please create an issue or send an [email](mailto:jiefengdev@gmail.com).

## License

[MIT License](./LICENSE)