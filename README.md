# Drone ID Maker

Python Library for creating drone IDs

![Example Output](./examples/03-1312.png)

## Install Dependancies

```bash
pip install -r requirements.txt
```

## Usage

```python
# import the class
from id_number import DroneTag

# Make a drone
drone_data = {
    "name": "Rory",
	"drone_id": "03-1312"
	"qr_data": "03-1312"
    "title": "Poké Drone",
    "front_color": "#DC141E",
	"back_color": "#000000",
	"id_size": 83,
	"title_size": 69,
    "logo": "./assets/rocket.png",
	"logo_color": "#DC141E",
    "logo_size": 0.2,
    "logo_border": 0.2
	"border_radius": 0.125
}
drone_tag = DroneTag(drone_data)

# The only key needed is 'name' or 'drone_id', 
# name is used to generate a drone_id and the rest will use default values.
# More Examples in id_number.py

```

# Docs
### General
- `'front_color': HEX COLOR`\
  	Sets the color of text and images.\
  	When ommited, the default is white.
- `'back_color': HEX COLOR`\
  	Sets the color of the backgroud.\
  	When ommited, the default is black.
- `'qr_data': BYTES|STRING`\
  	Sets what data the QR code stores. 
	This can be any "bytes" object or string, and the QR code will change "versions" to fit the data.\
	When ommited, `drone_id` will be used as the QR code text.


### Text
- `'name': STRING`\
	The name is hashed to create `drone_id` in the format of '00-0000'.
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
