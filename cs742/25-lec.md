(11th Oct)

# Continuing with Submarine Cabling
## Repeatered vs. Unrepeatered
- Light in fibre attenuates with distance (between about 0.15 dB/km and 2 dB/km depending on light wavelength and fibre type).
- Can run several hundred km without repeaters - but at a cost in terms of achievable data rate.
- Typical repeatered submarine cables will have repeaters every ~30-150km
    - Optical repeaters are expensive - around NZ$400K+ each, depending on the number of fibres that need repeating. Signal stays optical through the repeater.
        - Long transoceanic cables can have hundreds of repeaters.
    - Repeaters need power: repeatered cables need a low resistance copper conductor to power the repeaters.
        - High DC voltage injected at shore end of cable.
        - Repeaters are connected in series, electrically. Each repeater takes out a few volts (like a voltage divider).

## Design
Design for depth: transoceanic cables typically lie on the seafloor ~5000m down
- Must be waterproof under enormous pressures.
- Must be able to carry own weight of well over 5km of cable on the way down while being lad. E.g. weight of Southern Cross NEXT cable is 4,000kg/km.
    - Most of the cable is steel.
    - Takapuna to Hawaii, first came in late 90s, few Gb/s back then to now carrying Tb/s due to external upgrades on the terminal ends!
        - Terminal equipment has drastic impact on cable performance without needing to change the cable.
- Must be able to withstand conditions there for many years without failure ("15-20-30yrs").

Route needs careful planning
- Avoid anchor zones and bottom trawling grounds (interesting; you can bill the internet company for your anchor if you catch it)
- Avoid submarine hazards like slip-prone slopes, ammunition dumps.
- Cable going through turbulent waters or over coral reefs needs to be protected by pipes.

## Construction
- Cable is placed on ocean floor by specialist cable ship
    - Need for "slack control" when paying out cable (doesn't tangle and doesn't snap)
    - Frequent testing of cable during laying
    - Aim: good build with minimal ship time

### Recovering submarine cables for repair
Up to ~5000m depth, divers operate at 150-200m. Requires heavy process, bringing the cable ship back.

- Cutting
    - By remotely operated vehicle (ROV), or (recent approach)
    - CD: Cutting drive (drag) [more traditional approach], "kinda a fishing line, end of steel cable has a sickle, under the cable, instrument latches, mechanical contraption cuts", positioning via time delay optometry, broken region reflects light.

- Recovery
    - HD: Holding drive (drag), "bring cut cable up, for disposable, splice new cable onto it, lay it"

#### Scenario detailed
1. Cut cable at or near the damage site with ROV
    - CD will be used in low visibility
2. Recover each cable end with a HD around 2km away from cut
    - First recovered cable end is inspected, sealed and tied to a buoy
3. Splice second cable end to a spare piece of cable
    - This is needed as the cable ends will be some distance apart at the surface
4. Return to the first buoy and splice the spare piece to cable end there
5. Lower cable into a loop on the seafloor to prevent messy tangles

Total: 2 HD's and at most one CD.

### Issue: How come a cable piece ended up closer to Hunga than before?
- Likely caused by a turbidity current from a location other than Hunga
    - Precedents for cable damage from these date back to the Grand Banks EQ in 1929

- Submarine landslide
    - Slopes possible charged by as from Hunga
    - Significant amounts of seismicity
    - Possibly more than one event

- Fits with the late failure of the international cable
