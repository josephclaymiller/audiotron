#Game2Stereo_Shane Rhythm Guitar.wav
#[0,2,6,10,14,16,18,22,26,30,32,34,38,42,46,48,50,54,58,62,64,66,70,74,78,80,82,86,90,94,96,98,102,106,110,112,114,118,122,126,128,130,134,138,142,144,146,150,154,158,160,162,166,170,174,176,178,182,186,190,192,194,198,202,206,208,210,214,218,222,224,226,230,234,238,240,242,246,250,254,256,258,262,266,270]
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

#Game2Stereo_Kevin hachacha
#[0,2,3,4,6,7,8,10,11,12,14,15,16,18,19,20,22,23,24,26,27,28,30,31,32,34,35,36,38,39,40,42,43,44,46,47,48,50,51,52,54,55,56,58,59,60,62,63,64,66,67,68,70,71,72,74,75,76,78,79,80,82,83,84,86,87,88,90,91,92,94,95,96,98,99,100,102,103,104,106,107,108,110,111,112,114,115,116,118,119,120,122,123,124,126,127,128,130,131,132,134,135,136,138,139,140,142,143,144,146,147,148,150,151,152,154,155,156,158,159,160,162,163,164,166,167,168,170,171,172,174,175,176,178,179,180,182,183,184,186,187,188,190,191,192,194,195,196,198,199,200,202,203,204,206,207,208,210,211,212,214,215,216,218,219,220,222,223,224,226,227,228,230,231,232,234,235,236,238,239,240,242,243,244,246,247,248,250,251,252,254,255,256,258,259,260,262,263,264,266,267,268,270,271]

#Game2Stereo_Brian Backup Trumpet
#[4,12,20,28,36,44,52,60,68,76,84,92,100,108,116,120,124,128,144,160,184,188,192,220,224,228,236,244,252,260,268]

#Game2Stereo_Brian Backup Vocals
[0,14,56,60,64,78,84,92,100,108,116,124,132,140,148,156,164,172,180,188,196,204,212,220,228,236,244,252,260,268]

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
		'beatsPulse':	[0,14,56,60,64,78,84,92,100,108,116,124,132,140,148,156,164,172,180,188,196,204,212,220,228,236,244,252,260,268],
		'beatsLight':	[],
	},
	
	#level 1 enemy
	'1': #pyramid dudes
	{
		'model':		'enmod01',
		'scale':		0.25,
		'cScale':		2,
		'music':		'Game2Stereo_Tom Hon Solo.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	#level 2 enemy
	'2': #tri-angle tipped pom-poms
	{
		'model':		'enmod12',
		'scale':		0.075,
		'cScale':		6.66,
		'music':		'Game2Stereo_Shane Rhythm Guitar.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	#level 3 enemy
	'3': #cube dudes
	{
		'model':		'enmod03',
		'scale':		0.05,
		'cScale':		10,
		'music':		'Game2Stereo_Shane upbeat Vidaurri.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	#level 3 enemy
	'4': #squids
	{
		'model':		'enmod04',
		'scale':		0.125,
		'cScale':		4,
		'music':		'Game2Stereo_Kevin hachacha.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	#level 4 enemy
	'5': #dradles
	{
		'model':		'enmod05',
		'scale':		0.075,
		'cScale':		6.66,
		'music':		'Game2Stereo_Kevin Backup Guitar.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	#level 4 enemy
	'6': #fans
	{
		'model':		'enmod06',
		'scale':		0.075,
		'cScale':		6.66,
		'music':		'Game2Stereo_Brian Backup Trumpet.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	#level 5 enemy
	'7': #x's with flare
	{
		'model':		'enmod08',
		'scale':		0.05,
		'cScale':		10,
		'music':		'Game2Stereo_Brian Backup Vocals Hi.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
	
	#level 6 enemy
	'8': #spikes
	{
		'model':		'enmod13',
		'scale':		0.075,
		'cScale':		6.66,
		'music':		'Game2Stereo_Brian Backup Vocals.wav',
		'lighting':		('ALred', 'DLRblue', 'DLBwhite'),
		'beatsPulse':	[x * 4 for x in range(sixteenths / 4)],
		'beatsLight':	[],
	},
}
