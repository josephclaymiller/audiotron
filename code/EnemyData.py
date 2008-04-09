measures = 17
sixteenths = measures * 16

enemyData = \
{
	"testEnemy":
	{
		"model":		"emenytb_t1",
		"music":		"some.wav",
		"lighting":		('ALred', 'DLRblue', 'DLBwhite'),
		"beatsPulse":	[x * 4 for x in range(sixteenths / 4)],
		"beatsLight":	[],
	},
}