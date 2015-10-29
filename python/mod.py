import os, copy, math, shutil
from config import Module, format_float
from bodies import PlanetaryBody, bodies, opm_bodies

# settings
base_directory_format = "%sx"
mod_name_format = "HarderSolarSystem-%sx"
kopernicus_config_name = "HSSKopernicus.cfg"
opm_compatibility_config_name = "OuterPlanetsMod_HSS.cfg"
game_data_directory = "GameData"
compatibility_directory = "Compatibility"
axial_tilt = 23.4392811

def generate_mod(scale, directory):
	base_path = os.path.join(directory, base_directory_format % format_float(scale))
	game_data_path = os.path.join(base_path, game_data_directory)
	mod_path = os.path.join(game_data_path, mod_name_format % format_float(scale))
	static_path = os.path.join(os.path.dirname(directory), "static")
	if not os.path.exists(mod_path):
		os.makedirs(mod_path)
	generate_kopernicus_config(scale, mod_path)
	generate_compatibility_configs(scale, mod_path, static_path)

def generate_compatibility_configs(scale, mod_path, static_path):
	compatibility_path = os.path.join(mod_path, compatibility_directory)
	if not os.path.exists(compatibility_path):
		os.makedirs(compatibility_path)
	generate_remote_tech_settings_config(scale, compatibility_path, static_path)
	copy_contract_bug_fix_config(compatibility_path, static_path)
	generate_opm_compatibility_config(scale, compatibility_path)
	
def generate_remote_tech_settings_config(scale, compatibility_path, static_path):
	original_file = os.path.join(static_path, "RemoteTech_Settings.cfg")
	new_file = os.path.join(compatibility_path, "RemoteTech_Settings.cfg")
	with open(original_file, 'r') as f:
		original_file_data = f.read()
	new_file_data = original_file_data.replace("RangeMultiplier = 1", "RangeMultiplier = %s" % format_float(scale))
	with open(new_file, 'w') as f:
		f.write(new_file_data)
		
def copy_contract_bug_fix_config(compatibility_path, static_path):
	original_file = os.path.join(static_path, "Contract_Bug_Workaround.cfg")
	new_file = os.path.join(compatibility_path, "Contract_Bug_Workaround.cfg")
	shutil.copyfile(original_file, new_file)
	
	
def generate_opm_compatibility_config(scale, compatibility_path):
	config_path = os.path.join(compatibility_path, opm_compatibility_config_name)
	this_bodies = copy.deepcopy(opm_bodies)
	
	main_module = Module("@Kopernicus:AFTER[OPM]")
	
	for body in this_bodies:
		if scale != 1:
			body.rescale(scale)
		body_module = Module("@Body[%s]" % body.name)
		
		body_module.add_parameter("%%cacheFile = %s/Cache/%s.bin" % (mod_name_format % format_float(scale), body.name))
		
		if isinstance(body, PlanetaryBody):
			body.rotate_orbit(x_rot=axial_tilt)
			orbit_module = Module("@Orbit")
			if scale != 1:
				orbit_module.add_parameter("@semiMajorAxis = %d" % round(body.a))
			if not body.no_rotate:
				orbit_module.add_parameter("@inclination = %s" % format_float(body.i))
				orbit_module.add_parameter("@longitudeOfAscendingNode = %s" % format_float(body.o))
				orbit_module.add_parameter("@argumentOfPeriapsis = %s" % format_float(body.w))
			body_module.add_child(orbit_module)
			
		if scale != 1 and not body.is_potato:
			properties_module = Module("@Properties")
			properties_module.add_parameter("-mass = dummy")
			properties_module.add_parameter("@radius = %d" % round(body.r))
			if not body.is_tidally_locked:
				properties_module.add_parameter("@rotationPeriod = %s" % format_float(body.rot))
			body_module.add_child(properties_module)
		
		if scale != 1 and body.has_rings:
			rings_scale = format_float(1.0 / scale)
			rings_module = Module("@Rings")
			ring_module = Module("@Ring")
			ring_module.add_parameter("@outerRadius *= %s" % rings_scale)
			ring_module.add_parameter("@innerRadius *= %s" % rings_scale)
			rings_module.add_child(ring_module)
			body_module.add_child(rings_module)
		
		main_module.add_child(body_module)
	
	main_module.write_to_file(config_path)

def generate_kopernicus_config(scale, mod_path):
	config_path = os.path.join(mod_path, kopernicus_config_name)
	this_bodies = copy.deepcopy(bodies)
	
	main_module = Module("@Kopernicus:AFTER[Kopernicus]")
	
	for body in this_bodies:
		if scale != 1:
			body.rescale(scale)
		if body.name != "Eeloo":
			body_module = Module("@Body[%s]" % body.name)
		else:
			body_module = Module("@Body[%s]:NEEDS[!OPM]" % body.name)
			
		body_module.add_parameter("%%cacheFile = %s/Cache/%s.bin" % (mod_name_format % format_float(scale), body.name))
		
		if isinstance(body, PlanetaryBody):
			body.rotate_orbit(x_rot=axial_tilt)
			orbit_module = Module("@Orbit")
			if scale != 1:
				orbit_module.add_parameter("semiMajorAxis = %d" % round(body.a))
			if not body.no_rotate:
				orbit_module.add_parameter("inclination = %s" % format_float(body.i))
				orbit_module.add_parameter("longitudeOfAscendingNode = %s" % format_float(body.o))
				orbit_module.add_parameter("argumentOfPeriapsis = %s" % format_float(body.w))
			body_module.add_child(orbit_module)
		
		if scale != 1 and not body.is_potato:
			properties_module = Module("@Properties")
			properties_module.add_parameter("radius = %d" % round(body.r))
			if not body.is_tidally_locked:
				if body.name == "Kerbin":
					rot_speed = round(body.rot / 7200.0) * 7200
				else:
					rot_speed = body.rot
				properties_module.add_parameter("rotationPeriod = %s" % format_float(rot_speed))
			body_module.add_child(properties_module)
		
		if body.name == "Kerbin":
			body_module.add_child(generate_space_center_module(scale))
		
		main_module.add_child(body_module)
	
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