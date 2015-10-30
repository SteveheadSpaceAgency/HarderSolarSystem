import math
from physics import Vector


class Body(object):
	def __init__(self, name, r, rot="TL", is_potato=False, has_rings=False):
		self.name = name
		self.r = r
		self.rot = rot
		self.is_potato = is_potato
		self.has_rings = has_rings
		
	@property
	def is_tidally_locked(self):
		if self.rot == "TL":
			return True
		else:
			return False
		
	def rescale(self, scale):
		if not self.is_potato:
			self.r *= scale
			if not self.is_tidally_locked:
				self.rot = self.rot * scale / math.sqrt(scale)


class PlanetaryBody(Body):
	def __init__(self, name, r, a, i, o, w, no_rotate=False, *args, **kwargs):
		super(PlanetaryBody, self).__init__(name=name, r=r, *args, **kwargs)
		self.a = a
		self.i = i
		self.o = o
		self.w = w
		self.no_rotate=no_rotate
		
	def rescale(self, scale):
		super(PlanetaryBody, self).rescale(scale)
		self.a *= scale
		
	def rotate_orbit(self, x_rot=None, y_rot=None, z_rot=None):
		if self.no_rotate:
			return
		r, v = self.get_unitless_state_vectors()
		r.rotate(x_rot, y_rot, z_rot)
		v.rotate(x_rot, y_rot, z_rot)
		self.set_orbital_elements(r, v)
		
	def set_orbital_elements(self, pos, vel):
		pos.force_non_zero
		vel.force_non_zero
		Rx = pos.x
		Ry = pos.y
		Rz = pos.z
		Vx = vel.x
		Vy = vel.y
		Vz = vel.z
		
		R = math.sqrt(Rx * Rx + Ry * Ry + Rz * Rz)
		
		Hx = Ry * Vz - Rz * Vy
		Hy = Rz * Vx - Rx * Vz
		Hz = Rx * Vy - Ry * Vx
		H = math.sqrt(Hx * Hx + Hy * Hy + Hz * Hz)
		
		q = Rx * Vx + Ry * Vy + Rz * Vz

		i = math.acos(Hz / H)
		lan = 0;
		if i != 0:
			lan = math.atan2(Hx, -Hy)

		TAx = H * H / R - 1.0
		TAy = H * q / R
		TA = math.atan2(TAy, TAx)
		Cw = (Rx * math.cos(lan) + Ry * math.sin(lan)) / R

		Sw = 0
		if i == 0 or i == math.pi:
		   Sw = (Ry * math.cos(lan) - Rx * math.sin(lan)) / R
		else:
		   Sw = Rz / (R * math.sin(i))

		W = math.atan2(Sw, Cw) - TA
		if lan < 0:
			lan = 2.0 * math.pi + lan
		if W < 0:
			W = 2.0 * math.pi + W
		
		self.i = math.degrees(i)
		self.o = math.degrees(lan)
		self.w = math.degrees(W)
		
	def get_unitless_state_vectors(self):
		ec = 0.1 # need to use non-zero eccentricity
		i = math.radians(self.i)
		o0 = math.radians(self.o)
		w0 = math.radians(self.w)
		
		eca = ec / 2.0
		diff = 1000.0
		eps = 0.000001
		e1 = 0.0
		
		while diff > eps:
			e1 = eca - (eca - ec * math.sin(eca)) / (1 - ec * math.cos(eca))
			diff = math.fabs(e1 - eca)
			eca = e1
		
		ceca = math.cos(eca)
		seca = math.sin(eca)
		e1 = math.sqrt(math.fabs(1.0 - ec * ec))
		xw = ceca - ec
		yw = e1 * seca

		edot = 1.0 / (1.0 - ec * ceca)
		xdw = -edot * seca
		ydw = e1 * edot * ceca

		Cw = math.cos(w0)
		Sw = math.sin(w0)
		co = math.cos(o0)
		so = math.sin(o0)
		ci = math.cos(i)
		si = math.sin(i)
		swci = Sw * ci
		cwci = Cw * ci
		pX = Cw * co - so * swci
		pY = Cw * so + co * swci
		pZ = Sw * si
		qx = -Sw * co - so * cwci
		qy = -Sw * so + co * cwci
		qz = Cw * si
		x = xw * pX + yw * qx
		y = xw * pY + yw * qy
		z = xw * pZ + yw * qz
		xd = xdw * pX + ydw * qx
		yd = xdw * pY + ydw * qy
		zd = xdw * pZ + ydw * qz
		
		return (Vector(x, y, z), Vector(xd, yd, zd))


bodies = [
	Body(name="Sun", r=261600000, rot=432000),
	PlanetaryBody(name="Moho", r=250000, a=5263138304, i=7, o=70, w=15, rot=1210000),
	PlanetaryBody(name="Eve", r=700000, a=9832684544, i=2.1, o=15, w=0, rot=80500),
	PlanetaryBody(name="Gilly", r=13000, a=31500000, i=12, o=80, w=10, rot=28255, is_potato=True),
	PlanetaryBody(name="Kerbin", r=600000, a=13599840256, i=0, o=0, w=0, rot=21599.912014540),
	PlanetaryBody(name="Mun", r=200000, a=12000000, i=5.145, o=0, w=0),
	PlanetaryBody(name="Minmus", r=60000, a=47000000, i=0, o=78, w=38, rot=40400),
	PlanetaryBody(name="Duna", r=320000, a=20726155264, i=0.06, o=135.5, w=0, rot=65517.859375000),
	PlanetaryBody(name="Ike", r=130000, a=3200000, i=0.2, o=0, w=0),
	PlanetaryBody(name="Dres", r=138000, a=40839348203, i=5, o=280, w=90, rot=34800),
	PlanetaryBody(name="Jool", r=6000000, a=68773560320, i=1.304, o=52, w=0, rot=36000),
	PlanetaryBody(name="Laythe", r=500000, a=27184000, i=0, o=0, w=0),
	PlanetaryBody(name="Vall", r=300000, a=43152000, i=0, o=0, w=0),
	PlanetaryBody(name="Tylo", r=600000, a=68500000, i=0.025, o=0, w=0),
	PlanetaryBody(name="Bop", r=65000, a=128500000, i=15, o=10, w=25, is_potato=True),
	PlanetaryBody(name="Pol", r=44000, a=179890000, i=4.25, o=2, w=15, is_potato=True),
	PlanetaryBody(name="Eeloo", r=210000, a=90118820000, i=6.15, o=50, w=260, rot=19460),
]

opm_bodies = [
	PlanetaryBody(name="Sarnus", r=5300000, a=125798522368, i=2.02, o=184, w=0, rot=28500, has_rings=True),
	PlanetaryBody(name="Hale", r=6000, a=10488231, i=1, o=55, w=0, is_potato=True, no_rotate=True),
	PlanetaryBody(name="Ovok", r=26000, a=12169413, i=1.5, o=55, w=0, no_rotate=True),
	PlanetaryBody(name="Eeloo", r=210000, a=19105978, i=2.3, o=55, w=260, no_rotate=True),
	PlanetaryBody(name="Slate", r=540000, a=42592946, i=2.3, o=55, w=0),
	PlanetaryBody(name="Tekto", r=280000, a=97355304, i=9.4, o=55, w=0),	
	PlanetaryBody(name="Urlum", r=2177000, a=254317012787, i=0.64, o=61, w=0, rot=41000, has_rings=True),
	PlanetaryBody(name="Polta", r=220000, a=11727895, i=2.45, o=40, w=60),
	PlanetaryBody(name="Priax", r=74000, a=11727895, i=2.45, o=40, w=0, is_potato=True),
	PlanetaryBody(name="Wal", r=370000, a=67553668, i=1.9, o=40, w=0),
	PlanetaryBody(name="Tal", r=22000, a=3109163, i=1.9, o=40, w=0, is_potato=True),
	PlanetaryBody(name="Neidon", r=2145000, a=409355191706, i=1.27, o=259, w=0, rot=40250),
	PlanetaryBody(name="Thatmo", r=286000, a=32300895, i=161.1, o=66, w=0),
	PlanetaryBody(name="Nissee", r=30000, a=487743514, i=29.56, o=66, w=0),
	PlanetaryBody(name="Plock", r=189000, a=535833706086, i=6.15, o=260, w=50, rot=106300),
]