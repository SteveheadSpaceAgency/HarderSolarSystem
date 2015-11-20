# Harder Solar System
A set of Kopernicus configs that make the stock solar system more challenging. Comes in several size scales: 1x (stock), 2x, 3x, 4x. Also comes with a generic config that supports 64K and can potentially support other stock-like systems.

## Changes to Stock
* The orbits of planets/moons are inclined to simulate a 23.4° axial tilt for Kerbin, similar to how Real Solar System does it.
* KSC moved to a new location that has a latitude of 28.608389° N.
* Mun's inclination changed to 5.145° relative to Kerbin's orbit, like how the real Moon is. No more lunar/solar eclipses every Mun orbit.
* Minmus's inclination changed to 0.5° relative to Kerbin's orbit. Changed so that it's inclination is not too similar to Mun's.
* Rotation periods are adjusted based on scale.
* Jool's mass has been increased to more real life comparable levels, relative to scale. This does not affect the 1:2:4 resonance of its inner moons.
* Dres and Eeloo have had their inclinations increased relative to the ecliptic to roughly match Ceres and Pluto, respectively.
* High space altitude science threshold scales properly with scale choice.
* Note: Potato moons do not scale with the various scales to retain their intended shape.

## Outer Planets Mod Compatibility
* Same as above regarding orbits for most. For now, Sarnus's inner moons retain the original orbit relative to Sarnus's equator/rings, which looks better. Same applies to Urlum and its two inner moons.
* Like Jool, the gas giants have had their masses increased.
* Instead of Eeloo, Plock's inclination increased to better match Pluto's.
* Same situation with the potato moons as above.

## Remote Tech Compatibility
* Mission Control ground station is moved to the new KSC location.
* Added three Deep Space Network ground stations.
* Added two short range stations to assist with launches.
* Antennas and ground stations all scale with the varied scales available.

## 64K Support (Generic Config)
* The generic config that was designed with 64K in mind only changes the inclinations and Jool's mass. No changes to the KSC location nor any Remote Tech changes have been made to what 64K offers. Rotation periods remain same as 64K.
* It is recommended to use the higher latitude space centers in 64K (requires KSCSwitcher) for the extra difficulty.
* This generic config should work with most other stock solar system rescales.

### License
Public domain.

#### Thanks
* Thanks to Paul Kingtiger for inspiration on several parts of this. Also, some compatibility came straight from KScale2.
* Thanks to NathanKell's RSS for inspiring the axial tilt simulation.

### Changelog
* **v1.2.0** - 11/20/15 - Generic config added that supports 64K and should support most other stock-like solar systems by default. For OPM users, Urlum's inner moons now aligned with rings like Sarnus's inner moons and fixes for science altitude errors and rings.
* **v1.1.1** - 11/17/15 - Fix .version files for each scale. No change to configs.
* **v1.1.0** - 11/13/15 - Increased gas giant masses. Increased inclinations for the "dwarf planets". High space science altitude threshold scales based on selected scale. Fixed runway orientation to be due East/West. Fixed Eeloo not scaling in OPM.
* **v1.0.1** - 10/31/15 - Small fix for scaling a RT ground station antenna properly.
* **v1.0.0** - 10/30/15 - Initial release.
