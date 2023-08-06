#!/usr/bin/env python
#Copyright ReportLab Europe Ltd. 2000-2021
#see license.txt for license details
#history http://www.reportlab.co.uk/cgi-bin/viewcvs.cgi/public/reportlab/trunk/rl_addons/pyRXP/setup.py
if __name__=='__main__': #NO RUNTESTS
	import os, sys, re
	pkgDir=os.path.dirname(sys.argv[0])
	if not pkgDir:
		pkgDir=os.getcwd()
	elif not os.path.isabs(pkgDir):
		pkgDir=os.path.abspath(pkgDir)
	#test to see if we've a special command
	if 'test' in sys.argv:
		if len(sys.argv)!=2:
			raise ValueError('test command may only be used alone sys.argv[1:]=%s' % repr(sys.argv[1:]))
		cmd = sys.argv[-1]
		os.chdir(os.path.join(pkgDir,'test'))
		r = os.system(' '.join((sys.executable, 'runAll.py')))
		sys.exit(('!!!!! runAll.py --> %s exited with error !!!!!' % r) if r else r)
	elif 'null-cmd' in sys.argv or 'null-command' in sys.argv:
		sys.exit(0)

	try:
		from setuptools import setup, Extension
	except ImportError:
		from distutils.core import setup, Extension

	def raiseConfigError(msg):
		import exceptions 
		class ConfigError(exceptions.Exception): 
			pass 
		raise ConfigError(msg)

	LIBS = []
	LIBRARIES=[]
	EXT_MODULES = []
	EXT_KWARGS = {}
	DEFINE_MACROS=dict(CHAR_SIZE=16)
	for ev in ('DEBUG_PYRXP',):
		evv = os.environ.get(ev,'')
		try:
			evv = int(evv)
		except:
			pass
		else:
			DEFINE_MACROS[ev] = evv
	DEFINE_MACROS = list(DEFINE_MACROS.items())

	#building pyRXP
	if sys.platform=="win32":
		LIBS=['wsock32']
		if sys.version_info[:2]>=(3,5) and not int(os.environ.get('PYRXP35LONG','0')):
			EXT_KWARGS['extra_compile_args'] = ['/Od']
		#EXT_KWARGS['extra_compile_args'] = ['/Zi']
		#EXT_KWARGS['extra_link_args'] = ['/DEBUG']
	elif sys.platform=="sunos5":
		LIBS=['nsl', 'socket', 'dl']
	elif sys.platform=="aix4":
		LIBS=['nsl_r', 'dl']
	else:
		LIBS=[]

	rxpFiles = ('xmlparser.c', 'url.c', 'charset.c', 'string16.c', 'ctype16.c', 
				'dtd.c', 'input.c', 'stdio16.c', 'system.c', 'hash.c', 
				'version.c', 'namespaces.c', 'http.c', 'nf16check.c', 'nf16data.c')
	pyRXPDir = os.path.join(pkgDir,'src')
	RXPLIBSOURCES=[]
	pyRXP_c = os.path.join(pyRXPDir,'pyRXP.c')
	with open(pyRXP_c,'r') as _:
		VERSION = re.search(r'^#\s*define\s+VERSION\s*"([^"]+)"',_.read(),re.MULTILINE)
	VERSION = VERSION and VERSION.group(1) or 'unknown'
	RXPDIR=os.path.join(pyRXPDir,'rxp')
	RXPLIBSOURCES= [os.path.join(RXPDIR,f) for f in rxpFiles]
	EXT_MODULES =	[Extension( 'pyRXPU',
								[pyRXP_c]+RXPLIBSOURCES,
								include_dirs=[RXPDIR],
								define_macros=DEFINE_MACROS,
								library_dirs=[],
								# libraries to link against
								libraries=LIBS,
								**EXT_KWARGS
								),
					]

	with open('LICENSE.txt','r') as _:
		license = _.read()
	setup(	name = "pyRXP",
			version = VERSION,
			description = "Python RXP interface - fast validating XML parser",
			author = "Robin Becker",
			author_email = "robin@reportlab.com",
			url = "http://www.reportlab.com",
			packages = [],
			license=license,
			ext_modules = EXT_MODULES,
			package_data = {'': ['pyRXP-license.txt']},
            python_requires='>=3.6, <4',
            classifiers = [
				'Development Status :: 5 - Production/Stable',
				'Intended Audience :: Developers',
				'License :: OSI Approved :: BSD License',
				'Programming Language :: Python',
				'Programming Language :: C',
				'Operating System :: Unix',
				'Operating System :: POSIX',
				'Operating System :: Microsoft :: Windows',
				'Topic :: Software Development :: Libraries :: Python Modules',
				'Topic :: Text Processing :: Markup :: XML',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3.9',
                'Programming Language :: Python :: 3.10',
                ]
			)
