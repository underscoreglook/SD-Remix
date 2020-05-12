# Super Smash Brothers Melee: SD Remix
SD Remix is a mod of SSBM. Its main purpose is to balance the cast.
It also includes more stages and more features, such as crew battle mode, created by the Super Smash Brothers Melee modding community.

See http://sdremix.games for more information.

As this is a mod, an understanding of Melee hacking is expected if you're to use this repo. See the Melee Workshop forum on Smashboards to get started.


## Project Structure
### DOL changes 
Melee Code Manager is how DOL mods are applied for SD Remix. All mods live in MCM_Mods.
The expectation is for you to make a symlink from the "Mods Library" folder in MCM to the MCM_Mods folder provided in this repo (recommended to name the symlink "SD Remix"). This should create a new folder tab in MCM, which we can use to apply these mods.

### Configs
The config directory controls various configuration items that are used in deploy scripts.

#### game.cfg
##### METADATA section
This section holds various data that describes the game, stored in various.
* GAME_ID = This is the alphanumeric 4-length game ID we want to use, like GALE for Melee
* MAKER_CODE = This is the alphanumeric 2-length maker code we want to use, like 01 for Melee
* REVISION = This is the version number for this game. It can be from 0 to 255. Is 2 for Melee 1.02.
* GAME_NAME = The ASCII name for the game. It is "Super Smash Bros Melee" for Melee.
##### FILES_STRUCTURE section
The SSBM ISO isn't very tightly packed, because there's actually a lot of space leftover on the disc. As a result, some of the basic files (like the FST, DOL, and Debug stuff) are separated out by a huge amount. This section packs these items closer together. Read the comments in the config for more information.

### Characters
All characters should be stored in the "chars" directory. The main tool people use at the moment to change character files is Crazy Hand, which works directly with ISO files. As a result, when a change is made, the raw Pl*.dat files should be copied over to the "chars" directory and committed, with good commit messages saying what exactly has changed, since it's hard to read binary file changes.

### Stages
Much like characters, all stages are stored as raw .dat files. We don't replace any Melee stages, however, to have all the base stages still available, which are all of the name format "Gr*.dat". Instead, we store extra files as "Go*.dat", and we use DOL mods to specifically load those in.
Similarly to characters, the commit messages should be descriptive, as these are binary file changes.

### Menus
Menus files all live in the "menus" folder. They are all binary files, and thus commit messages should be descriptive.

opening.bnr is a particularly special file. It holds basic game metadata, including game descriptions and the game banner. This can be edited in the "DAT Texture Wizard".

Files starting with "Sd" are text files. These have to be edited with a hex editor. These are not ascii text, though. There should be a "Menu Text" converter in the "Melee Code Manager" tools section, and you can use this to both find existing string to replace or to write new strings.

The rest of the edits to this file can be done using the "DAT Texture Wizard" to change textures. There ARE non-texture changes that were made to some files, but it's unlikely we'll need to change them, so I'm just going to ignore them for now.

There is also an assets folder which hold raw assets for the menus. In order to edit a texture, you should first find the texture in "DAT Texture Wizard", then export that texture to the assets directory USING THE DEFAULT NAME. Then make changes to the asset. Then reimport that texture into the menu file. The texture is imported based on its name, which is why the name is important. Once an asset has been exported, it can be kept in the assets directory, where new changes can be made using the image files there instead of re-exporting every time we want to make a change. This way, it will also be a good way to see what assets have been changed in SD Remix.


## How to compile/build SDR from source
This goes over the deployment process, from the source files provided here to make all the builds.

### Compiling/building files
Currently, only Windows is supported for building. Also, this requires Python 3 to be installed, and that "python.exe" is in your PATH.

First, extract the Melee v1.02 ISO using GC-Tool and put it somewhere on your hard drive.

Second, create a text file called "isoRootPath.txt" in the configs directory and have it just be one line with the path to the "root" folder of the extracted ISO. This text file should be automatically ignored by git. NOTE: The directory pointed to has to contain UNALTERED Melee v1.02 files, so if they've been changed, the build will not work.

Third, run the "build.bat". This should (re)create a "root" directory in the "build" directory, and put all changed files except for the DOL file.

Third, we need to build the DOL. This is done via Melee Code Manager. Open the 1.02 Melee DOL in MCM and go to the "SD Remix" tab and select everything in here. Then "Save as" to save a new DOL. This DOL should be saved as "build/root/&&systemdata/Start.dol". NOTE: In the "Settings" mod group, there are a bunch of codes for setting default settings. Most of these can also be done through the Custom Rules UI in MCM, by selecting tournament rules. The two that can't be fixed this way are the omega and alpha stage mods. The alpha stage mods will likely cause 

### Building an ISO
Make a fresh copy of the Melee v1.02 extracted root folder. Then copy everything in build/root into the root directory of Melee v1.02.
After everything has been copied, build an ISO using GCR and the now altered Melee v1.02 root directory.