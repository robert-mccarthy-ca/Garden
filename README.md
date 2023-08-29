# Garden Control Software
# Soil/Aeroponic Modular Garden
Automated control software for my hybrid soil/aeroponic garden. Because if you're going to grow indoors in an artifical environment, make it an awesome one. Use an air compressor kind of bonkers
Control interface is via local wifi hotspot and a web site running on a Raspberry Pi Pico W.
Adjustable cycle timers with a toggleable test settings mode

Introduction
------------
I started with building a three way hybrid grow system where the top few inches are soil, the bottom of that being wire mesh and burlap. Below this is an aeroponic root chamber. In this chamber I have 2 systems, a low pressure aeroponic (LPA) system and an air atomized aeroponic (AAA) system. This requires both a low pressure system for spraying the biology across the roots without shredding them and an air atomized system  for the main nutrient and oxygen delivery to the root system. The idea behind this build is to attempt to blend Korean Natural Farming (KNF) techniques with modern hydroponics in both living soil and a living reservoir for maximum growth (aeroponics and nutrient delivery) while maintaining maximum crop quality (microbiological diversity).

This approach required a water pump for the low pressure aeroponic portion, another water pump for reservoir circulation, and an air atomizing nozzle, which in turn requried a water pump and an air compressor. I found a better nozzle however, a waste oil burner nozzle, which siphons the fluid out and has a 2 mm orifice. This removes the need for the water pump for the air atomizing nozzle, and removes the need for the low pressure system altogether, saving 2 pumps.

The soil portion is currently about 6 inches of soil over a wire mesh covered by burlap. This section is for supporting soil biology that does not form in hydroponics, such as mycelial networks for endomycorrhiza root colonization. Additional nutrients specific to a given plant can also be added here while continuing to share a common nutrient reservoir.

The low pressure system was simply a small submersible pump placed in the nutrient reservoir connected to a hose running to a manifold with cheap plastic screw in sprayer nozzles. The purpose of this system was to spray the microbiology in the reservoir all over the roots. This was intended to be a periodic soaking spray with as full coverage as possible. This was not as effective at nutrient transfer as a high pressure system, but carries more biology, being a dousing, not just a misting. This system was to maintain microbial populations and diversity. No longer used due to a better air atomizing nozzle making it obsolete.

The high pressure system is where the bulk of the nutrients and oxygen will be delivered from. This is built using a nozzle that takes an unpressurized nutrient feed and an air line from an air compressor to create a finely atomized spray of nutrients while also carrying fresh oxygen to the root zone. This system is designed to be the primary method of nutrient and oxygen delivery to the roots.

This requires more precision over the timing than was readily available for a reasonable price. So I started building one with a Raspberry Pi Pico W (about $15 delivered to your door). I wanted to use a Raspberry Pi, but there appears to be a world wide shortage of those, thus the Pico W, which with 2 cores and a wifi chip should have the processing I need to run as a web server that I can log into and still control all my devices in my garden. This will start with just getting it working, then getting it working on my phone, then making it pretty, redesigning the build, and then eventually making it an android app and rewrite it in C.

Progress:
--------
GardenEpic1 (Done):
------------------
- The current prototype is bare bones, but running
- Three timers are being used, one each for the solenoid to the air atomizing nozzle, the air atomizing nozzle water pump, and the low pressure aeroponic water pump
- Making modifications requires removing the pico W, reprogramming the Pico W, and reinstalling it in the garden, which is ridiculous, see GardenEpic2
- But it's running and plants can survive in it.

GardenEpic2 (Done):
------------------
- Pico W is now operating as an access point, log in to access the web interface at http://192.168.4.1
- Can now switch to Test Mode which uses different (much shorter) timings
- Adjusting the timings has a bug, needs to be fixed
- Interface looks like ass, need to go learn some basic html forms/input to make that more usable, and probably some CSS to make it look prettier. But it works enough that I can test the sprayer pressures

GardenEpic3 (In Progress):
-------------------------
- Replaced the air atomizing (AA) nozzle with a waste oil burner nozzle which siphons fluid without the need for a water pump
  - removes the need for the LPA system and the water pump to the AA nozzle
- currently not doing a very good job of things, need to tinker more with timings and pressures
  - now getting a spray, just not enough to keep roots happy (lots of them poking out, but none growing any significant distance into the air chamber), need to fix the timer adjustment bug (Garden9)
- timer fixed, now spraying at 43 psi for 3 seconds, will see how that goes
  - noticed that the spray got better further away from the nozzle, may have to redesign the chamber to allow for that
- (June 3, 2023) Had good root growth, but only in a small area in the center with the current setup (Images/Roots_June_3_2023.jpg). I've adjusted the nozzle a few times to get there, this was with the nozzle directly in the center of the root chamber at the bottom pointing up. I've adjusted the pressure to be 20 psi, which looks to be enough with the heduced siphon head to keep a mist. I should probably experiment with using a pressure regulated water pump in combination for the next iteration. Increased the cycle length to 1.6 seconds on and 59 seconds off. Need to make something better for the interface, as the off time changed by 0.1 seconds at a time is ridiculous, time to write something better. I've also adjusted the nozzle to be pointed at the corner without anything planted in it, to bounce back around the rest of the root chamber hopefully. Chamber shape is definitely going to be key on the next build, need to see what density is best first before I can make something better.
- (June 21, 2023) Have had mixed success. Lower pressures seemed to work better, but only at very select ranges. The current design of the root chamber is just bad. New design ready to build, will use a root chamber that is between a sealed inlet and the other end will be for airflow out of the root chamber so all mist has to go through the root area to leave and has far enough to atomize properly, and installing a second sprayer head to increase volume.
- (Aug 28, 2023) Good success finally. Current setup has 2 air atomizing nozzles (2.0 mm orifice) using a 5/16 nutrient feed line running at about 60 psi. Timer is 1 second on out of every 40 seconds. Small pump is attached to the feed line, which although it can spray without it, I've seen a better spray volume when it is running. Downsides include frequent leaks, both from connectors and from the drain itself. Next version must solve both of these issues.

GardenEpic4 (In Progress):
-------------------------
- Removed old timers for LPA and AA water pumps
- Added timer for circulation pump
- added AA water pump back

Key requirements and goals:
--------------------------
- GardenEpic1 (Done) Prototype working
  - Garden1 (Done) Frame built
  - Garden2 (Done) Low pressure pump and nozzles working on a cycle timer
  - Garden3 (Done) Air atomizing sprayer turning on as expected
	
- GardenEpic2 (Done) (relies on GardenEpic1), Adjust timings on my phone to test/tune prototype
  - Garden4 (Done) get the pico running as an access point that I can log into with my phone
  - Garden5 (Done) get the pico accepting http requests and serving a bare bones web page (learn more HTML later) that gives a UI for changing timings
  - Garden6 (Done) add a test mode so debug sessions don't screw with production settings
  - plants are already growing, pretty and maintainable are not priorities, speed is, will rewrite that afterwards

- GardenEpic3 (relies on GardenEpic2), Tune the prototype's timings and pressures
  - Garden7 (Done) replaced the air atomizing nozzle with one that does not require a water pump (waste oil burner nozzle)
  - Air Atomizing Aeroponic nozzle
    - get droplet size right, looking for a fine fog
      - get water pressure right
      - get air pressure right
    - get spray duration right
      - make sure it fully fills the root chamber without billowing out the drain
    - get frequency right
      - don't let the roots dry out
      - don't have the roots dripping either
    - make sure the nozzle is pointed in a way that fills the root chamber without harming the roots
    - make sure the nozzle is at an appropriate distance to get full atomization

- GardenEpic4 (In Progress) (relies on GardenEpic2), Clean up the interface and general refactoring/improving
  - Garden8 (Done) Have the onboard LED assignable to a timer for testing
  - Garden9 (Done) Fix timing bug that blows up when you adjust the timings upwards to the solenoid in test mode
    - CycleTimer now in milliseconds and simply increments to the next index since Python has no rollover limitations like the ESP32 had
    - Can now set individual settings without resetting the timer, allowing for adjusting timings by small increments without a bajillion resets
  - Garden10 (Done) update interface with new timer configuration for solenoid and circulation pump, removing old LPA water pump and AA water pump timers
  - Garden11 (Done) use text inputs instead of submit buttons
  - Garden12 (Done) html is now generated from the classes as needed instead of having a fixed index.html file
  - Garden13 (In Progress) make the interface not look like ass
    - proper buttons, arrows, text entry areas (Done)
    - proper resolution (Done)
    - reset buttons
    - disable button (always off)
    - always on button
    - reset all button
    - load changes
    - save changes
    - clean up the html code
  - file persistence
  - load configuration from file
  - final refactoring of all code
	
- GardenEpic5 (relies on GardenEpic3 and GardenEpic4), Replace the prototype with a new version
  - record rebuild for YouTube possibly, see how ambitious I get by this point. Probably depend on growing results, not worthwhile if I can only show what not to do
  - figure out new correct dimensions (height)
  - new chamber for roots that doesn't/can't leak
  - proper drain system/sump
  - easy way to lift the soil portion to inspect/adjust things
  - central reservoirs, veg, flower, and a spare for experiments/quarantine
  - can this be redesigned to use a shared shared nozzle via tubing/solenoid valves, or is the nozzle cheaper, see what the options are
  - additional grow stations (initial plan is six stations, further plans for another 4-5)
  - each grow station should be able to change between taking a veg or flower nutrient feed and drain to the respective sump
  - sump needs to empty to the respective reservoir
  - reservoirs should be getting topped up via float valve from filtered dehumidifier water so I don't have to keep emptying it (it's already distilled water, just filtering any dust/dirt from the fins)
	
- GardenEpic6, Port to Android
  - details to be determined later
  
- GardenEpic7, Rewrite in C
  - details to be determined later
