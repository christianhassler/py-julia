import sys
import cmath

def Q(z,c):
	return z * z + c

# r < |z|
def norm_cmp(r, z):
	z_norm = cmath.sqrt((z.real * z.real) + (z.imag * z.imag))
	if (r < z_norm.real):
		return 1
	else:
		return 0

# Is the orbit of z under f bounded (i.e. '< infinity') after 'depth' iterations?
def is_bounded(f,c,z,depth,infinity):
	i = 0
	while(i < depth):
		if (norm_cmp(infinity,z)):
			return 0
		z = f(z,c)
		i = i + 1
	return 1


def filled_julia(f,c,z0,width,height,r_res,i_res,depth,infinity):
	r_unit = complex(width / r_res)
	i_unit = complex(0 + (height / i_res)*1j)
	print r_unit
	print i_unit
	z = z0
	while (z.imag < z0.imag + height):
		while (z.real < z0.real + width):
			if (is_bounded(f,c,z,depth,infinity)):
				print "%f + %fi is in the filled julia set" % (z.real, z.imag)
			z = z + r_unit
		z = z0.real + z.imag*1j
		z = z + i_unit

filled_julia(Q,-0.5,-2.0 - 2.0j,4.0,4.0,100.0,100.0,1000,100)
