# Drone ID Maker

## Python Library for creating drone IDs

<img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/03-1312.png" width="300" /> <img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/%230000.png" width="300" />\
<img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/U992.png" width="364" /> <img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/12-1290.png" width="234" />

----

## Install Dependancies
```bash
pip install -r requirements.txt
```

## Usage
### Simple Configuration

```python
# import the class
from DroneTools import DroneTag

drone_ids = [] # This is optional. Used to track used IDs to handle hash collisions.

# Make Drone
drone_data = {
        "name": "Rory",
        "title": "Pup Drone",
        "front_color": "#DC141E",
}
drone_tag = DroneTag(drone_data, drone_ids)

# The only key needed is 'name' or 'drone_id',
# name is used to generate a drone_id and the rest will use default values.

# Save your tag.
drone_tag.save("/path/to/output.png")

```
### Fine Grain Configuration
```python
from DroneTools import DroneTag

drone_ids = []
drone_data = {
    "name": "Some Name",  # Ignored in this example because 'drone_id' is present below
    "drone_id": "03-1312",
    "code_data": "03-1312",
    "title": "Poké Drone",
    "front_color": "#DC141E",
    "back_color": "#000000",
    "square": True,
    "barcode": False,
    "barcode_height": 20, # Ignored in this example because 'barcode' is set to 'False' above
    "qr_roundness": 1,

    "top_padding": 20,
    "bottom_padding": 0,
    "left_padding": 20,
    "right_padding": 0,
    "font_path": "./assets/font.otf"
    "text_margin": 75,    # 'text_margin' and 'text_padding' are ignored in this example because
    "text_padding": 0,    # 'id_padding_override' + 'title_padding_override' and
                          # 'id_margin_override' + 'title_margin_override' are set below
    "id_size": 83,
    "id_shift": 0,
    "id_margin_override": 75,
    "id_padding_override": 0,
    "title_size": 69,
    "title_shift": 0,
    "title_margin_override": 75,
    "title_padding_override": 0,

    "logo": "./assets/rocket.png",
    "logo_color": "#DC141E",
    "logo_size": 0.2,
    "logo_border": 0.2,
    "border_radius": 0.125
}
drone_tag = DroneTag(drone_data, drone_ids)
drone_tag.save("/path/to/output.png")

```
More examples and tests in `Sample.py`

# Docs

`drone_tag = DroneTag(drone_data, drone_ids)`

- `drone_data: DICT` [Required]\
    Options used to create the drone tag.\
    Keys and vaues for options are below.

- `drone_ids: ARRAY` [Optional]\
    Optionally used to store a running list of generated IDs when using the `name` option.
    This array is not used unless `name` is set.\
    When ommited, hash collisions handling when using the `name` option will be disable.

##### Data Memebers
- `drone_data DICT`
    Stored options used to construct the drone tag.
- `drone_id: STRING`
    Stores options the drone id in String format.
- `drone_ids: ARRAY`
    Stored a running list of generated IDs when using the `name` option.
- `drone_tag: PIL.Image.Image`
    Stored drone tag image.

##### Methods
- `save([PATH: STRING])`\
    Saves the drone tag image to a specified path.
    If no path is provided the file is saved under the ID number in the current working directory.
- `get_image()`\
    Returns the drone tag image as a `PIL.Image.Image` object.

## General Options
- `'front_color': HEX COLOR`\
    Sets the color of text and images.\
    When ommited, the default is white.
- `'back_color': HEX COLOR`\
    Sets the color of the backgroud.\
    When ommited, the default is black.
- `'square': BOOLEAN`\
    When 'True' the generated image is padded out into a perfect square.\
    When ommited, the default is 'False'.
- `'top_padding': INT`\
    Adds padding to the top of the tag.\
	When omitted, the padding is selected automatically.
- `'bottom_padding': INT`\
    Adds padding to the bottom of the tag.\
	When omitted, the padding is selected automatically.
- `'left_padding': INT`\
    Adds padding to the left of the tag.\
	When omitted, the padding is selected automatically.
- `'right_padding': INT`\
    Adds padding to the right of the tag.\
	When omitted, the padding is selected automatically.

## Text Options
- `'front_path': STRING`\
    Sets path for the font file used for text to a custom one.\
    When ommited, the default font is used.
- `'text_margin': INT`\
    Sets the margin on the left and right of all text.
	This option will be ignored by text using the 'margin_override' option.\
    Set this when using a custom font.\
    When ommited, text margins are selected automatically.
- `'text_padding': INT`\
    Sets the padding seperating all text from the code.
	This option will be ignored by text using the text's 'padding_override' option.\
    Set this when using a custom font.\
    When ommited, text padding is selected automatically.

##### ID Options (Top Text)

- `'name': STRING`\
    The name is hashed to create `drone_id` in the format of '00-0000'.
    The first number is always 0 unless the id exists in `drone_ids`, in which case it will increment.
    This option is ignore when `drone_id` is set.\
    If ommited, `drone_id` must be set.
- `'drone_id': STRING`\
    Used to set the ID number and formatting. `name` is ignore when this option is set.\
    If ommited, `name` must be set.
- `'id_size': INT`\
    Overrides the ID number's size.\
    When ommited, the ID's size is selected automatically.
- `'id_shift': INT`\
    Shifts the ID text left or right of center. Postitive numbers will shift right
	while negative number will shift left.\
	When ommited, the ID will be centered.
- `'id_margin_override': INT`\
    Overrides the margin on the left and right of the ID.
	When set, the ID text will ignore `text_margin`. \
    When ommited, the ID's margin is selected automatically.
- `'id_padding_override': INT`\
    Overrides the padding seperating the ID from the code.
	When set, the ID text will ignore `text_padding`. \
    When ommited, the ID's padding is selected automatically.

##### Title Options (Side Text)

- `'title': STRING`\
    Sets the drone's title on the sidebar.\
    When ommited, the sidebar will not be rendered.
- `'title_size': INT`\
    Overrides the title's size.\
    When ommited, the title's size is selected automatically.
- `'title_shift': INT`\
    Shifts the Title text up or down of center. Postitive numbers will shift up
	while negative number will shift down.\
	When ommited, the title will be centered.
- `'title_margin_override': INT`\
    Overrides the margin on the top and bottom of the title.
	When set, the title text will ignore `text_margin`. \
    When ommited, the title's margin is selected automatically.
- `'title_padding_override': INT`\
    Overrides the padding seperating the title from the code.
	When set, the title text will ignore `text_padding`. \
    When ommited, the title's padding is selected automatically.

## QR/Barcode Options

- `'barcode': BOOLEAN`\
    When 'True' a barcode is generated instead of a QR Code.
    This should only be used with small sizes of data, such as the ID number. 
	Links or messages should use a QR code.\
    Logo options are ignored in this mode.\
    When ommited, the default is 'False'.
- `'code_data': BYTES|STRING`\
    Sets what data the QR code stores.
    This can be any "bytes" object or string, and the QR code will change "versions" to fit the data.\
    When ommited, `drone_id` will be used as the QR code text.
- `'qr_roundness': [ 1.0 - 0.0 ]`\
    Sets roundness of the lines on the QR code. 1 is fully round and 0 is fully square.
    This option is ignored when `barcode` is set to 'True'.\
    When ommited, the QR code is rounded.
- `'barcode_height': [ 1.0 - 0.0 ]`\
    Sets height of the lines on the Barcode.
    This option is ignored when `barcode` is set to 'False' or ommited.\
    When ommited, the Barcode height is selected automatically.

##### Logo Options (Not compatible with barcodes)

- `'logo': STRING`\
    Path to the logo file. This is intended to be a solid color png.\
    This option is ignored when `barcode` is set to 'True'.\
    When ommited, the logo will not be rendered.
- `'logo_color': HEX COLOR`\
    Overrides the logo's color.\
    When ommited, `front_color` will be used.
- `'logo_size': [ 1.0 - 0.0 ]`\
    Sets the logo's size.\
    When ommited, the default is `0.2`.
- `'logo_border': [ 1.0 - 0.0 ]`\
    Sets the logo's border thickness.\
    When ommited, the default is `0.2`.
- `'border_radius': [ 1.0 - 0.0 ]`\
    Sets the logo's border corner roundness.\
    When ommited, the default is `0.125`.
