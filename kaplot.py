from copy import deepcopy
# required to make pydocs work
from functools import wraps
import matplotlib
# backends @ http://matplotlib.org/faq/usage_faq.html
matplotlib.use('macosx')
import matplotlib.pyplot as plt 
import pickle

__author__		= 'Kamil'
__version__		= '0.3'
__name__		= 'kaplot'
__file__		= 'kaplot.py'

"""
CHANGELOG
=========
** 03/04/2014 , v0.3 **
	- 	made changes to update_default_kwargs so that when value='Auto' those values are not included
		and the plot resorts to default MPL behavior
	-	fixed various bugs, including tick formatting bugs
	-	changed dictionaries to use 'Auto' so that rcParams are used by default
	- 	updated saveObj()


** 03/03/2014 , v0.2 **
	- 	documentation added to functions
	- 	check_name now returns all lowercase kwargs
	- 	added saveObj() ; which uses pickle. to be tested.
	- 	ls/lw now standard in all dictionaries
	- 	adjusted tight layout values for subplots

** 03/02/2014 , v0.1 **
	- 	initial release

TODO 
====
	- 	add spline
	- 	need to add loadObj()
	- 	fix latex output to use the same font
 	- 	add_rectangle
 	- 	add_plotdata
 	- 	update set_unique_colors to use cmap
 			+ 	user specified unique_colors
 	- 	fix the color/marker/fill selector
 	-	 fix random +1 in the ADD PLOTDATA portion of kaplot
 	- 	plot_type - only line is supported now, should expand to : line , bar , rectangle
"""

def check_name(fn):
	"""
	decorator function for kaplot class. checks if the $name$ kwarg is 
	valid and inserts $ind$ into the kwarg list. additionally, changes all
	kwargs to be lower case.
	** args **
	fn 		- function
	"""
	@wraps(fn)
	def wrapper(self,*args,**kwargs):
		if 'name' not in kwargs:
			kwargs['name'] = 'main'
		if kwargs['name'].lower() in self._LAYER_NAMES:
			oind = self._LAYER_NAMES.index(kwargs['name'].lower())
			kwargs['ind'] = oind
			# rebuild kwargs
			new_kwargs = {}
			for key,val in kwargs.iteritems():
				new_kwargs[key.lower()] = val
			return fn(self,*args,**new_kwargs)
		raise AttributeError('No layer/axes named %s' % kwargs['name'])
	return wrapper

class kaplot(object):
	"""
	multi layer plotting class

	organization ; 
	a PLOT contains any number of LAYERS,
	each LAYER has a NAME associated with it,
	the NAME is how a LAYER can be identified,
	each LAYER can have any number of features added to it.
	"""

	# used to make latex output same font
	matplotlib.rcParams['font.family'] 		= 'sans-serif'
	matplotlib.rcParams['font.sans-serif']	= 'Arial, Helvetica, sans-serif'
	matplotlib.rcParams['mathtext.default']	= 'regular'

	LAYER_SETTINGS		=	{ 	'twin'			:	None 	, \
								'twin_ref'		:	None}
	# settings for the entire plot
	SAVEFIG_SETTINGS 	= 	{	'dpi'			:	100		, \
							  	'transparent'	:	False	, \
							  	'width'			:	8	, \
							  	'height'		:	6}
	# predefined settings
	_LOCATION_TIGHT		= 	{	'upper left'	:	[0.18,0.595,0.25,0.25] , \
								'upper right'	:	[0.70,0.595,0.25,0.25] , \
								'lower right'	:	[0.70,0.195,0.25,0.25] , \
								'lower left'	:	[0.18,0.195,0.25,0.25]}

	_LOCATION			= 	{	'upper left'	:	[0.22,0.595,0.25,0.25] , \
								'upper right'	:	[0.63,0.595,0.25,0.25] , \
								'lower right'	:	[0.63,0.180,0.25,0.25] , \
								'lower left'	:	[0.22,0.180,0.25,0.25]}

	_FONT_TITLE			= 	{	'family'	: 	'Auto' 		, \
								'style'		:	'Auto'		, \
								'weight'	:	'Auto'		, \
								'size'		:	'Auto'		, \
								'color'		:	'Auto'		, \
								'alpha'		:	'Auto'		, \
								'va'		:	'Auto'		, \
								'ha'		:	'Auto'		, \
								'rotation'	:	'Auto'}

	_FONT_XLABEL		= 	{	'family'	: 	'Auto' 		, \
								'style'		:	'Auto'		, \
								'weight'	:	'Auto'		, \
								'size'		:	'Auto'		, \
								'color'		:	'Auto'		, \
								'alpha'		:	'Auto'		, \
								'va'		:	'Auto'		, \
								'ha'		:	'Auto'		, \
								'rotation'	:	'Auto'}

	_FONT_YLABEL		= 	{	'family'	: 	'Auto' 		, \
								'style'		:	'Auto'		, \
								'weight'	:	'Auto'		, \
								'size'		:	'Auto'		, \
								'color'		:	'Auto'		, \
								'alpha'		:	'Auto'		, \
								'va'		:	'Auto'		, \
								'ha'		:	'Auto'		, \
								'rotation'	:	'Auto'}

	_GRID_SETTINGS		= 	{	'alpha'		:	'Auto'		, \
								'color'		:	'Auto'		, \
								'ls'		:	'Auto'		, \
								'lw'		:	'Auto'}

	_FONT_XTICK 		= 	{	'family'	: 	'Auto' 		, \
								'style'		:	'Auto'		, \
								'weight'	:	'Auto'		, \
								'size'		:	'Auto'		, \
								'color'		:	'Auto'		, \
								'alpha'		:	'Auto'		, \
								'va'		:	'Auto'		, \
								'ha'		:	'Auto'		, \
								'rotation'	:	'Auto'}

	_FONT_YTICK 		= 	{	'family'	: 	'Auto' 		, \
								'style'		:	'Auto'		, \
								'weight'	:	'Auto'		, \
								'size'		:	'Auto'		, \
								'color'		:	'Auto'		, \
								'alpha'		:	'Auto'		, \
								'va'		:	'Auto'		, \
								'ha'		:	'Auto'		, \
								'rotation'	:	'Auto'}

	_FRAME_LIST			= 	{	'top'		:	'Auto' 		, \
								'bottom'	:	'Auto'		, \
								'right'		:	'Auto'		, \
								'left'		:	'Auto'}

	_XTICK_PARAMS		= 	{	'direction'		:	'Auto'	, \
								'length'		:	'Auto'	, \
								'width'			:	'Auto'	, \
								'color'			:	'Auto'	, \
								'pad'			:	'Auto'	, \
								'labelsize'		:	'Auto'	, \
								'labelcolor'	:	'Auto'	, \
								'labeltop'		:	'Auto' 	, \
								'labelbottom'	:	'Auto' 	, \
								'top'			:	'Auto'	, \
								'bottom' 		:	'Auto'}

	_YTICK_PARAMS		= 	{	'direction'		:	'Auto'	, \
								'length'		:	'Auto'	, \
								'width'			:	'Auto'	, \
								'color'			:	'Auto'	, \
								'pad'			:	'Auto'	, \
								'labelsize'		:	'Auto'	, \
								'labelcolor'	:	'Auto'	, \
								'labelleft'		:	'Auto' 	, \
								'labelright'	:	'Auto' 	, \
								'left'			:	'Auto' 	, \
								'right'			:	'Auto'}

	_XTICK_FORMAT		= 	{	'style'		:	'plain'		, \
								'sci_min'	:	0			, \
								'sci_max'	:	0}
	_YTICK_FORMAT		= 	{	'style'		:	'plain'		, \
								'sci_min'	:	0			, \
								'sci_max'	:	0}

	_AX_LINE 			= 	{	'min'		:	'Auto'		, \
								'max'		:	'Auto'		, \
								'alpha'		:	'Auto'		, \
								'ls' 		: 	'Auto'		, \
								'lw'		:	'Auto'		, \
								'color'		:	'Auto'}

	_TEXT_FONT 			= 	{ 	'family'	: 	'Auto' 		, \
								'style'		:	'Auto'		, \
								'weight'	:	'Auto'		, \
								'size'		:	'Auto'		, \
								'color'		:	'Auto'		, \
								'alpha'		:	'Auto'		, \
								'va'		:	'Auto'		, \
								'ha'		:	'Auto'		, \
								'rotation'	:	'Auto'}

	_LINE_DEFAULTS		= 	{	'x'			:	None			, \
								'y'			:	None			, \
								'xerr'		:	None			, \
								'yerr'		:	None			, \
								'label'		: 	'_nolegend_'	, \
								'increment'	:	True 			, \
								'color'		:	'Auto'			, \
								'lw'		:	'Auto'			, \
								'ls'		:	'Auto'			, \
								'marker'	:	'Auto'			, \
								'mec' 		: 	'Auto'			, \
								'ms'		:	'Auto'			, \
								'markevery'	:	'Auto'			, \
								'mfc' 		: 	'Auto'			, \
								'ecolor'	:	'Auto'			, \
								'elinewidth':	'Auto'			, \
								'capsize'	:	'Auto'}

	_LEGEND_FONTPROPS	= {		'family'	:	'sans-serif'	, \
								'style'		:	'normal'		, \
								'weight'	:	'normal'		, \
								'size'		:	'medium'}

	_LEGEND_DEFAULTS	= {		'bool'			:	False			, \
								'loc'			:	'upper right'	, \
								'numpoints'		:	1 				, \
								'markerscale'	:	1 		 		, \
								'frameon'		:	True 			, \
								'fancybox'		:	False 			, \
								'shadow'		:	False 			, \
								'framealpha'	:	1.0 			, \
								'ncol'			:	1 				, \
								'title'			:	None			, \
								'fontsize'		:	'medium'		, \
								'borderpad'		:	0.1 			, \
								'labelspacing'	: 0.1 				, \
								'handletextpad'	: 0.25				, \
								'columnspacing'	: 0.1}

	_COLOR_LIST			= ['black' , 'red' , 'blue' , 'fuchsia' , 'orange' , 'lime' , 'aqua' , 'maroon' , '0.40' , '0.85']
	_MARKER_LIST 		= [None , 's' , 'o' , '^' , 'D']
	_MARKER_FILL_LIST	= [None , 'white']

	def __init__(self):
		# list of layers and associated properties
		self._SAVED				= None
		self._LAYER_NAMES		= []
		self._LAYER_OBJECTS		= []
		self._LAYER_SETTINGS	= []
		self._LAYER_PLT_OBJECT	= []
		self.PLOT_SETTINGS 		= {	'tight_layout'	:	False 	, \
									'xkcd'			:	False	, \
									'x_label_sep_l'	:	' , '	, \
									'x_label_sep_r'	:	''		, \
									'y_label_sep_l'	:	' , '	, \
									'y_label_sep_r'	:	''}

		self._LAYER_NAMES.append('main')
		self._LAYER_OBJECTS.append(deepcopy(kaxes()))
		self._LAYER_SETTINGS.append(deepcopy(self.LAYER_SETTINGS))
		return

	def set_tight(self,tl_bool):
		"""
		updates the tight_layout boolean

		** args **
		tl_bool 	- True/False for tight layout
		"""
		if type(tl_bool) is type(True):
			self.PLOT_SETTINGS['tight_layout'] = tl_bool
		return

	def set_xkcd(self,xk_bool):
		"""
		updates the xkcd mode boolean

		** args **
		xk_bool 	- True/False for xkcd mode
		"""
		if type(xk_bool) is type(True):
			self.PLOT_SETTINGS['xkcd'] = xk_bool
		return

	def add_layer(self,name,location=None,twin=None,twin_ref='main'):
		"""
		adds a new layer to the plot with name $name$

		** args **
		name 		- layer name
		location 	- either None, 'upper left/right' , 'lower left/right' or a 4 coordinate list
		twin 		- either 'x' or 'y' , this will make the new layer share axes 'x' or 'y' with twin_ref
		twin_ref 	- layer name with which this layer will share an axes with
		"""
		if name.lower() not in self._LAYER_NAMES:
			# add layer
			self._LAYER_NAMES.append(name.lower())
			# add layer object and location settings
			k = kaxes()
			k.set_location(location)
			self._LAYER_OBJECTS.append(k)
			# add layer settings
			tmp = deepcopy(self.LAYER_SETTINGS)
			if twin is not None and twin.lower() in ['x', 'y']:
				tmp['twin']		= twin.lower()
				tmp['twin_ref']	= twin_ref.lower()
			self._LAYER_SETTINGS.append(tmp)
		else:
			print 'KAPLOT: add_layer error. layer exists.'
		return

	@check_name
	def set_plot_type(self,ptype,**kwargs):
		"""
		sets the plot type of the layer

		** args **
		ptype 	- plot type , either line , bar , rect 

		** kwargs **
		name 	- layer name if not main
		"""
		k = self._LAYER_OBJECTS[kwargs['ind']]
		if ptype.lower() in ['line', 'bar']:
			k.set_plot_type(ptype)
		else:
			print "KAPLOT Error. Not a valid plot"
		return

	@check_name
	def set_legend(self,lbool,**kwargs):
		"""
		sets a legend for the layer

		** args **
		lbool 			- True/False for displaying a legend

		** kwargs **
		name 			- layer name, if not main 

		loc 			- location 'upper', 'lower', 'left' , 'right', 'center'
		numpoints		- number of markers to show
		markerscale		- marker scaling
		frameon			- True/False , show frame
		fancybox		- True/False , use a curved frame
		shadow			- True/False , draw a shadow behind the frame
		framealpha		- alpha level for the frame
		ncol 			- number of legend columns
		title 			- legend title 
		fontsize 		- font size 
		borderpad		- padding inside the legend 
		labelspacing	- spacing between labels
		handletextpad	- spacing between legend handle and text 
		columnspacing	- spacing between columns

		** font prop kwargs **
		family			- font family , 'sans-serif' 'serif' 'monospace' 'fantasy'
		style 			- 'normal' or 'oblique'
		weight			- 'normal' 'regular' 'semibold' 'bold' 'black'
		size 			- font size , #points 'xx-small' 'medium' 'xx-large'
		"""
		k 		= self._LAYER_OBJECTS[kwargs['ind']]
		ldict 	= update_default_kwargs(self._LEGEND_DEFAULTS,kwargs)
		fdict 	= update_default_kwargs(self._LEGEND_FONTPROPS,kwargs)
		ldict['bool'] = lbool
		k.set_legend(fdict=fdict,**ldict)
		return

	@check_name
	def set_title(self,title,**kwargs):
		"""
		adds a title to the layer

		** args **
		title 		- layer title

		** kwargs **
		name 		- layer name

		family		- font family , 'sans-serif' 'serif' 'monospace' 'fantasy'
		style 		- 'normal' or 'oblique'
		size 		- font size , #points 'xx-small' 'medium' 'xx-large'
		color 		- font color
		alpha 		- alpha level
		va 			- vertical alignment , 'center' 'top' 'bottom' 'baseline'
		ha 			- horizontal alignment , 'center' , 'right' , 'left'
		rotation	- rotate text by some degree
		"""
		fdict 	= update_default_kwargs(self._FONT_TITLE,kwargs)
		k 		= self._LAYER_OBJECTS[kwargs['ind']]
		k.set_title(title,**fdict)
		return

	@check_name
	def set_grid(self,gbool,**kwargs):
		"""
		adds grid lines to the layer

		** args **
		gbool 	- True/False for turning grid bool

		** kwargs ** 
		name 	- layer name
		alpha	- alpha level 
		color 	- line color
		ls 		- line style
		lw 		- line width
		"""
		k 		= self._LAYER_OBJECTS[kwargs['ind']]
		gdict	= update_default_kwargs(self._GRID_SETTINGS,kwargs)
		k.set_grid(gbool,**gdict)
		return

	@check_name
	def set_axes_type(self,ptype='linear',**kwargs):
		"""
		sets the axes type for the layer

		** args **
		ptype 	- axes type , 'linear' 'log-log' 'semilog-x' 'semilog-y'

		** kwargs **
		name 	- layer name
		"""
		if ptype.lower() in ['linear','log-log','semilog-x','semilog-y']:
			k 	= self._LAYER_OBJECTS[kwargs['ind']]
			k.set_axes_type(ptype.lower())
		else:
			print 'KAPLOT: set_axes_type error. ptype must be either linear,log-log,semilog-x,semilog-y.'
		return

	@check_name
	def set_base(self,basex=1.0,basey=1.0,**kwargs):
		"""
		sets the base for the axis, useful for semilog and log-log axis

		** args **
		basex 	- x base
		basey 	- y base 

		** kwargs **
		name 	- layer name
		"""
		try:
			basex = float(basex)
			basey = float(basey)
			k = self._LAYER_OBJECTS[kwargs['ind']]
			k.set_base(basex,basey)
		except:
			print 'KAPLOT: set_base error. basex or basey must be a valid float.'

	@check_name
	def set_xlabel(self,lab='',unit=None,**kwargs):
		"""
		adds a xlabel to the layer

		** args **
		lab 		- long label 
		unit 		- label unit

		** kwargs **
		name 		- layer name

		family		- font family , 'sans-serif' 'serif' 'monospace' 'fantasy'
		style 		- 'normal' or 'oblique'
		weight		- 'normal' 'regular' 'semibold' 'bold' 'black'
		size 		- font size , #points 'xx-small' 'medium' 'xx-large'
		color 		- font color
		alpha 		- alpha level
		va 			- vertical alignment , 'center' 'top' 'bottom' 'baseline'
		ha 			- horizontal alignment , 'center' , 'right' , 'left'
		rotation	- rotate text by some degree
		"""
		fdict 	= update_default_kwargs(self._FONT_XLABEL,kwargs)
		if unit is not None:
			lab 	= '%s%s%s%s' % (lab,self.PLOT_SETTINGS['x_label_sep_l'],unit,self.PLOT_SETTINGS['x_label_sep_r'])
		else:
			lab 	= '%s' % lab
		k 		= self._LAYER_OBJECTS[kwargs['ind']]
		k.set_xlabel(lab,**fdict)
		return

	@check_name
	def set_ylabel(self,lab='',unit=None,**kwargs):
		"""
		adds a ylabel to the layer

		** args **
		lab 		- long label 
		unit 		- label unit

		** kwargs **
		name 		- layer name

		family		- font family , 'sans-serif' 'serif' 'monospace' 'fantasy'
		style 		- 'normal' or 'oblique'
		weight		- 'normal' 'regular' 'semibold' 'bold' 'black'
		size 		- font size , #points 'xx-small' 'medium' 'xx-large'
		color 		- font color
		alpha 		- alpha level
		va 			- vertical alignment , 'center' 'top' 'bottom' 'baseline'
		ha 			- horizontal alignment , 'center' , 'right' , 'left'
		rotation	- rotate text by some degree
		"""
		fdict 	= update_default_kwargs(self._FONT_YLABEL,kwargs)
		if unit is not None:
			lab 	= '%s%s%s%s' % (lab,self.PLOT_SETTINGS['y_label_sep_l'],unit,self.PLOT_SETTINGS['y_label_sep_r'])
		else:
			lab 	= '%s' % lab
		k 		= self._LAYER_OBJECTS[kwargs['ind']]
		k.set_ylabel(lab,**fdict)
		return

	@check_name
	def set_xticks(self,start,stop,incr,log=False,**kwargs):
		"""
		sets the values of the ticks , can be logarithmic or custom
		if $myList$ is specified it will overwrite all other values

		** args **
		start 		- start value
		end 		- finish value
		icnr		- increment
		log 		- multiply instead of add boolean

		** kwargs **
		name 		- layer name
		mylist		- custom list

		family		- font family , 'sans-serif' 'serif' 'monospace' 'fantasy'
		style 		- 'normal' or 'oblique'
		size 		- font size , #points 'xx-small' 'medium' 'xx-large'
		weight		- 'normal' 'regular' 'semibold' 'bold' 'black'
		color 		- font color
		alpha 		- alpha level
		va 			- vertical alignment , 'center' 'top' 'bottom' 'baseline'
		ha 			- horizontal alignment , 'center' , 'right' , 'left'
		rotation	- rotate text by some degree
		"""
		fdict 	= update_default_kwargs(self._FONT_XTICK,kwargs)
		k 		= self._LAYER_OBJECTS[kwargs['ind']]
		if 'mylist' in kwargs:
			tick_list = kwargs['mylist']
		else:
			tick_list = srange(start,stop,incr,log)
		k.set_xticks(tick_list,**fdict)
		return

	@check_name
	def set_yticks(self,start,stop,incr,log=False,**kwargs):
		"""
		sets the values of the ticks , can be logarithmic or custom
		if $myList$ is specified it will overwrite all other values

		** args **
		start 		- start value
		end 		- finish value
		icnr		- increment
		log 		- multiply instead of add boolean

		** kwargs **
		name 		- layer name
		mylist		- custom list

		family		- font family , 'sans-serif' 'serif' 'monospace' 'fantasy'
		style 		- 'normal' or 'oblique'
		size 		- font size , #points 'xx-small' 'medium' 'xx-large'
		weight		- 'normal' 'regular' 'semibold' 'bold' 'black'
		color 		- font color
		alpha 		- alpha level
		va 			- vertical alignment , 'center' 'top' 'bottom' 'baseline'
		ha 			- horizontal alignment , 'center' , 'right' , 'left'
		rotation	- rotate text by some degree
		"""
		fdict 	= update_default_kwargs(self._FONT_YTICK,kwargs)
		k 		= self._LAYER_OBJECTS[kwargs['ind']]
		if 'mylist' in kwargs:
			tick_list = kwargs['mylist']
		else:
			tick_list = srange(start,stop,incr,log)
		k.set_yticks(tick_list,**fdict)
		return

	@check_name
	def set_xlim(self,**kwargs):
		"""
		set the upper and lower values of the plot

		** kwargs **
		name 	- layer names
		min 	- lower value
		max 	- upper value
		"""
		xmin = None
		xmax = None
		if 'min' in kwargs:
			xmin = kwargs['min']
		if 'max' in kwargs:
			xmax = kwargs['max']
		k 	= self._LAYER_OBJECTS[kwargs['ind']]
		k.set_xlim(xmin,xmax)
		return

	@check_name
	def set_ylim(self,**kwargs):
		"""
		set the upper and lower values of the plot

		** kwargs **
		name 	- layer names
		min 	- lower value
		max 	- upper value
		"""
		ymin = None
		ymax = None
		if 'min' in kwargs:
			ymin = kwargs['min']
		if 'max' in kwargs:
			ymax = kwargs['max']
		k 	= self._LAYER_OBJECTS[kwargs['ind']]
		k.set_ylim(ymin,ymax)
		return

	@check_name
	def set_tick_params(self,axis='both',**kwargs):
		"""
		sets the properties of ticks, tick labels and axes labels 

		** args **
		axis 		- which axis to modify, 'both' 'x' 'y'

		** kwargs **
		name 		- layer name

		direction 	- in / out
		length		- length of tick in points
		width 		- width of tick in points
		color 		- color of tick
		pad 		- padding between tick and label
		labelsize	- tick label font size
		labelcolor 	- tick label font color

		* valid in both / x-axis *
		labeltop	- True/False 
		labelbottom	- True/False
		top 		- True/False , draw ticks
		bottom		- True/False , draw ticks

		* valid in both / y-axis *
		labelleft	- True/False
		labelright	- True/False
		left 		- True/False , draw ticks
		right		- True/False , draw ticks
		"""
		k 	= self._LAYER_OBJECTS[kwargs['ind']]
		# gets both lists, regardless
		x_params= update_default_kwargs(self._XTICK_PARAMS,kwargs)
		y_params= update_default_kwargs(self._YTICK_PARAMS,kwargs)
		if axis is 'both':
			k.set_x_tick_params(**y_params)
			k.set_y_tick_params(**y_params)
		elif axis is 'x':
			k.set_x_tick_params(**x_params)
		elif axis is 'y':
			k.set_y_tick_params(**y_params)			
		return

	@check_name
	def set_tick_format(self,axis='both',**kwargs):
		"""
		sets the tick label formatting, i.e. allows for scientific notation

		** args **
		axis 		- which axis to modify , 'both' 'x' 'y'

		** kwargs **
		name 		- layer name
		style 		- 'plain' or 'sci'
		sci_min		- min for sci notation
		sci_max		- max for sci notation
		"""
		k 	= self._LAYER_OBJECTS[kwargs['ind']]
		x_format = update_default_kwargs(self._XTICK_FORMAT,kwargs)
		y_format = update_default_kwargs(self._YTICK_FORMAT,kwargs)
		if axis is 'both':
			k.set_x_tick_format(**x_format)
			k.set_y_tick_format(**y_format)
		elif axis is 'x':
			k.set_x_tick_format(**x_format)
		elif axis is 'y':
			k.set_y_tick_format(**y_format)
		return

	@check_name
	def set_frames(self,**kwargs):
		"""
		removes frames from plots , this function should
		be used in combination with set_tick_params() to 
		remove ticks

		** kwargs **
		name 	- layer name
		top 	- True/False
		bottom 	- True/False
		left 	- True/False
		right 	- True/False
		"""
		k 		= self._LAYER_OBJECTS[kwargs['ind']]
		k.set_frames(**kwargs)
		return

	@check_name
	def set_unique_colors(self,ubool,**kwargs):
		"""
		changes the program to use unique colors for the layer

		** kwargs **
		name 	- layer name
		"""
		k = self._LAYER_OBJECTS[kwargs['ind']]
		k.set_unique_colors(ubool)
		return

	@check_name
	def add_axhline(self,location,**kwargs):
		"""
		adds a horizontal line to the layer at location y = $location$

		** args **
		location 	- the y-intercept of the horizontal line

		** kwargs **
		name 		- layer name
		min 		- minimum x value
		max 		- maximum x value 
		alpha 		- alpha level 
		ls			- line style
		lw			- line width 
		color 		- line color
		"""
		k 	= self._LAYER_OBJECTS[kwargs['ind']]
		ax = update_default_kwargs(self._AX_LINE,kwargs)
		ax['y']			= location
		if 'min' in kwargs:
			ax['xmin']		= ax.pop('min')
		if 'max' in kwargs:
			ax['xmax']		= ax.pop('max')	
		# remove all 'auto' values
		k.add_axhline(**ax)
		return

	@check_name
	def add_axvline(self,location,**kwargs):
		"""
		adds a vertical line to the layer at location x = $location$

		** args **
		location 	- the x-intercept of the vertical line

		** kwargs **
		name 		- layer name
		min 		- minimum y value
		max 		- maximum y value 
		alpha 		- alpha level 
		ls			- line style
		lw			- line width 
		color 		- line color
		"""
		k 	= self._LAYER_OBJECTS[kwargs['ind']]
		ax = update_default_kwargs(self._AX_LINE,kwargs)
		ax['x']			= location
		if 'min' in kwargs:
			ax['ymin']		= ax.pop('min')
		if 'max' in kwargs:
			ax['ymax']		= ax.pop('max')	
		# remove all 'auto' values
		k.add_axvline(**ax)
		return

	@check_name
	def add_text(self,txt,x,y,**kwargs):
		"""
		adds text to the layer at the point $x$,$y$
		
		** args **
		txt 		- text to be added
		x 			- x-coordinate in data coordinates
		y 			- y-coordinate in data coordinates

		** kwargs **
		name 		- layer name
		family		- font family , 'sans-serif' 'serif' 'monospace' 'fantasy'
		style 		- 'normal' or 'oblique'
		size 		- font size , #points 'xx-small' 'medium' 'xx-large'
		color 		- font color
		alpha 		- alpha level
		va 			- vertical alignment , 'center' 'top' 'bottom' 'baseline'
		ha 			- horizontal alignment , 'center' , 'right' , 'left'
		rotation	- rotate text by some degree
		"""
		k 		= self._LAYER_OBJECTS[kwargs['ind']]
		tdict 	= update_default_kwargs(self._TEXT_FONT,kwargs)
		tdict['txt'] = txt
		tdict['x']	 = x
		tdict['y']	 = y
		k.add_text(**tdict)
		return

	@check_name
	def add_plotdata(self,x,y,**kwargs):
		"""
		adds plot data to the layer

		** args **
		x 			- x data array/list
		y 			- y data array/list
	
		** kwargs **
		name 		- layer name
		xerr		- x-error data array/list
		yerr		- y-error data array/list
		label 		- data label to be used in legend
		increment 	- True/False , increment the auto color/marker/fill

		** line plot kwargs **
		color 		- line color
		ls 			- line style 
		lw 			- line width
		m 			- marker 
		mec 		- marker edge color
		ms 			- marker size 
		markevery 	- marker every data points 
		mfc 		- marker face color
		ecolor 		- error line color
		elinewidth	- error line width 
		capsize		- error cap size
		"""
		k 		= self._LAYER_OBJECTS[kwargs['ind']]
		tmp 	= update_default_kwargs(self._LINE_DEFAULTS,kwargs)
		tmp['x']= x
		tmp['y']= y
		pdict	= {}
		# remove all auto
		for key,val in tmp.iteritems():
			if val is not 'Auto':
				pdict[key] = val
		k.add_plotdata(**pdict)
		return

	def makePlot(self):
		"""
		generates the matplotlib object from all inputs
		"""
		if self.PLOT_SETTINGS['xkcd']:
			plt.xkcd()
		for i,name in enumerate(self._LAYER_NAMES):
			name 	= self._LAYER_NAMES[i]
			k 		= self._LAYER_OBJECTS[i]
			setting = self._LAYER_SETTINGS[i]
			print 'working on layer : %s' % name
			# if axes is twin'd
			if setting['twin'] is not None:
				# grab the axes object to copy
				ind 	= self._LAYER_NAMES.index(setting['twin_ref'])
				mpobj 	= self._LAYER_PLT_OBJECT[ind]
				if setting['twin'] == 'x':
					mpobj = mpobj.twinx()
				else:
					mpobj = mpobj.twiny()
			elif k.SETTINGS['location'] is None:
				mpobj 	= plt.axes()
			else:
				loc_txt = k.SETTINGS['location']
				if self.PLOT_SETTINGS['tight_layout']:
					loc_cor = self._LOCATION_TIGHT[loc_txt]
				else:
					loc_cor = self._LOCATION[loc_txt]
				mpobj = plt.axes(loc_cor)
			# ADD PLOTDATA
			if len(k.DATA_LIST) is not 0:
				# generate color,marker,fill list for the plot
				color_marker_fill 	= []
				inc_cnt = 0
				for pd in k.DATA_LIST:
					if pd['increment']:
						inc_cnt += 1
				# unique colors
				if k.SETTINGS['uniq_cols']:
					cols = unique_colors(inc_cnt+1)
					for col in cols:
						color_marker_fill.append((col,None,None))
				else:
					for cnt in range(0,inc_cnt+1):
						cind = cnt%len(self._COLOR_LIST)-1
						mind = (cnt // len(self._COLOR_LIST)) % len(self._MARKER_LIST)
						find = (cnt // (len(self._COLOR_LIST)*len(self._MARKER_LIST))) % len(self._MARKER_FILL_LIST)
						color 	= self._COLOR_LIST[cind]
						marker 	= self._MARKER_LIST[mind]
						fill	= self._MARKER_FILL_LIST[find]
						color_marker_fill.append((color,marker,fill))
				# # plotting portion
				cnt = 0
				for pd in k.DATA_LIST:
					col , mar , fill = color_marker_fill[cnt]
					if pd['increment']:
						cnt += 1
					pd['color'] = col
					pd['marker']= mar
					pd['mfc']	= fill
					pd.pop('increment')
					mpobj.errorbar(**pd)
			# do stuff to mpobj
			# TITLE
			if k.SETTINGS['title'] is not None:
				mpobj.set_title(k.SETTINGS['title'],**k.SETTINGS['title_prop'])
			# GRID
			if k.SETTINGS['grid_bool']:
				mpobj.grid(**k.SETTINGS['grid_prop'])
			# AXES TYPE AND BASE SETTING
			if k.SETTINGS['axes_type'] in ['log-log','semilog-x','semilog-y']:
				if k.SETTINGS['axes_type'] is 'log-log':
					mpobj.set_xscale('log',basex=k.SETTINGS['x_base'])
					mpobj.set_yscale('log',basey=k.SETTINGS['y_base'])
				elif k.SETTINGS['axes_type'] is 'semilog-y':
					mpobj.set_yscale('log',basey=k.SETTINGS['y_base'])
				else:
					mpobj.set_xscale('log',basex=k.SETTINGS['x_base'])
			else:
				mpobj.set_xscale('linear')
				mpobj.set_yscale('linear')
			# AXES LABELS, TICKS, FORMATTING, and PARAMETERS 
			if k.SETTINGS['xlabel'] is not None:
				mpobj.set_xlabel(k.SETTINGS['xlabel'],**k.SETTINGS['xlab_prop'])
			if k.SETTINGS['ylabel'] is not None:
				mpobj.set_ylabel(k.SETTINGS['ylabel'],**k.SETTINGS['ylab_prop'])
			if k.SETTINGS['xticks'] is not None:
				mpobj.set_xticks(k.SETTINGS['xticks'])
				mpobj.set_xticklabels(k.SETTINGS['xticks'],**k.SETTINGS['xtick_prop'])
			if k.SETTINGS['yticks'] is not None:
				mpobj.set_yticks(k.SETTINGS['yticks'])
				mpobj.set_yticklabels(k.SETTINGS['yticks'],**k.SETTINGS['ytick_prop'])
			if k.XTICK_FORMAT is not None:
				mpobj.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
				mpobj.ticklabel_format(axis='x',**k.XTICK_FORMAT)
			if k.YTICK_FORMAT is not None:
				mpobj.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
				mpobj.ticklabel_format(axis='y',**k.YTICK_FORMAT)				
			if k.XTICK_PARAM is not None:
				mpobj.tick_params(axis='x',**k.XTICK_PARAM)
			if k.YTICK_PARAM is not None:
				mpobj.tick_params(axis='y',**k.YTICK_PARAM)
			# AXES LIMITS
			if k.SETTINGS['x_limit'] is not None:
				xmin , xmax = k.SETTINGS['x_limit']
				if xmin is not None:
					mpobj.set_xlim(xmin=xmin)
				if xmax is not None:
					mpobj.set_xlim(xmax=xmax)
			if k.SETTINGS['y_limit'] is not None:
				ymin , ymax = k.SETTINGS['y_limit']
				if ymin is not None:
					mpobj.set_ylim(ymin=ymin)
				if ymax is not None:
					mpobj.set_ylim(ymax=ymax)
			# FRAME ELEMENTS
			if not k.FRAMES['top']:
				mpobj.spines['top'].set_color('None')
			if not k.FRAMES['bottom']:
				mpobj.spines['bottom'].set_color('None')
			if not k.FRAMES['right']:
				mpobj.spines['right'].set_color('None')
			if not k.FRAMES['left']:
				mpobj.spines['left'].set_color('None')
			# ADD AXHLINE
			if len(k.AXHLINE_LIST) is not 0:
				for ax in k.AXHLINE_LIST:
					# convert xmin and xmax values to x,y values
					if 'xmin' in ax.keys():
						xmin , err = convert_xy(mpobj,ax['xmin'],0)
						ax['xmin'] = xmin
					if 'xmax' in ax.keys():
						xmax , err = convert_xy(mpobj,ax['xmax'],0)
						ax['xmax'] = xmax
					mpobj.axhline(**ax)
			# ADD AXVLINE
			if len(k.AXVLINE_LIST) is not 0:
				for ax in k.AXVLINE_LIST:
					# convert ymin and xmax values to x,y values
					if 'ymin' in ax.keys():
						err , ymin = convert_xy(mpobj,0,ax['ymin'])
						ax['ymin'] = ymin
					if 'ymax' in ax.keys():
						err, ymax  = convert_xy(mpobj,0,ax['ymax'])
						ax['ymax'] = ymax
					mpobj.axvline(**ax)
			# ADD TEXT
			if len(k.TEXT_LIST) is not 0:
				for txt in k.TEXT_LIST:
					txt['s'] = txt.pop('txt')
					mpobj.text(**txt)
			# ADD LEGEND
			if k.SETTINGS['leg_props'] is not None:
				if k.SETTINGS['leg_props']['bool']:
					k.SETTINGS['leg_props'].pop('bool')
					mpobj.legend(prop=k.SETTINGS['leg_fprop'],**k.SETTINGS['leg_props'])
			# make copy of the entire object
			self._LAYER_PLT_OBJECT.append(mpobj)
		if self.PLOT_SETTINGS['tight_layout']:
			plt.tight_layout(pad=1.0)
		return

	def saveMe(self,fname,**kwargs):
		"""
		saves the figure to file $fname$ 

		** args **
		fname 	- path/filename to save to

		** kwargs ** 
		height 	- dimension of figure, in inches
		width 	- dimension of figure, in inches
		dpi 	- the dots per inch of the figure
		"""
		if self._SAVED is None:
			self._SAVED = pickle.dumps(self,pickle.HIGHEST_PROTOCOL)
		sf = update_default_kwargs(self.SAVEFIG_SETTINGS,kwargs)
		fig = plt.gcf()
		if 'width' in sf and 'height' in sf:
			fig.set_size_inches(sf['width'],sf['height'])
			sf.pop('width')
			sf.pop('height')
		plt.savefig(fname,**sf)
		return

	def saveObj(self,fname):
		"""
		saves the plot objects to a file $fname$ to edit later

		** args **
		fname 	- path/filename to save to
		"""
		f = open(fname,'wb')
		if self._SAVED is None:
			#save_list = [self.PLOT_SETTINGS , self._LAYER_NAMES , self._LAYER_OBJECTS , self._LAYER_SETTINGS]
			#pickle.dump(save_list,f)
			pickle.dump(self,f,pickle.HIGHEST_PROTOCOL)
		else:
			f.write(self._SAVED)
		f.close()
		return

	def showMe(self):
		"""
		shows the figure which has been generated
		note : this depends on the backend selected
		"""
		if self._SAVED is None:
			self._SAVED = pickle.dumps(self,pickle.HIGHEST_PROTOCOL)
		plt.show()
		return

class kaxes(object):
	"""
	helper class for kaplot, all functions here are internal. 
	used to build layer objects for the final figure.
	"""
	# location options
	_LOCATION = ['upper left', 'upper right', 'lower left', 'lower right']

	def __init__(self):
		self.SETTINGS 	= 	{	'plot_type'	:	'line'		, \
								'uniq_cols'	:	False		, \
								'location'	:	None		, \
								'title'		:	None		, \
								'title_prop':	None		, \
								'grid_bool'	:	False		, \
								'grid_prop'	:	None		, \
								'axes_type'	:	'linear'	, \
								'x_base'	:	1.0			, \
								'y_base'	:	1.0			, \
								'xlabel'	:	None		, \
								'xlab_prop'	:	None		, \
								'ylabel'	:	None		, \
								'ylab_prop'	:	None		, \
								'xticks'	:	None		, \
								'xtick_prop':	None		, \
								'yticks'	:	None		, \
								'ytick_prop':	None		, \
								'x_limit'	:	None		, \
								'y_limit'	:	None		, \
								'leg_props'	:	None		, \
								'leg_fprop'	:	None}

		self.FRAMES 	= 	{	'top'		:	True 		, \
								'bottom'	:	True 		, \
								'left'		:	True 		, \
								'right'		:	True}
		self.XTICK_PARAM 	=	None
		self.YTICK_PARAM 	=	None
		self.XTICK_FORMAT 	= 	None
		self.YTICK_FORMAT 	= 	None
		self.AXHLINE_LIST	= 	[]
		self.AXVLINE_LIST	= 	[]
		self.TEXT_LIST 		= 	[]
		self.DATA_LIST		= 	[]
		return

	def set_location(self,location):
		if location is type([]) and len(location) == 4:
			self.SETTINGS['location'] = location
		elif location is None:
			self.SETTINGS['location'] = None
		elif location.lower() in self._LOCATION:
			self.SETTINGS['location'] = location.lower()
		else:
			print 'KAXES: set_location error. location does not exist.'
		return

	def set_plot_type(self,ptype):
		self.SETTINGS['plot_type'] = ptype
		return

	def set_title(self,title,**fdict):
		if title is not None:
			self.SETTINGS['title'] = title
			self.SETTINGS['title_prop'] = fdict
		else:
			print 'KAXES: set_title error. title is None.'
		return

	def set_grid(self,gbool,**gdict):
		if gbool:
			self.SETTINGS['grid_bool'] 	= True
			self.SETTINGS['grid_prop']	= gdict
		return

	def set_axes_type(self,ptype):
		self.SETTINGS['axes_type'] = ptype.lower()
		return

	def set_base(self,basex,basey):
		self.SETTINGS['x_base'] = basex
		self.SETTINGS['y_base'] = basey
		return

	def set_xlabel(self,lab,**fdict):
		self.SETTINGS['xlabel'] 	= lab
		self.SETTINGS['xlab_prop']	= fdict
		return

	def set_ylabel(self,lab,**fdict):
		self.SETTINGS['ylabel'] 	= lab
		self.SETTINGS['ylab_prop']	= fdict
		return

	def set_xticks(self,myList,**fdict):
		self.SETTINGS['xticks']		= myList
		self.SETTINGS['xtick_prop']	= fdict
		return

	def set_yticks(self,myList,**fdict):
		self.SETTINGS['yticks']		= myList
		self.SETTINGS['ytick_prop']	= fdict
		return

	def set_xlim(self,xmin,xmax):
		self.SETTINGS['x_limit']	= [xmin, xmax]
		return

	def set_ylim(self,ymin,ymax):
		self.SETTINGS['y_limit']	= [ymin, ymax]
		return

	def set_frames(self,**frames):
		frame_dict = update_default_kwargs(self.FRAMES,frames)
		self.FRAMES = frame_dict
		return

	def set_x_tick_params(self,**params):
		self.XTICK_PARAM = params
		return

	def set_y_tick_params(self,**params):
		self.YTICK_PARAM = params
		return

	def set_unique_colors(self,ubool):
		self.SETTINGS['uniq_cols'] = ubool
		return

	def set_y_tick_format(self,**p):
		self.YTICK_FORMAT = {'style':p['style'], 'scilimits':(p['sci_min'],p['sci_max'])}
		return

	def set_x_tick_format(self,**p):
		self.XTICK_FORMAT = {'style':p['style'], 'scilimits':(p['sci_min'],p['sci_max'])}
		return

	def add_axhline(self,**ax):
		self.AXHLINE_LIST.append(ax)
		return

	def add_axvline(self,**ax):
		self.AXVLINE_LIST.append(ax)
		return

	def add_text(self,**text):
		self.TEXT_LIST.append(text)
		return

	def add_plotdata(self,**pdict):
		self.DATA_LIST.append(pdict)
		return

	def set_legend(self,fdict,**kwargs):
		self.SETTINGS['leg_fprop'] = fdict
		self.SETTINGS['leg_props'] = kwargs
		return

## HELPER FUNCTIONS
def update_default_kwargs(default_dict,current_dict):
	"""
	dictionary helper function. takes a $default_dict$ and combines it
	with $current_dict$ while filling in missing values. 

	** args **
	default_dict - complete dictionary
	current_dict - user supplied dictionary

	returns a dictionary with all values.
	"""
	return_dict = {}
	for key,kval in default_dict.iteritems():
		if key in current_dict:
			return_dict[key] = current_dict[key]
		else:
			if kval is not 'Auto':
				return_dict[key] = kval
	return return_dict

def srange(start,end,incr,log=False):
	"""
	returns a number range, from $start$ to $end$ with an 
	increment value of $incr$ , it can also be incremented
	multiplicativly by specifying the $log$ boolean.

	** args **
	start 	- start value
	end 	- finish value
	icnr	- increment
	log 	- multiply instead of add boolean

	returns a list
	"""
	if incr == 0:
		return []
	if start == end:
		return []
	if log == False:
		cval = float(start)
		retList =[]
		while cval <= end:
			retList.append(cval)
			cval = float(cval)+float(incr)
	else:
		cval = start
		retList = []
		while cval <= end:
			retList.append(cval)
			cval = float(cval)*float(incr)
	return retList

def convert_xy(ax,x,y):
	"""
	converts $x$ and $y$ coordinates on an axes object, $ax$ to the 
	matplotlib normalized values.

	** args **
	ax 		- matplotlib axes object
	x 		- x value 
	y 		- y value 

	returns normalized coordinate tuple
	"""
	rx , ry = ax.transAxes.inverted().transform(ax.transData.transform((x,y)))
	return (rx,ry)

def unique_colors(ncols,color_map='gist_rainbow'):
	"""
	color generating function. $ncols$ specifies how many unique colors 
	to generate from $color_map$. for more color_map options consult :
	http://matplotlib.org/examples/color/colormaps_reference.html

	** args **
	ncols 		- number of colors
	color_map	- matplotlib colormap name

	returns a list of color tuples
	"""
	retList = []
	cm = plt.get_cmap(color_map)
	for i in range(ncols):
		color = cm(1.0*i/ncols)
		retList.append(color)
	return retList
