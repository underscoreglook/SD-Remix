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
* Requires: Python 3 to be installed, and that "python.exe" is in your PATH.
* Requires: GameCube Rebuilder. The current version we use is 1.1.
* Requires: An ISO of SSBM NTSC (any version, tested with v1.02).
* Optional: Dolphin (if you want to use the "Run With Dolphin" script)
* Optional: xdelta 3.0.11 executable (tested with 64 bit version, for xdelta target)
* Optional: ISOs of all three versions of SSBM NTSC, to create xdelta patches from (for xdelta target)

## Configure Build
The first time you build, you first need to run configure.bat. This will ask you to specify the location of various
prerequisites. Based on this should create a config file that holds the paths to all of these items so you don't need
to specify them on each build. If a prerequisite is optional, you may simply cancel the open file dialog and it will
be skipped.

You may run this again if you change the locations of prerequisites, something went wrong, or you want to include an
optional item that you previously didn't specify.

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

### 'xdelta' target
This builds an ISO, just like the ISO target, but then also creates xdelta patches with the base being various Melee
ISOs. This uses version specific Melee ISOs and creates xdelta files in the build directory of the names
"SDR from 1.0[v].xdelta", where "[v]" is the minor version number of the ISO it's based of off.

This requires the xdelta executable and copies of all the Melee NTSC ISOs.

## Testing Built Iso
If you specified a Dolphin exe using configure.bat and also built an ISO using the build script, you can use the
play_iso.bat to play the ISO you've built.

## Creating DIOS MIOS file replacements
There are still some people that use DIOS MIOS with extracted files. It is not supported by our build system because
there are much easier ways to play SDR nowadays, and it comparatively doesn't save much time. However, here's the
way to create a fileset that can be dropped into a GALE01 folder for use with DIOS MIOS with GCReEx folder format.
1. Use the build script to build either the "iso" or "full" targets.
2. Create a folder where the DIOS MIOS SD Remix files will go. I'll call in "DIOS_MIOS_SDR" in these instructions.
3. Create a directory inside "DIOS_MIOS_SDR" called "root".
4. Copy all the files in build/sdrFiles to SDR_FILES/root. Do NOT copy the "&&systemdata" folder.
5. Download GCReEx.
6. Copy build/game.iso to the GCReEx folder, in the same folder as the EXE.
7. Open a command line in the GCReEx folder, run
8. Run the command "gcreex.exe -x game.iso". It should extract the SDR ISO in GCReEx format in a folder it creates
based on the GAME_ID and MAKER_CODE from configs/game.cfg.
9. After it's finished, copy the "sys" folder within the created folder into your "DIOS_MIOS_SDR" folder.
10. The DIOS_MIOS_SDR folder should now be the complete set of files needed to play with DIOS MIOS. Package it with
any other files (like a readme, changelist, or whatever).

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

## docs
This contains both docs intended for external consumption (for players) and for internal consumption (for devs).

### internal
This folder is meant for any documentation that's designed for other developers, such as notes for codes, how
different parts of the codebase is designed, explanation of changes, etc.

### external
This folder is meant to hold any documentation that is meant to be bundled with builds, put on the website, or
would otherwise be useful for players.

#### SDRE32.ini
This is the Dolphin Gecko Code file. It holds codes meant to be used with Slippi build of Dolphin so players can
have a better experience playing on Netplay. The player must add the file to Sys/GameSettings/ in their Slippi
folder.