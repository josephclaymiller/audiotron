#Game2Stereo_Shane Rhythm Guitar.wav
#[0,2,6,10,14,16,18,22,26,30,32,34,38,42,46,48,50,54,58,62,64,66,70,74,78,80,82,86,90,94,96,98,102,106,110,112,114,118,122,126,128,130,134,138,142,144,146,150,154,158,160,162,166,170,174,176,178,182,186,190,192,194,198,202,206,208,210,214,218,222,224,226,230,234,238,240,242,246,250,254,256,258,262,266,270], 
#x*16, x*16+2, x*16+6, x*16+10, x*16+14

#Game2Stereo_Shane upbeat Vidaurri.wav
#[0,2,6,10,14,18,22,26,30,34,38,42,46,50,54,58,62,66,70,74,78,82,86,90,94,98,102,106,110,114,118,122,126,130,134,138,142,146,150,154,158,162,166,170,174,178,182,186,190,194,198,202,206,210,214,218,222,226,230,234,238,242,246,250,254,258,262,266,270]
#x*4+2 & 0

#Game2Stereo_Tom Hon Solo.wav
#[0,2,6,10,12,14,16,18,22,26,28,30,32,34,38,42,44,46,48,50,54,58,60,62,64,66,70,74,76,78,
#						80,82,86,88,90,92,94,96,98,102,106,108,110,112,114,118,122,124,126,
#						128,130,134,136,138,140,142,144,148,150,154,156,160,162,164,166,168,170,172,174,176,178,180,182,184,186,188,190,
#						192,194,198,202,204,206,208,210,214,216,218,222,224,226,230,232,234,236,238,240,242,
#						246,248,250,254,256,258,262,264,266,270]

#Game2Stereo_Brian Backup Trumpet

measures = 17
sixteenths = measures * 16

enemyLevels = ['testEnemy']
comboLevels = [4]

enemyData = \
{
	'testEnemy':
	{
		'model':		'enmod01',
		'anim':			'enemy01animation',
		'playRate':		3.0,
		'scale':		0.25,
		'cScale':		2,
		'music':		'Game2Stereo_Shane Rhythm Guitar.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[0,2,6,10,14,16,18,22,26,30,32,34,38,42,46,48,50,54,58,62,64,66,70,74,78,80,82,86,90,94,96,98,102,106,110,112,114,118,122,126,128,130,134,138,142,144,146,150,154,158,160,162,166,170,174,176,178,182,186,190,192,194,198,202,206,208,210,214,218,222,224,226,230,234,238,240,242,246,250,254,256,258,262,266,270],#[120,124,128,144,160,184],
		'beatsLight':	[],
	},
	
	'1': #pyramid dudes
	{
		'model':		'enmod01',
		'scale':		0.25,
		'cScale':		2,
		'music':		'some.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	'2': #tri-angle tipped pom-poms
	{
		'model':		'enmod12',
		'scale':		0.075,
		'cScale':		6.66,
		'music':		'some.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	'3': #cube dudes
	{
		'model':		'enmod03',
		'scale':		0.05,
		'cScale':		10,
		'music':		'some.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	'4': #squids
	{
		'model':		'enmod04',
		'scale':		0.125,
		'cScale':		4,
		'music':		'some.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	'5': #dradles
	{
		'model':		'enmod05',
		'scale':		0.075,
		'cScale':		6.66,
		'music':		'some.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	'6': #fans
	{
		'model':		'enmod06',
		'scale':		0.075,
		'cScale':		6.66,
		'music':		'some.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	'7': #x's with flare
	{
		'model':		'enmod08',
		'scale':		0.05,
		'cScale':		10,
		'music':		'some.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	'8': #spikes
	{
		'model':		'enmod13',
		'scale':		0.075,
		'cScale':		6.66,
		'music':		'some.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
}