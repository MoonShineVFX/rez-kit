
import os
import sys

if sys.version_info[0] == 2:
	from idlelib import PyShell as pyshell
	from idlelib.configHandler import idleConf, IdleUserConfParser
else:
	from idlelib import pyshell
	from idlelib.config import idleConf, IdleUserConfParser


# Change to use our own user configs, instead the one in home dir
this_dir = os.path.dirname(__file__)
for cfg_type in idleConf.config_types:
	cfg_path = os.path.join(this_dir, "config-%s.cfg" % cfg_type)
	idleConf.userCfg[cfg_type] = IdleUserConfParser(cfg_path)
	idleConf.userCfg[cfg_type].Load()

# Back on track
pyshell.main()
