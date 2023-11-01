(Sept 27th)

Advantage of covering this "legacy" technique; basically introduces us to a broad range of techniques that are used all the way up to 5GHz, but respectively are in a more primitive form, hence easier to understand.

# Mobile network case study: GSM (2G)
What happens on-air?
- Two 25MHz bands - one for uplink (890-915MHz, mobile to base), one for downlink (935-960MHz, base to mobile).
- What does the uplink and downlink frequency separation of 45MHz have to do with the weight of your handset? As we are trying to protect our receiver from our transmitter signals one of things that we can do is we can put a filter on front of our receiver and a filter in front of our transmitter. In case of a transmitter, filter allows our transmitter transmit on intended frequency and suppresses unintended and vice versa re: receiver. Filters are lighter weight when the separation between frequencies is bigger. So effectively, 45MHz ~ implies lighter weight phones. Don't receive and transmit simultaneously, but neighbouring phones/interference exists.
- Frequency Division Multiple Access (`FDMA`): 25MHz band is divided into 124 frequency sub-bands of 200kHz each (plus one guard band)
- Time Division Multiple Access (`TDMA`): on each 200kHz sub-band, there are 8 time slots (bursts). Each burst lasts about 0.577ms and has a length of 156.25bits. A full frame of 8 bursts last then 4.615ms. Idea is to transmit on one, listen on the other - separating the two by some buffer to allow for clear cut separation between transmission and receiving (4 bursts).
- Each burst is allocated to a single user A "channel" in GSM is defined by its frequency and the burst offset in the frame.
- Uplink and downlink channels are separated by 3 other bursts - a mobile never has to transmit and receive simultaneously.
- Theoretical channel bandwidth is just under 34kbps, but overheads are significant! Only 60 bits in each burst carry actual data - the rest is system overhead.
- Frequency hopping may be used to combat multipath and co-channel problems.

[<img src="./gsm-frame.png">](frame screenshot)
