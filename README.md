# Soil/Aeroponic Garden Automation

Introduction
------------
I started this project to automate my indoor garden, which is pretty much a hard requirement if you want to grow plants using air atomized aeroponics (AAA), which was my goal. This software runs on a Raspberry Pi Pico W, a small microcontroller that at the time of writing is about $15 CAD. I was initially going to use a Raspberry Pi to run everything, but it turns out that a microcontroller is more than enough computing power to get the job done ... and it was actually in stock. The garden itself is a hybrid soil and aeroponic system. This is to maximize the plants exposure to beneficial microbiology, not all of which like to live in a reservoir without soil.

Version 1
---------
- grow tent (4' x 8')
  - 1 x 8" exhaust carbon filter and fan
  - reservoir
    - circulation pump
    - water pump for nutrient line to AAA nozzles
    - air stone
  - grow chamber
    - hollow wooden box above a nutrient reservoir
	- a soil planter box with a mesh bottom for the roots to grow down through sits on top of that
    - 2 x AAA nozzles
- air compressor
- air pump

With this version, the software only had to run the timers for the pumps and solenoid and be configurable from my phone. This was set up as a wifi access point on the Pico W that I would connect to. Persistence was not included.

Files:
webServerAccessPoint.py (rename to main.py to run live)
cycleTimer.py

Version 2
---------
- grow tent (4' x 8')
  - 2 x 8" exhaust carbon filter and fan
  - grow chamber
    - wooden box with 3 chambers running lengthwise
	- each chamber has its own sump system that can be directed to drain into either reservoir
	- chamber 1
	  - 4 x 1020 trays lengthwise
	  - 1 x AAA sprayer that can be fed from either reservoir
	- chamber 2
      - 4 x 1020 trays crosswise centered on 2' intervals measured against the tent
	  - 2 x AAA sprayers that can be fed from either reservoir
	- chamber 3
	  - 4 x 1020 trays lengthwise
	  - 1 x AAA sprayer that can be fed from either reservoir
	- low pressure sprayers
- 2 x nutrient reservoirs
  - 100L capacity (plastic garbage pail on wheels with a lid)
  - vegetative or flower nutrients as appropriate
  - lines feed AAA sprayers and return nutrients from the sumps
  - circulation pump
  - 2 x air stone
- 1 x water reservoir
  - 100L capacity (plastic garbage pail on wheels with a lid)
  - tap water or reverse osmosis as available
  - automatic top off to the 2 reservoirs
- air compressor
- air pump

Files:
gardenController.py (rename to main.py to run live)
targets.py
controls.py
timers.py

Version 1 (Done) was in a 4' x 8' grow tent, with an 8" carbon filtered exhaust fan (24/7), a fan inside for air movement (24/7), and approximately 1100 W of LED grow lights (either 18 hours on, 6 hours off or 12 and 12 depending on growth stage). The grow system itself consisted of an elevated hollow box made of wood and draining into a reservoir. Above this root chamber was a soil planter approximately 6" deep with a steel mesh and burlap to allow the roots to grow down into the hollow root chamber before draining into the reservoir. The reservoir had air stones running to keep it oxygenated. Nutrients were supplied by 2 siphoning air atomizing nozzles powered by water pumps and an air compressor (5/16" water line, 1/4" NPT air connection, 2.0 mm orifice). I had made attempts at adding a low pressure aeroponic system to it as well but ended up sticking with just the air atomizing nozzle for the first attempt. The operational requirements for version 1 of the software were to control the timers for the pumps and solenoid, and be configurable from my phone.

Version 2 (In Progress) will be in the same 4' x 8' grow tent with the same lighting. The goal is to have two carbon filtered fans this time, as one just couldn't dump the humidity and heat fast enough, I was seeing temperatures above 32 C at times under the canopy. These will be controlled by a thermostat with the aim of maintaining the ideal temperatures a bit more consistently. I will also be adding more fans for circulation, but those need not be on a timer, those can run 24/7. The growth chamber will once again be built from wood and sealed from moisture due to having the tools to work with wood (probably be better to build it from something that cannot rot). This version will have three parallel channels running lengthwise down the tent instead of just one chamber, draining to three separate sumps. These sumps will have a float vale triggered water pump to pump back to either reservoir, configurable by channel as well as air stones to keep them oxygenated. The water reservoir will automatically top off the two main reservoirs giving me a bit longer of a buffer before I need to deal with the garden and letting me see how fast my plants are using nutrients. Unlike the first version, this one will also have low pressure nozzles. The difference here is droplet size, with the low pressure system being vastly larger. I intend to use this on an hourly cycle with the AAA nozzle being what feeds tha plants the rest of the time. I found that the roots could get a little dry on the first run, so making sure that everything can get as much water as it wants and get a solid coating of biology from the reservoir. These sprayers are going to be made of pvc pipe with screw in plastic sprayer heads. They will draw from whichever reservoir is required like everything else. They will be located on the sides for chambers 1 and 3. Chamber 2 will have the sides as well as inter-plant sprayers running crossways. The goal of this design is to have 1 of the smaller chambers for a crop that feeds solely on vegetative nutrients such as greens, with the other smaller chamber being a flowering nutrient such as an everbearing strawberry. The middle chamber will be for my larger plants (4 of them) that can use either reservoir as needed.

Growing methodology:
The idea behind this build was inspired by Korean Natural Farming (KNF) and JADAM techniques which I wanted to blend with modern hydroponics in both living soil and a living reservoir for maximum growth (aeroponics for maximum oxygen and nutrient delivery) while maintaining maximum crop quality (microbiological diversity in the soil). No pesticides, herbicides or any other biocide will be used, just clean crops. This system relies heavily on microbes, specifically I use worm castings as a steeped bag in the reservoir along with LAB from KNF. As I have it available, I will also be adding IMO (Indigenous microgorganisms, an aerobic cultivation of soil microbiology) and JMS (Jadam microbiology solution, an anaerobic culturing of soil microbiology). 
The nutrients are synthetic, RAW a dry nutrient line from NPK Industries.  I run a living reservoir, one that does not get sterilized or dumped on a regular basis. I add 1:500 LAB when adding water/nutrients, and add about a cup of worm castings in a paint strainer bag to the reservoir to steep once a week. Periodically I will dump a few liters of nutrient to ensure no major buildups occur, but the main culture is kept and added to with fresh nutrients/water as applicable. I try not to let my reservoir go below 40% as I've found it begins to have pH issues below that point. The nutrients will be delivered as a fine mist from the AAA (Air atomized Aeroponic) nozzles for about 2 seconds once a minute and from the low pressure sprayers for about one minute once an hour to make sure there's ample opportunity for thirsty plants to drink as much as they like.
The soil portion above will be in a sturdy 1020 tray (I'll be using the deep mesh ones from Bootstrap Farmer) filled with soil, below which is the root chamber.
