# CyberGarden
Automated control software for my hybrid soil/low pressure aeroponic/air atomized aeroponic garden.

Introduction
------------
I have built a three way hybrid grow system where the top few inches are soil, the bottom of that being wire mesh and burlap. Below this is an aeroponic root chamber. In this chamber I have 2 systems, a low pressure system and a high pressure system. The purpose for this design is to run a nutrient reservoir with a highly active microbial population. This requires both a low pressure system for spraying the biology across the roots without shredding them. The air atomized system is for the main nutrient and oxygen delivery to the root system.

The low pressure system is simply a small submersible pump placed in the nutrient reservoir connected to a hose running to a manifold with cheap plastic screw in sprayer nozzles. The purpose of this system is to spray the microbiology in the reservoir all over the roots. This is intended to be a periodic soaking spray with as full coverage as possible. This is not as effective at nutrient transfer as a high pressure system, but carries more biology, being a dousing, not just a misting.

The high pressure system is where the bulk of the nutrients and oxygen will be delivered from. This is built using a nozzle that takes a pressurized nutrient feed and a 1/4" air line from an air compressor to create a finely atomized spray of nutrients while also carrying fresh oxygen to the root zone.

This requires more precision over the timing than was readily available for a reasonable price. So I started building one with a Raspberry Pi Pico W.

The current prototype is bare bones, but running. Making modifications requires reprogramming the Pico W, which is ridiculous. And thus this project, my Cyber Garden. The goal is to use the Pico W as a very simple web server on 1 core, and run the timers on the other core. I want to be able to check and modify configuration from my phone, since that's what I'll have on me. I want it to be persistent in the event of an outage. Eventually I want to add in a time of day timer and several sensors and relays. So preferably I would be able to add in new ones arbitrarily without having to change the code, just configure a new one and hook up the wire without even turning it off. It also needs to be able to have an offset so I can use solenoids instead of extra pumps and just offset the different grow stations since I plan on having several.

It also gives me a chance to learn some web development and micropython. I haven't really touched html much since the mid-90's when HTML 1.0 first was first coming out. As for python, had read it, never used it, so another new thing to learn.


Key requirements
----------------
GardenEpic1 (Done) Prototype working
	Garden1 (Done) Frame built
  Garden2 (Done) Low pressure pump and nozzles working on a cycle timer
	Garden3 (Done) Air atomizing sprayer turning on as expected
	
GardenEpic2 (relies on GardenEpic1), Adjust timings on my phone to test/tune prototype
	get the pico running as an access point that I can log into with my phone
	get the pico accepting http requests and serving a bare bones web page (learn more HTML later) that gives a UI for changing timings
	add a test mode so debug sessions don't screw with production settings

GardenEpic3 (relies on GardenEpic2), Tune the prototype's timings and pressures
	Air Atomizing Aeroponic nozzle
		get droplet size right
			get water pressure right
			get air pressure right
		get spray duration right
			make sure it fills the root chamber without billowing out the drain
		get frequency right
			don't let the roots dry out
			don't have the roots dripping either
		make sure the nozzle is pointed in a way that fills the root chamber without harming the roots
	Low Pressure Aeroponic nozzles
		make sure the pressure is high enough to reach all nozzles
		make sure the pressure is low enough to not harm the roots
		make sure there's good root coverage with enough nozzles pointed in the right directions
		make sure the pump stays on until the roots are all covered
		when running in a pair as normal, only trigger every 3 hours. But if the AA sysem isn't working, run this at every 10 minutes

GardenEpic4 (relies on GardenEpic2), Refactor and clean up the interface
	file persistence
	load web page from file
	make the interface not look like ass
		proper buttons, arrows, text entry areas
		reset buttons
		disable button (always off)
		always on button
		reset all button
		load changes
		save changes
		clean up the html code
	final refactoring of all code
	
GardenEpic5 (relies on GardenEpic3 and GardenEpic4), Replace the prototype with a new version
	record rebuild for YouTube possibly, see how ambitious I get by this point. Probably depend on growing results
	figure out new correct dimensions (height)
	new chamber for roots that doesn't/can't leak
	proper drain system/sump
	easy way to lift the soil portion to inspect/adjust things
	central reservoirs, veg, flower, and a sprare for experiments/quarantine
	can this be redesigned to use a shared shared nozzle via tubing/solenoid valves, or is the nozzle cheaper, see what the options are
	additional grow stations (initial plan is six stations, further plans for another 4-5)
	each grow station should be able to change between taking a veg or flower nutrient feed and drain to the respective sump
	sump needs to empty to the respective reservoir
	reservoirs should be getting topped up via float valve from dehumidifier water so I don't have to keep emptying it
	
GardenEpic6, Port to Android
	details to be determined
