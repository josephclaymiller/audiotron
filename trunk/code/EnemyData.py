measures = 17
sixteenths = measures * 16

enemyData = \
{
	"testEnemy":
	{
		"model":		"enemy_tb_trans_am_incan",
		"music":		"some.wav",
		"lighting":		('ALred', 'DLRblue', 'DLBwhite'),
		"beatsPulse":	[x * 4 for x in range(sixteenths / 4)],
		"beatsLight":	[],
	},
}