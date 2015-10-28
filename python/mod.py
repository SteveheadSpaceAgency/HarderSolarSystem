import os, copy, math
from config import Module
from bodies import PlanetaryBody, bodies

# settings
base_directory_format = "%dx"
mod_name_format = "HarderSolarSystem-%dx"
kopernicus_config_name = "HSSKopernicus.cfg"
remote_tech_compatability_config_name = "RemoteTech_HSS.cfg"
game_data_directory = "GameData"
compatability_directory = "Compatability"
axial_tilt = 23.4392811

def generate_mod(scale, directory):
	base_path = os.path.join(directory, base_directory_format % scale)
	game_data_path = os.path.join(base_path, game_data_directory)
	mod_path = os.path.join(game_data_path, mod_name_format % scale)
	if not os.path.exists(mod_path):
		os.makedirs(mod_path)
	generate_kopernicus_config(scale, mod_path)
	if scale != 1:
		generate_compatability_configs(scale, mod_path)

def generate_compatability_configs(scale, mod_path):
	compatability_path = os.path.join(mod_path, compatability_directory)
	if not os.path.exists(compatability_path):
		os.makedirs(compatability_path)
	generate_remote_tech_compatability_config(scale, compatability_path)

def generate_kopernicus_config(scale, mod_path):
	config_path = os.path.join(mod_path, kopernicus_config_name)
	this_bodies = copy.deepcopy(bodies)
	
	main_module = Module("@Kopernicus:AFTER[Kopernicus]")
	
	for body in this_bodies:
		if scale != 1:
			body.rescale(scale)
		body_module = Module("@Body[%s]" % body.name)
		
		if isinstance(body, PlanetaryBody):
			body.rotate_orbit(x_rot=axial_tilt)
			orbit_module = Module("@Orbit")
			if scale != 1:
				orbit_module.add_parameter("semiMajorAxis = %d" % round(body.a))
			orbit_module.add_parameter("inclination = %f" % body.i)
			orbit_module.add_parameter("longitudeOfAscendingNode = %f" % body.o)
			orbit_module.add_parameter("argumentOfPeriapsis = %f" % body.w)
			body_module.add_child(orbit_module)
		
		properties_module = Module("@Properties")
		if scale != 1:
			properties_module.add_parameter("radius = %d" % round(body.r))
			if not body.is_tidally_locked:
				properties_module.add_parameter("rotationPeriod = %f" % body.rot)
		body_module.add_child(properties_module)
		
		if body.name == "Kerbin":
			body_module.add_child(generate_space_center_module(scale))
		
		main_module.add_child(body_module)
	
	main_module.write_to_file(config_path)
		
def generate_remote_tech_compatability_config(scale, compatability_path):
	config_path = os.path.join(compatability_path, remote_tech_compatability_config_name)
	main_module = Module("@PART[*]:HAS[@MODULE[ModuleRTAntenna],!MODULE[ModuleCommand]]:NEEDS[RemoteTech]:Final")
	
	antenna_module = Module("@MODULE[ModuleRTAntenna]")
	antenna_module.add_parameter("@Mode0DishRange *= %f" % scale)
	antenna_module.add_parameter("@Mode1DishRange *= %f" % scale)
	antenna_module.add_parameter("@Mode0OmniRange *= %f" % scale)
	antenna_module.add_parameter("@Mode1OmniRange *= %f" % scale)
	
	main_module.add_child(antenna_module)
	main_module.write_to_file(config_path)
	

def generate_space_center_module(scale):
	ksc_module = Module("SpaceCenter")
	ksc_module.add_parameter("latitude = 28.608389")
	ksc_module.add_parameter("longitude = -19.7")
	ksc_module.add_parameter("lodvisibleRangeMult = 6")
	ksc_module.add_parameter("repositionRadiusOffset = 53")
	ksc_module.add_parameter("reorientFinalAngle = 305")
	ksc_module.add_parameter("decalLatitude = 28.608389")
	ksc_module.add_parameter("decalLongitude = -19.7")
	ksc_module.add_parameter("heightMapDeformity = 80")
	ksc_module.add_parameter("absoluteOffset = 0")
	ksc_module.add_parameter("absolute = true")
	ksc_module.add_parameter("radius = 10000")
	return ksc_module