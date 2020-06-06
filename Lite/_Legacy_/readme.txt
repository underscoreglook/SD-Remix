=============================
==                         ==
==    SD Remix 3.2 LITE    ==
==   for SSBM NTSC v1.02   ==
==                         ==
=============================


--------------------------
- What is SD Remix Lite? -
--------------------------
SD Remix Lite is a version of SD Remix that does not require any
console modifications to run. The way it works is that it takes
advantage of a vulnurability in the name tag entry screen to run
arbitrary code from the memory card, which replaces game code with
SD Remix code. As long as you have a modified game file on a memory
card and the coorpesponding version of an SSBM disc, you can run
SD Remix Lite on unmodified GameCubes or Wiis. Essentially, SD Remix
Lite is the modified save file that turns Melee into SD Remix.


----------------------------
- How to use SD Remix Lite -
----------------------------
Before you start make sure:
  - that the modified save file you have works with the version of
    Super Smash Brothers Melee you have. See the section "SSBM
	Versions" at the end of this document for more info.
  - that this save file is on your memory card. See the section
    "Installation Instructions" for more details.

To activate SD Remix Lite:
  - Put the memory card into "Slot A" of your GameCube or Wii.
  - Boot up SSBM.
  - Once the game is loaded, go to the title screen.
  - Optionally, you may take out the memory card at the title screen
    to use it for other setups, if you're running a tournament.
  - From the main menu, go to "VS Mode" then "Name Entry". You should
    hear the announcer say "Success!" and you should see a message
	that tells you to press B.
  - Press the B button to exit the name entry screen.
SD Remix Lite is now fully activated. If you go back into the name
entry screen, you will be able to edit your name tags. Note that the
maximum number of name tags is now 15 instead of 120, to make room
for all of the SD Remix Lite changes.
You can now play SD Remix Lite! Enjoy!


-----------------------------
- Installation Instructions -
-----------------------------

Copying from one memory card to another
---------------------------------------
The way most people will get SD Remix Lite is by sharing it with
other people at events and get togethers. You can copy save files
from one memory card to another using you Gamecube or Wii.

On Gamecube, you can copy save files by going to the boot menu. You
can access the boot menu by holding A during the GameCube startup
animation. The memory card screen is the bottom menu.

On Wii, click on the "Wii" button at the Wii main screen. This will
take you to the Wii menu. Select "Data Management", then "Save Data",
then "Nintendo GameCube". You're now at the memory card screen.

Transfering from PC to Memory Card
----------------------------------
However, copying SD Remix Lite to other memory cards requires that
someone already has SD Remix Lite on their memory card. If you want
to be one of the heroes of SD Remix and distribute SD Remix Lite to
your friends and at events, you will need to transfer the .gci file,
which contains the save file data, to your GameCube memory card.

The main way to do this is via GCMM, a homebrew app that lets you
copy data to and from a GameCube memory card and an SD Card. This
will require you be able to run homebrew apps on your GameCube on Wii.

To install the homebrew channel to your Wii, go to sdremix.com and
go to "Installation" -> "Wii Installation" -> "Homebrew Channel
Installation".

To run homebrew on your GameCube, go to sdremix.com and go to
"Installation" -> "GameCube Installation" -> "Running GCN Homebrew".

To get GCMM and also for instructions on how to use it, visit
http://wiibrew.org/wiki/GCMM


------------
- Features -
------------
- Character balance changes: The main draw of SD Remix is the
  character changes that balance the cast. To see a complete list of
  character changes, go to http://uglook.net/writing/sdremix/#changed
  [by sdremix_troubleshooter, Ripple, Achilles, Dan Salvato, Magus,
      standardtoaster, _glook]
- Taunt Cancelling: If you taunt, you will keep your momentum, allowing
  the taunt to be cancelled by sliding to the edge of a platform.
  [by Dan Salvato]
- Game set to 4-stock, 8 minutes, Friendly Fire and Score Display On.
- A new options menu replaces Tournament Mode!
  [by _glook, Dan Salvato, Achilles, Magus, donny2112]
  From here, you can access various options:
  > Widescreen: Toggles widescreen mode [by Dav Salvato]
  > Options: You can toggle whether to enable or disable gameplay
    options, so that you can be tournament ready. If options are
	disabled, the "Ready to Fight" banner text color at the character
	select screen will be normal colored (yellow). If options are
	enabled, you will be able to access the "Options >" submenu and the
	"Ready to Fight" banner will be blue colored. [by Dan Salvato]
  > Options menu: This menu holds gameplay options that can be toggled
    on and off. They include:
	* Overtime: "Sudden Death" means overtime should behave normally.
	  "Tournament" means that at the end of a match, if players are
	  tied, the ties are broken by displayed percentage. If percentage
	  is still tied, it goes into sudden death, which is a one stock,
	  3 minute match. If still tied, it repeats sudden death.
	  [by _glook]
	* Wall Bracing: If enabled, players will be able to brace against
	  walls if they are hit by non-launching moves while they're on the
	  ground. Bracing is achieved by holding left or right on the
	  control stick when they are hit, similar to crouch cancelling.
	  When you brace a hit, your character's feet leave the ground.
	  This allows for upward DI. Without DI, you can also immediately
	  land afterwards, cutting down stun time against attacks. This is
	  meant to combat wall infinites. [by _glook]
	* Ledge invincibility: If set to "Dynamic", ledge invincibility is
	  treated similarly to shields, in that when you grab the ledge,
	  the amount of invincibility time on your next ledge grab is
	  reduced, but the invincibility time recovers over time, like
	  shields. This is meant to combat infinite ledge stalling.
	  [by _glook]
	* Handicap: If set to "Stock/Crew", the handicap option controls
	  the number of stocks a player has in Stock Mode. If set to
	  "Auto", the handicap for the winner of the last match is
	  automaticaly set to the number of stocks they had left, which
	  makes this ideal for crew battles. Not compatible with team
	  battles. [by Jorgasms]
  > Credits: List of people who contributed to SD Remix Lite
  > Debug menu: This is a pared down version of the SSBM Debug Menu.
- If L+R+A+Start is pressed while loading a stage, it will go to the
  Character Select Screen instead of the main menu.
  [by Jorgasms]
- Salty Runback: Holding A+B at the end of a match will restart that
  match. [by Dan Salvato]
- C-Stick does smash attacks in Single Player [by Zauron]
- Pause camera range significantly increased [by Achilles]
- Portrait colors on the character select screen changed, so SDR Lite
  setups look different [by Shamrock, _glook]
- If no nametag selected, "SDR 3.2 Lite" shows up in the character
  select screen instead of the character name, so people know which
  mod they are playing.
- Stage Striking: At the stage select screen, press X to strike the
  currently highlighted stage, Y to strike all but the random stages,
  and Z to unstrike all stages. [by Dan Salvato]
- If there are four players on Fountain of Dreams, background elements
  are disabled to get rid of lag [by Dan Salvato, _glook]
- Omega Stages: [by _glook, ShamRock]
  At the character select screen, pressing "R" will toggle Omega stages
  and pressing "L" will toggle Alpha stages. When Alpha is toggled,
  the flashing stage border is Red, while Omega displays Purple.
  Alpha stages are the normal stages, just like Normal Melee.
  Omega stages are new or altered stages. The Omega stages are:
  > Omega Icicle Mountain => Snag The Trophies [Achilles]
    This is the "Snag the Trophies" stage from Classic Mode.
  > Omega Peach's Castle [Zauron]
    Switches and bullet bill are removed.
  > Omega Rainbow Cruise => Cranky's Treehouse [Achilles]
    Version of Jungle Japes with no water and no side platforms.
  > Omega Kongo Jungle [Milun]
    The rock, the barrel, the klaptraps and the logs are removed.
  > Omega Jungle Japes [flieskiller]
    Water physics and klaptraps removed
  > Omega Great Bay => Trophy Tussle: Majora's Mask
    This is the Majora's Mask stage from Event Mode.
  > Omega Hyrule Temple => Smash Mount Olympus [Achilles]
    This is an altered version of Snag The Trophies with three
	platforms, grabbable ledges, and no pink platform.
  > Omega Yoshi's Story [Zauron]
    Flyguys removed.
  > Omega Yoshi's Island [Milun]
    Altered stage design based on the left side of the alpha version.
  > Omega Fountain of Dreams [Zauron]
    Platforms and water jets removed.
  > Omega Green Greens [flieskiller, Zauron]
    All bricks removed. Wind and apples disabled.
  > Omega Corneria [Zauron]
    No ships and Great Fox gun destroyed.
  > Omega Venom => Warzone Corneria
    Corneria from Adventure Mode, with Massive Arwing attack
  > Omega Flatzone => Reversed Battlefield [Achilles, _glook]
    Battlefield except with platform heights reversed.
  > Omega Brinstar [Zauron]
    Rising lava disabled.
  > Omega Brinstar Depths [Milun]
    Kraid removed. Rotation disabled.
  > Omega Onett [flieskiller]
    Cars disabled. Drugstore platforms removed.
  > Omega Fourside => Smashville Fourside [Milun]
    Turned into a Melee version of Fourside using the crane.
  > Omega Mute City [flieskiller]
    Cars removed.
  > Omega Big Blue [Milun]
    All cars except for the first are removed.
  > Omega Pokemon Stadium [Zauron]
    No transformations.
  > Omega PokeFloats => Whispy's Battlegrounds [Milun, Achilles]
    Version of Green Greens with no hazards and no gaps.
  > Omega Mushroom Kingdom [Milun]
    Side floors removed. Pulley platforms lower.
	Most of the blocks except for 6 are removed.
  > Omega Mushroom Kingdom 2 [Milun]
    Side floors removed. Middle floor made bigger.
  > Omega Battlefield [Milun]
    Ledges are slightly easier to wall jump and grapple.
  > Omega Final Destination [Achilles, Dan Salvato]
    Background transitions disabled.
  > Omega Dreamland 64 [Zauron]
    Wind disabled
  > Omega Yoshi's Story 64 [Milun]
    Clouds removed. Top platform removed. Side platforms move to
	be at the same height and angle.
  > Omega Kongo Jungle 64 [flieskiller]
    Barrel removed.

-------------------
- Troubleshooting -
-------------------
Issue: The game crashes when I go into the Name Entry screen.
Solution: You likely have the wrong save file for your version of
   SSBM. See the section "SSBM Versions" at this end of this doc
   to see what version of SSBM you have, and make sure the save
   file you have is compatible with this version.

Issue: The game crashes when I try to select or add names from the
   Character Select Screen or try to access the Rumble Options.
Solution: If you have not activated SD Remix Lite, you will
   experience many instabilities. To fix this, activate SD Remix
   Lite first (see the section "How to use SD Remix Lite").


-----------------
- SSBM Versions -
-----------------
There are four versions of Super Smash Brothers Melee that were
released over the years: NTSC 1.00, NTSC 1.01, NTSC 1.02, and PAL.
All three NTSC versions were released in Japan and most of the
Americas. 1.00 was the first version released, and then the other
two versions followed, which introduced bugfixes and some
character changes. This was done silently, but if you live in the
NTSC regions of the world, you can see which version you have by
checking the underside of your disc. Look for "DOL-GALE-0-"
somewhere on the underside of your disc (should be closer to the
center of the disc).
If it says DOL-GALE 0-00, you have NTSC 1.00.
If it says DOL-GALE 0-01, you have NTSC 1.01.
If it says DOL-GALE 0-02, you have NTSC 1.02.
The PAL version was the final version released. It is exclusive
to the PAL regions of the world, which include Europe, Australia,
most of Asia, most of Africa, and parts of South America.