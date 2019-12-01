# [v0.3.0](https://github.com/Deuchnord/kosmorro/compare/v0.2.3...v0.3.0) (2019-12-01)


### Bug Fixes

* **position:** remove useless altitude argument ([d079fc7](https://github.com/Deuchnord/kosmorro/commit/d079fc7b201c7f5855c05acc80955e3b16c4ef6d))
* **terminology:** use the "Object" term ([e21f632](https://github.com/Deuchnord/kosmorro/commit/e21f6327f4dc7e5a9d46ccd6ca493207064745f8))


### Features

* **moon-phase:** compute more accurate Moon phase ([6856d45](https://github.com/Deuchnord/kosmorro/commit/6856d456439215c7a63432e76318e231fc17870d))


### Performance Improvements

* **position:** enhance the position performing ([61536da](https://github.com/Deuchnord/kosmorro/commit/61536da9df4e742e9f7046fb177ecd09fb711b38))


### BREAKING CHANGES

* **position:** invoking kosmorro command with the --altitude argument
will now fail with an "unrecognized arguments" error.
* **moon-phase:** JSON format now returns the moon phase as an object
instead of a string



# [v0.2.3](https://github.com/Deuchnord/kosmorro/compare/v0.2.2...v0.2.3) (2019-11-24)


### Bug Fixes

* **dumper:** display the right date on output text ([2511d31](https://github.com/Deuchnord/kosmorro/commit/2511d31c37dc5bbb790ebeabc7c230e8641b1448))



# [v0.2.2](https://github.com/Deuchnord/kosmorro/compare/v0.2.1...v0.2.2) (2019-11-18)


### Bug Fixes

* set times are now correct ([82bdc70](https://github.com/Deuchnord/kosmorro/commit/82bdc7055b903bcd586e69374ba93f843ae95ceb))


### Features

* add argument to get the current version ([5f74b08](https://github.com/Deuchnord/kosmorro/commit/5f74b08d15bbccededfc5a195b6943c408c93d16))

# [v0.2.1](https://github.com/Deuchnord/kosmorro/compare/v0.2.0...v0.2.1) (2019-11-17)


### Bug Fixes

* Move version constant to its own file to prevent sgp4 module failing in the AUR ([9a0c9d3](https://github.com/Deuchnord/kosmorro/commit/9a0c9d3ae34c5fa561b5a1b252d39a5ef2a0a4b9))

# [v0.2.0](https://github.com/Deuchnord/kosmorro/compare/v0.1.0...v0.2.0) (2019-11-17)

### Added

- Add JSON output
- Add argument to clear the cache

### Changed

- Update Numpy to v1.17.4
- Update PyLint to v2.4.4

# v0.1.0 (2019-11-10)

- First version
