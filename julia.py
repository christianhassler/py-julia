import sys
import cmath

def progress_bar(progress):
	sys.stderr.write('\r[{0}{1}] {2}%'.format('#'*int(progress),'-'*(100-int(progress)), progress)),

def Q(z,c):
	return z * z + c

# r < |z|
def norm_cmp(r, z):
	z_norm = cmath.sqrt((z.real * z.real) + (z.imag * z.imag))
	if (r < z_norm.real):
		return 1
	else:
		return 0

# square bound test b/c the norm test takes too long
def lazy_cmp(bounds, z):
	if (bounds[0] > z.real or bounds[1] < z.real):
		return 1
	elif (bounds[2] > z.imag or bounds[3] < z.imag):
		return 1
	else:
		return 0

class julia:
	_f = Q
	_c = -0.5
	_bounds = [-1.5,1.5,-1,1]
	_res = [1000.0,1000.0]
	_depth = 100
	
	# Is the orbit of z under f bounded (i.e. '< infinity') after 'depth' iterations?
	def is_bounded(self,z):
		i = 0
		while(i < self._depth):
			if (lazy_cmp(self._bounds,z)):
				return 0
			z = Q(z,self._c)
			i = i + 1
		return 1

	def filled_julia(self,center,zoom):
		bounds = self._bounds
		view = [center[0] + (zoom * bounds[0]), center[0] + (zoom * bounds[1]), center[1] + (zoom * bounds[2]), center[1] + (zoom * bounds[3])]
		r_unit = complex((view[1] - view[0]) / self._res[0])
		i_unit = complex(0 + ((view[3] - view[2])/ self._res[1])*1j)
		z0 = complex(view[0] + (view[2])*1j)
		#print r_unit
		#print i_unit
		progress = 0
		total_progress = self._res[0] * self._res[1]
		while (z0.imag < view[3]):
			while (z0.real < view[1]):
				if (self.is_bounded(z0)):
                                    print('{0},{1}'.format(z0.real,z0.imag))
				z0 = z0 + r_unit
				progress = progress + 1;
				progress_bar((progress/total_progress)*100)
			z0 = view[0] + z0.imag*1j
			z0 = z0 + i_unit

j = julia()
j.filled_julia([0.0,0.8],2.0)
