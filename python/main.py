import os
from mod import generate_mod

# settings
output_directory_name = "output"
scales_supported = [1, 2, 3, 4, 'generic']

# directories
script_directory = os.path.dirname(os.path.realpath(__file__))
base_directory = os.path.dirname(script_directory)
output_directory = os.path.join(base_directory, output_directory_name)

# generate configs
for scale in scales_supported:
	generate_mod(scale=scale, directory=output_directory)