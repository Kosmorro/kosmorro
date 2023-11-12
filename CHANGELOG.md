# [Version 0.10.12](https://github.com/Kosmorro/kosmorro/compare/v0.10.11...v0.10.12) (2023-05-24)


### Bug Fixes

* support Python 3.11 ([#316](https://github.com/Kosmorro/kosmorro/issues/316)) ([209aab0](https://github.com/Kosmorro/kosmorro/commit/209aab06e48a75b3161f337b0d0f56b6a63ce97f))



# [Version 0.10.11](https://github.com/Kosmorro/kosmorro/compare/v0.10.10...v0.10.11) (2022-11-11)


### Bug Fixes

* fix localization for Earth and apsis ([#275](https://github.com/Kosmorro/kosmorro/issues/275)) ([1f1118c](https://github.com/Kosmorro/kosmorro/commit/1f1118cf3e003c773a429f3d5d593960368a50e1))


### Build System

* add support for Python 3.11 ([#295](https://github.com/Kosmorro/kosmorro/issues/295)) ([08da307](https://github.com/Kosmorro/kosmorro/commit/08da3072f57add8c40b52a4fd45291b1c9216b8a))
* remove AppImage ([#294](https://github.com/Kosmorro/kosmorro/issues/294)) ([3bf4ed7](https://github.com/Kosmorro/kosmorro/commit/3bf4ed737c3278173dabb47324d9993e87141741))


### BREAKING CHANGES

* Python 3.7 is not supported anymore
* AppImage is no longer available. This decision has been made because it has become hard to maintain lately, and I don't have time nor motivation to fix it.



# [Version 0.10.10](https://github.com/Kosmorro/kosmorro/compare/v0.10.9...v0.10.10) (2022-03-20)


### Bug Fixes

* use Babel to translate the dates ([9268113](https://github.com/Kosmorro/kosmorro/commit/92681131062eb0a93e901a5598353e36d9fc590f))
* **events:** ignore unsupported event types ([9bfa8f5](https://github.com/Kosmorro/kosmorro/commit/9bfa8f503d4b46f91777d0b99fbc84f2a116a340))


### Features

* **i18n:** delete pseudo-translation ([b2535ab](https://github.com/Kosmorro/kosmorro/commit/b2535abd4aa03e700e5e482f8c5cf7af050eac29))


### BREAKING CHANGES

* Docker support has been removed.
  If you were using it, please migrate to [one of the other available options](https://kosmorro.space/cli/download/).



# [Version 0.10.9](https://github.com/Kosmorro/kosmorro/compare/v0.10.7...v0.10.9) (2022-01-12)


### Bug Fixes

* fix distribution on PyPI



# [Version 0.10.8](https://github.com/Kosmorro/kosmorro/compare/v0.10.7...v0.10.8) (2022-01-10)


### Bug Fixes

* fix locale support that led to an exception ([38571c3](https://github.com/Kosmorro/kosmorro/commit/38571c3084edfec6cafeac16755dde2cd6c5ee66))



# [Version 0.10.7](https://github.com/Kosmorro/kosmorro/compare/v0.10.6...v0.10.7) (2021-12-04)


### Bug Fixes

* return next Moon phase with the correct time zone ([1cc8913](https://github.com/Kosmorro/kosmorro/commit/1cc891395e2081d431d63a4d4be303a8121c2daa))



# [Version 0.10.6](https://github.com/Kosmorro/kosmorro/compare/v0.10.5...v0.10.6) (2021-11-20)


### Bug Fixes

* **colors:** use colors adapted on both dark and light background ([9bdb490](https://github.com/Kosmorro/kosmorro/commit/9bdb490435a4ca9741911396a28fa6bbdb47159b))
* **events:** fix event details display for maximal elongation ([d73f74a](https://github.com/Kosmorro/kosmorro/commit/d73f74a34cc21ff8b092d65f77aacf66529ab8bb))



# [Version 0.10.5](https://github.com/Kosmorro/kosmorro/compare/v0.10.4...v0.10.5) (2021-11-09)


### Bug Fixes

* fix a display issue on the events list when Kosmorrolib returns events not supported by the CLI ([e82af8f](https://github.com/Kosmorro/kosmorro/commit/e82af8f4b9d3a1511876718ff99d5bcc6dce9067))
* fix KeyError on events processing ([be6bf53](https://github.com/Kosmorro/kosmorro/commit/be6bf530b7c57e9a54da09c86bcca7bfcbadf595))



# [Version 0.10.4](https://github.com/Kosmorro/kosmorro/compare/v0.10.3...v0.10.4) (2021-11-01)

This version is empty and contains exactly the same things as v0.10.3.
It has been created because of a manipulation mistake that led to the creation of a wrong version on PyPI.

If v0.10.3 does not exist on your distribution, install v0.10.4, and you will have exactly the same thing.

# [Version 0.10.3](https://github.com/Kosmorro/kosmorro/compare/v0.10.2...v0.10.3) (2021-11-01)


### Bug Fixes

* update Kosmorrolib to version 1.0.1 ([#207](https://github.com/Kosmorro/kosmorro/issues/207)) ([b492e7f](https://github.com/Kosmorro/kosmorro/commit/b492e7f946c3452de3f09a36d40f458947f8f6e9))
**Note:** if you were using Kosmorro < 0.10.3, files were automatically downloaded. Those files are not necessary anymore, so you can delete the folder `$HOME/.kosmorro-cache`


# [Version 0.10.2](https://github.com/Kosmorro/kosmorro/compare/v0.10.1...v0.10.2) (2021-08-26)


### Bug Fixes

* NoneType error on JSON output without position ([#199](https://github.com/Kosmorro/kosmorro/issues/199)) ([6988e77](https://github.com/Kosmorro/kosmorro/commit/6988e77838c31ce4bf2fcff9da8e13b21cd5b494))



# [Version 0.10.1](https://github.com/Kosmorro/kosmorro/compare/v0.10.0...v0.10.1) (2021-06-20)


### Bug Fixes

* enhance forward compatibility with Kosmorrolib ([#189](https://github.com/Kosmorro/kosmorro/issues/189)) ([1fe90d2](https://github.com/Kosmorro/kosmorro/commit/1fe90d2603edbe68d7a119a0a7fb3649b55abe68))
* **PDF export:** fix the failure on PDF saving ([#186](https://github.com/Kosmorro/kosmorro/issues/186)) ([8d71b61](https://github.com/Kosmorro/kosmorro/commit/8d71b611e036c7cbb39683054dd6485c774076f7))



# [Version 0.10.0](https://github.com/Kosmorro/kosmorro/compare/v0.9.0...v0.10.0) (2021-05-30)


### Bug Fixes

* fix English messages ([#178](https://github.com/Kosmorro/kosmorro/issues/178)) ([6661984](https://github.com/Kosmorro/kosmorro/commit/666198497398700f0a9540ba5cf7448895e29e75))


### Features

* add official Docker image ([#137](https://github.com/Kosmorro/kosmorro/issues/137)) ([a6d3575](https://github.com/Kosmorro/kosmorro/commit/a6d3575977046003d27c03f82e4635c36f7f34e7))
* use Kosmorrolib ([#162](https://github.com/Kosmorro/kosmorro/issues/162)) ([87206d7](https://github.com/Kosmorro/kosmorro/commit/87206d706893fef714e955cf6047483bc815a327))



# [Version 0.9.0](https://github.com/Kosmorro/kosmorro/compare/v0.8.1...v0.9.0) (2021-01-31)


### Code Refactoring

* use `enum` instead of `dict`s for the events and moon phase ([#129](https://github.com/Kosmorro/kosmorro/issues/129)) ([8b723bf](https://github.com/Kosmorro/kosmorro/commit/8b723bfd221dbcddae1717c5e1211a99d828b67e))


### Continuous Integration

* **compatibility:** add support for Python 3.9 ([#131](https://github.com/Kosmorro/kosmorro/issues/131)) ([0b12e71](https://github.com/Kosmorro/kosmorro/commit/0b12e71da8ba5ef9079a86a5eb401ae3f32beba2))


### Features

* **event:** add support for moon apogee and perigee ([331ab99](https://github.com/Kosmorro/kosmorro/commit/331ab99aa1c3647a45eb05c6850241ebb205fdfb))


### BREAKING CHANGES

* **compatibility:** on Ubuntu 20.04+, the `texlive-latex-extra` package is needed to generate the PDF output
* **kosmorrolib:** some methods in `Event` and `MoonPhase` classes have been dropped in favor of `enum.Enum`'s `name` and `value` properties.



# [Version 0.8.1](https://github.com/Deuchnord/kosmorro/compare/v0.8.0...v0.8.1) (2020-06-07)


### Bug Fixes

* avoid returning ephemerides for yesterday or tomorrow ([75eba49](https://github.com/Deuchnord/kosmorro/commit/75eba4977c7ea928e76a99710041f01c2f500972))
* handle out of range date error ([c39cd3a](https://github.com/Deuchnord/kosmorro/commit/c39cd3aefa263eef9d2a4f42717e0eb05d3e0920))



# [Version 0.8.0](https://github.com/Deuchnord/kosmorro/compare/v0.7.0...v0.8.0) (2020-05-22)


### Code Refactoring

* simplify ephemerides, remove dead code ([6618712](https://github.com/Deuchnord/kosmorro/commit/6618712030432d992f957f34e522b792ee74ecc0))


### Features

* add support for relative dates on --date argument ([b9454be](https://github.com/Deuchnord/kosmorro/commit/b9454be45941ce2b271959f9873692516c555c88)) (thanks @Brainface1!)
* display a graph in the PDF output for the ephemerides ([4ea148e](https://github.com/Deuchnord/kosmorro/commit/4ea148e8d1a31ad6d369ace1b5bdaa9b0440be3b))


### BREAKING CHANGES

* the JSON format has deeply changed to enhance its consistency



# [Version 0.7.0](https://github.com/Deuchnord/kosmorro/compare/v0.6.2...v0.7.0) (2020-04-05)


### Features

* add support for environment variables ([5dec0dc](https://github.com/Deuchnord/kosmorro/commit/5dec0dcc4cb3483ee4962a4ae7e86135e4bded06))
* add support for Moon conjunctions ([c063f6e](https://github.com/Deuchnord/kosmorro/commit/c063f6e0f50e0c11c0e77c9fe16dedef0133a9af))
* add support for occultations ([b8d6ae2](https://github.com/Deuchnord/kosmorro/commit/b8d6ae2f510b384ecbc0a960bea764e96ec656a0))
* move the date to a single argument ([32489ae](https://github.com/Deuchnord/kosmorro/commit/32489ae355bba4facb6202eed929dfe4639cb632))


### BREAKING CHANGES

* the --day, --month and --year arguments have been removed in the
favor of a single one.



# [Version 0.6.2](https://github.com/Deuchnord/kosmorro/compare/v0.6.1...v0.6.2) (2020-03-19)


### Bug Fixes

* remove Mercury and Venus opposition ([1b4c499](https://github.com/Deuchnord/kosmorro/commit/1b4c4991274503663ace52c02fd46a19bef6b718))



# [Version 0.6.1](https://github.com/Deuchnord/kosmorro/compare/v0.6.0...v0.6.1) (2020-03-08)


### Bug Fixes

* **events:** prevent false detection of conjunctions ([c7bc757](https://github.com/Deuchnord/kosmorro/commit/c7bc7574df1b0469aad1226887495ce013b615f1))
* handle KeyboardInterrupt exception ([a7cb46e](https://github.com/Deuchnord/kosmorro/commit/a7cb46e857e2ca8e55c61fba522b911fcabdc86c))
* remove the "timezone" word in the PDF output’s introduction ([5ec56c4](https://github.com/Deuchnord/kosmorro/commit/5ec56c40b1ad80c81a7f5c4e1f63d099403f0a5d))



# [Version 0.6.0](https://github.com/Deuchnord/kosmorro/compare/v0.5.2...v0.6.0) (2020-03-01)


### Features

* add ability to save PDF file ([2fadc2a](https://github.com/Deuchnord/kosmorro/commit/2fadc2a95ebd7b8e72633d4a7209a08bcb0dfebc))
* add support for maximal elongations of Mercury and Venus ([9dbc093](https://github.com/Deuchnord/kosmorro/commit/9dbc09363134f6b4647d07cb54aea387e1a36fab))
* add support for timezones ([d7730bd](https://github.com/Deuchnord/kosmorro/commit/d7730bd2ad5e1bd0d28de759c674e0c799c0bb06))



# [Version 0.5.2](https://github.com/Deuchnord/kosmorro/compare/v0.5.1...v0.5.2) (2020-02-04)


### Bug Fixes

* add missing dependency for PIP ([906a592](https://github.com/Deuchnord/kosmorro/commit/906a5924a2cbdca71da793b355880571072aa81c))



# [Version 0.5.1](https://github.com/Deuchnord/kosmorro/compare/v0.5.0...v0.5.1) (2020-02-03)


### Bug Fixes

* add compatibility for Skyfield 1.17 ([081aab1](https://github.com/Deuchnord/kosmorro/commit/081aab129e8245e795e569f38f139285a697777a))



# [Version 0.5.0](https://github.com/Deuchnord/kosmorro/compare/v0.4.0...v0.5.0) (2020-01-26)


### Features

* add colors in the text return ([38fc066](https://github.com/Deuchnord/kosmorro/commit/38fc06657fb7452e35e81e61fb2b8990bf341f72))
* **i18n:** make the strings translatable ([c4f07a1](https://github.com/Deuchnord/kosmorro/commit/c4f07a1d647a6829bdc1ed7afe85462093203ef7))
    * Kosmorro is now available in French and German!



# [Version 0.4.0](https://github.com/Deuchnord/kosmorro/compare/v0.3.1...v0.4.0) (2019-12-28)


### Features

* **events:** add support for conjunctions ([8d60a2a](https://github.com/Deuchnord/kosmorro/commit/8d60a2ad9925a9bd10f070e5df8d5f18cdd0f81b))
* rename fields in the JSON response for more coherence ([4029ba9](https://github.com/Deuchnord/kosmorro/commit/4029ba9ec208214d24070f99be06bc88d7923210))
* **ephemerides:** compute ephemerides if the position is set only ([467c822](https://github.com/Deuchnord/kosmorro/commit/467c8227df0460785a2ade87de6a07f4c0ba0fc9))
* **events:** add support for opposition events ([fa2da9e](https://github.com/Deuchnord/kosmorro/commit/fa2da9e4a9468b4f8ad0fa2b2184fa93c5513fbe))


### BREAKING CHANGES

* the fields "details" and "ephemerides" have been switched.
* **ephemerides:** invoking kosmorro command without --latitude and
--longitude arguments will now only output the Moon phase and,
eventually, the events for the given date (or today if date not given).



# [Version 0.3.1](https://github.com/Deuchnord/kosmorro/compare/v0.3.0...v0.3.1) (2019-12-01)


### Bug Fixes

* **moonphase:** fix the Moon phase prediction ([d715746](https://github.com/Deuchnord/kosmorro/commit/d7157466d90c7596a35dce63088b6aacb7c33c3c))



# [Version 0.3.0](https://github.com/Deuchnord/kosmorro/compare/v0.2.3...v0.3.0) (2019-12-01)


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



# [Version 0.2.3](https://github.com/Deuchnord/kosmorro/compare/v0.2.2...v0.2.3) (2019-11-24)


### Bug Fixes

* **dumper:** display the right date on output text ([2511d31](https://github.com/Deuchnord/kosmorro/commit/2511d31c37dc5bbb790ebeabc7c230e8641b1448))



# [Version 0.2.2](https://github.com/Deuchnord/kosmorro/compare/v0.2.1...v0.2.2) (2019-11-18)


### Bug Fixes

* set times are now correct ([82bdc70](https://github.com/Deuchnord/kosmorro/commit/82bdc7055b903bcd586e69374ba93f843ae95ceb))


### Features

* add argument to get the current version ([5f74b08](https://github.com/Deuchnord/kosmorro/commit/5f74b08d15bbccededfc5a195b6943c408c93d16))

# [Version 0.2.1](https://github.com/Deuchnord/kosmorro/compare/v0.2.0...v0.2.1) (2019-11-17)


### Bug Fixes

* Move version constant to its own file to prevent sgp4 module failing in the AUR ([9a0c9d3](https://github.com/Deuchnord/kosmorro/commit/9a0c9d3ae34c5fa561b5a1b252d39a5ef2a0a4b9))

# [Version 0.2.0](https://github.com/Deuchnord/kosmorro/compare/v0.1.0...v0.2.0) (2019-11-17)

### Added

- Add JSON output
- Add argument to clear the cache

### Changed

- Update Numpy to v1.17.4
- Update PyLint to v2.4.4

# v0.1.0 (2019-11-10)

- First version
