import sys
import cmath
import png
from struct import pack
from array import array 

def F(z,c):
	z2 = z * z;
	return (z2 * z2) - z2 + c

def progress_bar(progress):
	sys.stderr.write('\r[{0}{1}] {2}%'.format('#'*int(progress),'-'*(100-int(progress)), progress)),

# square bound test b/c the norm test takes too long
def lazy_cmp(bounds, z):
	if (bounds[0] > z.real or bounds[1] < z.real):
		return 1
	elif (bounds[2] > z.imag or bounds[3] < z.imag):
		return 1
	else:
		return 0

def gen_rgb_gradient(color1,color2,saturation_color,e):
	# convert rgb values from bytes to floats
	r1 = float(color1[0]) / 255.0
	g1 = float(color1[1]) / 255.0
	b1 = float(color1[2]) / 255.0

	r2 = float(color2[0]) / 255.0
	g2 = float(color2[1]) / 255.0
	b2 = float(color2[2]) / 255.0

	# re-normalizing factor
	norm_factor = 255.0 / (255.0 ** e)

	gradient = []
	for i in range(0,255):
		t = int((i ** e) * norm_factor)
		red   = int((255 - t)*r1 + t*r2) & 0xff # red
		green = int((255 - t)*g1 + t*g2) & 0xff # green
		blue  = int((255 - t)*b1 + t*b2) & 0xff # blue
		gradient.append([red, green, blue]) 
	gradient.append(saturation_color)
	return gradient

def get_rgb(f):
	saturation_point = 0.1
	if (f == 1):
		return [0x00,0x00,0x00]
	elif (f > saturation_point):
		f = saturation_point
	red = int((f/saturation_point)*255)
	print red
	return [red,0x03,0xf0]

class julia:
	_c = 1.0 # control parameter
	_bounds = [-2,2,-2,2] # if an orbit goes outside of this rectange, it is considered to be divergent
	_res = [500,500] # resolution
	_depth = 80 # number of iterations of F

	# generate the filled julia set as a png file
	def filled_julia(self,center,zoom,filename):
		# prepare the file
		f = open(filename,'wb')
		w = png.Writer(self._res[0],self._res[1])
		buf = [] # file buffer b/c pypng can't do byte streams (at least, I can't figure it out)

		# generate a color gradient
		gradient = gen_rgb_gradient([0x00,0x00,0xff],[0xff,0xff,0xff], [0x00,0x00,0x00], 0.25)
		total_progress = float(self._res[0] * self._res[1])
		depth_conv = 255.0 / float(self._depth)

		# mathematical constants
		bounds = self._bounds
		view = [(center[0] + bounds[0]) / zoom, (center[0] + bounds[1]) / zoom, (center[1] + bounds[2]) / zoom, (center[1] + bounds[3]) / zoom]
		r_unit = complex((view[1] - view[0]) / self._res[0]) # real unit
		i_unit = complex(0 + ((view[3] - view[2])/ self._res[1])*1j) # imaginary unit

		# iterated variables
		z0 = complex(view[0] + (view[2])*1j)
		progress = 0
		for k in range(0,self._res[1]): # loop over imaginary numbers
			row = array('B')
			for j in range(0,self._res[0]): # loop over real numbers
				z = z0
				i = 0
				while (i <  self._depth):
					if (lazy_cmp(self._bounds,z)):
						break
					z = F(z,self._c) # transfer function
					i = i + 1
				#print('{0},{1},{2}'.format(z0.real,z0.imag,float(i)/self._depth))
				row.extend(gradient[int(i*depth_conv)])
				z0 = z0 + r_unit

				# progress bar (comment out for speed)
				progress = progress + 1
				progress_bar((progress/total_progress)*100)
			z0 = view[0] + z0.imag*1j
			z0 = z0 + i_unit
			buf.append(row)
		w.write(f,buf)
		f.close()

j = julia()
j.filled_julia([0.0,0.0],1.0,'filled_julia.png')
