# Super Smash Brothers Melee: SD Remix
SD Remix is a mod of SSBM. Its main purpose is to balance the cast. It also includes more stages and more features,
such as crew battle mode, created by the Super Smash Brothers Melee modding community.

See http://sdremix.games for more information.

As this is a mod, an understanding of Melee hacking is expected if you're to use this repo. See the Melee Workshop
forum on Smashboards to get started.


# Building
This goes over the deployment process, from the source files provided here to make all the builds. At the moment, only
windows is supported.

## Prerequisites
Currently, only Windows is supported for building.
Requires:
* Requires Python 3 to be installed, and that "python.exe" is in your PATH.
* Requires GameCube Rebuilder. The current version we use is 1.1.
* Optional: Dolphin (if you want to use the "Run With Dolphin" script)
* Finally: Requires an ISO of SSBM NTSC.

## Configure Build
The first time you build, you first need to run configure.bat. This will ask you to specify the location of various
prerequisites. Based on this should create a config file that holds the paths to all of these items so you don't need
to specify them on each build.

You may run this again if you change the locations of prerequisites or if something went wrong.

## Build
The build script is build.bat. By default, running this does a full build. However, you can pass an argument to the
script to build different targets. The following sections will describe what the various targets do.

### "clean" target
"build.bat clean" will completely clean the build folder to start things back as new.

### Common to all other targets
First, it will extract the Melee ISO to the raw files, so we can use it as a base.

Second, it will copy all the game files in "chars", "stages", and "menus" to a sdr build folder. It will also copy the
dol file to the system folder in that sdr build folder.

Third, it will build other system files, in particular, the Game's TOC and ISO Header files.

### "full" target
This target builds every other target below

### 'iso' target
This target builds a playable ISO in the build directory as "game.iso".

### 'diosmios' target
This target builds a folder in the build directory called "DiosMiosFiles", which contains files that can be copied
into a Dios Mios compatible folder containing Super Smash Brothers Melee to turn it into SD Remix.

### 'xdelta' target
This builds an ISO, just like the ISO target, but then also creates xdelta patches with the base being various Melee
ISOs. This uses version specific Melee ISOs and creates xdelta files in the build directory of the form
"SDR 1.0[v].xdelta", where "[v]" is the version number of the ISO it's based of off.


# File Structure

## DOL 
Melee Code Manager is how DOL mods are applied for SD Remix. All mods live in the "MCM_Mods" directory.

There's also the "dol" folder, where the "Start.dol" should be save to using MCM. If you make a change to MCM mods,
you should also build the dol to "dol/Start.dol" as well, as MCM does not have a command line interface, so we can't
automatically build it (yet).

## Configs
The config directory controls various configuration items that are used in deploy scripts.

### game.cfg

#### METADATA section
This section holds various data that describes the game, stored in various.
* GAME_ID = This is the alphanumeric 4-length game ID we want to use, like GALE for Melee
* MAKER_CODE = This is the alphanumeric 2-length maker code we want to use, like 01 for Melee
* REVISION = This is the version number for this game. It can be from 0 to 255. Is 2 for Melee 1.02.
* GAME_NAME = The ASCII name for the game. It is "Super Smash Bros Melee" for Melee.
#### FILES_STRUCTURE section
The SSBM ISO isn't very tightly packed, because there's actually a lot of space leftover on the disc. As a result,
some of the basic files (like the FST, DOL, and Debug stuff) are separated out by a huge amount. This section packs
these items closer together. Read the comments in the config for more information.

## Characters
All characters should be stored in the "chars" directory. The main tool people use at the moment to change character
files is Crazy Hand, which works directly with ISO files. As a result, when a change is made, the raw Pl*.dat files
should be copied over to the "chars" directory and committed, with good commit messages saying what exactly has changed,
since it's hard to read binary file changes.

## Stages
Much like characters, all stages are stored as raw .dat files. We don't replace any Melee stages, however, to have all
the base stages still available, which are all of the name format "Gr*.dat". Instead, we store extra files as "Go*.dat",
and we use DOL mods to specifically load those in.

Similarly to characters, the commit messages should be descriptive, as these are binary file changes.

## Menus
Menus files all live in the "menus" folder. They are all binary files, and thus commit messages should be descriptive.

opening.bnr is a particularly special file. It holds basic game metadata, including game descriptions and the game
banner. This can be edited in the "DAT Texture Wizard".

Files starting with "Sd" are text files. These have to be edited with a hex editor. These are not ascii text, though.
There should be a "Menu Text" converter in the "Melee Code Manager" tools section, and you can use this to both find
existing string to replace or to write new strings.

The rest of the edits to this file can be done using the "DAT Texture Wizard" to change textures. There ARE non-texture
changes that were made to some files, but it's unlikely we'll need to change them, so I'm just going to ignore them for
now.

There is also an assets folder which hold raw assets for the menus. In order to edit a texture, you should first find
the texture in "DAT Texture Wizard", then export that texture to the assets directory USING THE DEFAULT NAME. Then make
changes to the asset. Then reimport that texture into the menu file. The texture is imported based on its name, which is
why the name is important. Once an asset has been exported, it can be kept in the assets directory, where new changes
can be made using the image files there instead of re-exporting every time we want to make a change. This way, it will
also be a good way to see what assets have been changed in SD Remix.

## Scripts
The scripts directory holds the scripts necessary for building SDR.