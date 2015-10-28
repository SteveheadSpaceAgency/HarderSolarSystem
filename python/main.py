import os
from config import generate_config

# settings
output_directory_name = "output"
scales_supported = [1, 2, 3]
config_name_format = "HarderSolarSystem-%dscale"

# directories
script_directory = os.path.dirname(os.path.realpath(__file__))
base_directory = os.path.dirname(script_directory)
output_directory = os.path.join(base_directory, output_directory_name)

# generate configs
for scale in scales_supported:
	config_name = config_name_format % scale
	generate_config(scale=scale, directory=output_directory, name=config_name)