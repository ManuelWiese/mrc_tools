# mrc_tools
Tools to convert mrc workout files to erg or wahooplan files(works on ELEMNT and ELEMNT bolt)

# Requirements
python3(tested on version 3.6.5)

# How to use
Converting mrc to erg using FTP
```
python3 mrc_to_erg.py MRC_FILE FTP
python3 mrc_to_erg.py workout.mrc 300
```
This will create a workout.erg file.

Converting mrc to wahooplan
```
python3 mrc_to_wahoo_plan.py MRC_FILE
python3 mrc_to_wahoo_plan.py workout.mrc
```
This will create a workout.plan file.
# Where to place wahooplan file
## Android
Place *.plan files in /sdcard/ELEMNT/plans folder
## iOS
Please help to find out!
