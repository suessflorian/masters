(21st Sept)
Re-motivates this idea of spherical spreading (path loss).

# Receivers
1. The carrier frequency they operate on (measured in Hz). This must match that of the transmitter.
2. Bandwidth that they receive (around the receive frequency).
3. Their sensitivity. For good receivers, this is determined by bandwidth and noise floor (which in turn is a function of frequency and temperature). The sensitivity is the minimum signal (typically quoted in dBm) that the receiver requires in order to recover the transmitted information with acceptable quality.
4. The modulation scheme that the receiver can demodulate.
5. ... few other characteristics.

## Detrimental effects in radio communication
1. Noise
2. Interference
3. Fading

Will explore each of these.

## Noise
- Noise is a very important aspect in radio communication
- Noise is primarily caused by fact that electronic components **in the receiver** are not at absolute zero temperature: atoms wiggle around a bit and knock electrons out of their orbits generating small random voltages.
- Thermal noise is uncorrelated. That is, even if we know the noise voltage across a component at a particular moment, we cannot predict the voltage at a future point in time.
- However, we can make statements about the average noise voltage and/or power. The higher the temperature, the higher the noise!
- Average noise power P, at receiver in a (kelvin) T degrees environment is: P = kT delta f. `k` is the Boltzmann constant (k = 1.38*10^-23 J/K (joules per kelvin)) and delta f is the bandwidth of the receiver.
- Interfering signals are often thrown in with "noise" but this is strictly speaking not valid as they behave differently, e.g., they may not be uncorrelated.

## Interference
- Interference is also a very important aspect in radio communication.
- Interference is generally injected into the signal path at the receiver's antenna (one might say it originates **in the channel**)
- Interference can be caused  by artificial and by natural sources.
- Artificial sources of interference may include: anything that causes sparks (electric motors, ignitions, switching gear) or other electronic equipment that operates or switches at similar frequencies as your communications application. Interference may be deliberate.
- Example: A badly-shielded computer (that switches its bus lines on and off millions of times a second) interferes with a radio receiver.
- Example: A microwave over that shares the 2.45GHz band with Bluetooth and 802.11 WiFi affects a wireless office network
- Example: Soviet government jamming transmitters make reception of the BBC and other Western radio stations difficult during the Cold War.
- Natural sources of interference can include: Lightning and other static discharges.

## Fading
- Actually a kinda of "self-interference": signal from transmitter arrives at the receiver by more than one path and partially cancels out
- Multiple paths can be caused by reflection and/or refraction of the signal
- Paths may vary over time as atmospheric conditions change or receiver, transmitter, or reflecting object(s) move
- Very common problem especially in mobile communication in urban areas!

# Shannon-Hartley Capacity Theorem
Minimum signal to noise ratio needed if we want to communicate with a given capacity and bandwidth. Capacity here is a theoretical upper limit of the bitrate through this communication pathway.

- Remember that for received signal power S and noise power N, we get capacity C in bandwidth B.
```
C = B log_2(S+N / N)
```
- If we want to communicate in bandwidth B with a certain rate `R <= C`, this means that we need a certain minimum SNR:
```
S + N / N >= 2^(R/B)
```

- Note: the practical modulation schemes do not achieve equality here.

# Link Budgets
Link budgets basically tell us, whether a communication that we're intending to happen can work. In a link budget, we try to model our communication to see whether it will succeed with the combination of components we have chosen. We look at our signal level at each stage and see whether the signal level at the receiver exceeds the given _noise_ floor. The example here is for an 802.11b WiFi link (example only & without looking at coding gain!)
