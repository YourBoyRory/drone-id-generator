# Drone ID Maker

Python Library for creating drone IDs

<img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/examples/03-1312.png" width="300" /> <img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/examples/%230000.png" width="300" />\
<img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/examples/U992.png" width="354" /> <img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/examples/12-1290.png" width="244" />

## Install Dependancies

```bash
pip install -r requirements.txt
```

## Usage

```python
# import the class
from DroneTools import DroneTag


drone_ids = [] # This is optional. Used to track used IDs to handle hash collisions.

# Make a drone
drone_data = {
    "name": "Rory",
    "drone_id": "03-1312",
    "code_data": "03-1312",
	"barcode": False
    "title": "Poké Drone",
    "front_color": "#DC141E",
    "back_color": "#000000",
    "id_size": 83,
    "title_size": 69,
    "logo": "./assets/rocket.png",
    "logo_color": "#DC141E",
    "logo_size": 0.2,
    "logo_border": 0.2,
    "border_radius": 0.125
}
drone_tag = DroneTag(drone_data, drone_ids)

# The only key needed is 'name' or 'drone_id',
# name is used to generate a drone_id and the rest will use default values.
# More Examples in DroneTools.py

# Save your tag.
drone_tag.save("/path/to/output")

```

# Docs

`drone_tag = DroneTag(drone_data, drone_ids)`

- `drone_data: DICT` [Required]\
	Options used to create the drone tag.\
	Keys and vaues for options are below.

- `drone_ids: ARRAY` [Optional]\
	Optionally used to store a running list of generated IDs when using the `name` option.
	This array is not used unless `name` is set.\
	When ommited, hash collisions handling when using the `name` option will be disable.

### General
- `'front_color': HEX COLOR`\
  	Sets the color of text and images.\
  	When ommited, the default is white.
- `'back_color': HEX COLOR`\
  	Sets the color of the backgroud.\
  	When ommited, the default is black.
- `'code_data': BYTES|STRING`\
  	Sets what data the QR code stores. 
	This can be any "bytes" object or string, and the QR code will change "versions" to fit the data.\
	When ommited, `drone_id` will be used as the QR code text.
- `'barcode': BOOLEAN`\
  	When 'True' A barcode is generated instead of a QR Code. 
	This should only be used with small sizes of data, such as the ID number. Links or messages should use a QR code.\
	When ommited, the default is 'False'.


### Text
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
	When ommited, the ID size is selected automatically.
- `'title': STRING`\
	Sets the drone's title on the sidebar.\
	When ommited, the sidebar will not be rendered.
- `'title_size': INT`\
	Overrides the title's size.\
	When ommited, the ID size is selected automatically.

### Logo
- `'logo': STRING`\
  	Path to the logo file. This is intended to be a solid color png.\
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
