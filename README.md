# Soil/Aeroponic Garden Automation

Introduction
------------
I started this project to automate my indoor garden, which is pretty much a hard requirement if you want to grow plants using air atomized aeroponics (AAA), which was my goal. This software runs on a Raspberry Pi Pico W, a small microcontroller that at the time of writing is about $15 CAD. I was initially going to use a Raspberry Pi to run everything, but it turns out that a microcontroller is more than enough computing power to get the job done ... and it was actually in stock. The garden itself is a hybrid soil and aeroponic system. This is to maximize the plants exposure to beneficial microbiology, not all of which like to live in a reservoir without soil.
The currently finishing run is using Version 1, with Version 2's design and code underway.

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
    - 2 x AAA (2.0 mm) nozzles
- air compressor
- air pump

Software Requirements:
- To handle the cycle timers for the solenoids and pumps
- Be configurable from my phone

Files:
- webServerAccessPoint.py (rename to main.py to run live)
- cycleTimer.py

Version 2
---------
- grow tent (4' x 8')
  - 2 x 8" exhaust carbon filter and fan
  - grow chamber
    - wooden box with 3 chambers running lengthwise
	- each chamber has its own sump system that can be directed to drain into either reservoir
	- chamber 1
	  - 4 x 1020 trays lengthwise
	  - 1 x AAA sprayer (2.0 mm) that can be fed from either reservoir
	- chamber 2
      - 4 x 1020 trays crosswise centered on 2' intervals measured against the tent
	  - 2 x AAA sprayers (2.0 mm) that can be fed from either reservoir
	- chamber 3
	  - 4 x 1020 trays lengthwise
	  - 1 x AAA sprayer (2.0 mm) that can be fed from either reservoir
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

Software Requirements:
- To handle the cycle timers for the solenoids and pumps
- Be configurable from my phone
- configuration persistence through power cycle
- handle hot-expansion, adding new hardware without resetting the device
- handle test switches (turn on while pressed without impacting the underlying control)
- handle daily timers for the lighting/cooling
- add thermostats
- add data logging, temperature and humidity to start, pH and EC eventually as well
- allow for multiple controls on the same pin (for example, a fan control that needs to start exhausting at full speed 5 minutes before the lights go off to prevent condensation, but also need to turn on when the temperature is high enough or when I press the test button))

Files:
- gardenController.py (rename to main.py to run live)
- targets.py
- controls.py
- timers.py
- config.json

Growing methodology:
- no pesticides or any other form of biocide
- reuse the soil, ammending with organic amendments
- nutrient reservoir is synthetic nutrients, RAW from NPK Industries, a dry nutrient line that I've been very happy with
- microbes in both the soil and the reservoir (LAB, JMS, IMO, worm castings)
  - worm castings added to a strainer bag hanging in the reservoir (about a cup once a week)
  - LAB in the reservoir (1:500) and foliarly (1:1000)
  - JMS as a foliar spray or soil drench only, not in the reservoir (1:20)
  - liquid IMO as foliar
  - solid IMO as soil inocculant or added to the strainer bag with the worm castings
- low pressure aeroponic sprayers 1 minute on, 59 minutes off
- air atomized aeroponic sprayers 2 seconds on 58 seconds off

The idea behind this was to grow as organically as possible, inspired by KNF and JADAM farming practices, but still utilizing the technological gains of hydroponics. The eventual goal is to ferment my own organic nutrients in either LAB or IMO instead of having a synthetic line, but that's a project down the road, no time for it just yet.
