# Semantic Versioning Changelog

# [1.16.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.15.0...v1.16.0) (2023-09-03)


### Features

* add all missing APIs ([#65](https://github.com/casdoor/casdoor-python-sdk/issues/65)) ([542c8d9](https://github.com/casdoor/casdoor-python-sdk/commit/542c8d90499ce362896699a04e96f75bfb51ad3c))

# [1.15.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.14.2...v1.15.0) (2023-08-08)


### Features

* Removed cached_property for python 3.7 compatibility ([#62](https://github.com/casdoor/casdoor-python-sdk/issues/62)) ([2bae07a](https://github.com/casdoor/casdoor-python-sdk/commit/2bae07ad40227187d443fc0b3a3d532cb800d59b))

## [1.14.2](https://github.com/casdoor/casdoor-python-sdk/compare/v1.14.1...v1.14.2) (2023-08-08)


### Bug Fixes

* Removed unused code and fixed incorrect type hints  ([#60](https://github.com/casdoor/casdoor-python-sdk/issues/60)) ([712c1f8](https://github.com/casdoor/casdoor-python-sdk/commit/712c1f895bfa8657ba7c98a38550f58fc5529a2e))

## [1.14.1](https://github.com/casdoor/casdoor-python-sdk/compare/v1.14.0...v1.14.1) (2023-08-07)


### Bug Fixes

* fix broken links ([#54](https://github.com/casdoor/casdoor-python-sdk/issues/54)) ([db480cc](https://github.com/casdoor/casdoor-python-sdk/commit/db480cc29eb2a1008fff8f0b0a6ca10436afc8e7))

# [1.14.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.13.1...v1.14.0) (2023-08-07)


### Features

* Encapsulated aiohttp methods to replace __del__ to avoid http connection leaks ([#55](https://github.com/casdoor/casdoor-python-sdk/issues/55)) ([2a2b482](https://github.com/casdoor/casdoor-python-sdk/commit/2a2b482daa171b5fe169b43f942ab29a2ef172bb))

## [1.13.1](https://github.com/casdoor/casdoor-python-sdk/compare/v1.13.0...v1.13.1) (2023-08-05)


### Bug Fixes

* Removed unused code and fixed incorrect type hints ([#53](https://github.com/casdoor/casdoor-python-sdk/issues/53)) ([b5b3e01](https://github.com/casdoor/casdoor-python-sdk/commit/b5b3e016468263b856e0c582498fafd31af7c825))

# [1.13.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.12.1...v1.13.0) (2023-07-25)


### Features

* support kwargs in parse_jwt_token() ([51cd7bd](https://github.com/casdoor/casdoor-python-sdk/commit/51cd7bd09e072a096db2aab03267adb193c5950e))

## [1.12.1](https://github.com/casdoor/casdoor-python-sdk/compare/v1.12.0...v1.12.1) (2023-07-21)


### Bug Fixes

* Fixed an incorrect type hint. ([#50](https://github.com/casdoor/casdoor-python-sdk/issues/50)) ([40e0f88](https://github.com/casdoor/casdoor-python-sdk/commit/40e0f88c556e08ca25a02e805f9b8d60f07f884b))

# [1.12.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.11.0...v1.12.0) (2023-05-04)


### Features

* add batch_enforce ([#46](https://github.com/casdoor/casdoor-python-sdk/issues/46)) ([83de7de](https://github.com/casdoor/casdoor-python-sdk/commit/83de7de2c9cbdbf429f514efadfb1a53a1246607))

# [1.11.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.10.0...v1.11.0) (2023-04-30)


### Features

* support refresh token in get_oauth_token() ([#45](https://github.com/casdoor/casdoor-python-sdk/issues/45)) ([27fef52](https://github.com/casdoor/casdoor-python-sdk/commit/27fef5267835a6cf6dc3247837dd814e0638515b))

# [1.10.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.9.0...v1.10.0) (2023-04-25)


### Features

* add v3-v5 field into enforce function's arg. ([#44](https://github.com/casdoor/casdoor-python-sdk/issues/44)) ([485ee89](https://github.com/casdoor/casdoor-python-sdk/commit/485ee897ecf7ccd91cfa6106e8ec8508b07682e7))

# [1.9.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.8.0...v1.9.0) (2023-04-15)


### Features

* add get_user_count() to sdk ([#42](https://github.com/casdoor/casdoor-python-sdk/issues/42)) ([f06ae3f](https://github.com/casdoor/casdoor-python-sdk/commit/f06ae3f686a133171c5bb9005b4e6c4c279f5664))

# [1.8.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.7.0...v1.8.0) (2023-02-10)


### Features

* Added ability to use Client Credentials Grant ([#39](https://github.com/casdoor/casdoor-python-sdk/issues/39)) ([fee0fe0](https://github.com/casdoor/casdoor-python-sdk/commit/fee0fe08b346092ed12e62196eec8e64d3a6003d))

# [1.7.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.6.0...v1.7.0) (2023-02-09)


### Features

* Added ability to use Resource Owner Password Credentials Grant ([#38](https://github.com/casdoor/casdoor-python-sdk/issues/38)) ([caf8e8a](https://github.com/casdoor/casdoor-python-sdk/commit/caf8e8af862fe9c2ba361358278efa4b318c987a))

# [1.6.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.5.1...v1.6.0) (2023-01-17)


### Features

* Append enforce function to sdk ([#37](https://github.com/casdoor/casdoor-python-sdk/issues/37)) ([1546819](https://github.com/casdoor/casdoor-python-sdk/commit/15468198312ff310b45d99e8bb9c79287570dbd4))

## [1.5.1](https://github.com/casdoor/casdoor-python-sdk/compare/v1.5.0...v1.5.1) (2022-12-12)


### Bug Fixes

* Code-style was refactored with PEP8 standard and linter was appended ([#35](https://github.com/casdoor/casdoor-python-sdk/issues/35)) ([51a2501](https://github.com/casdoor/casdoor-python-sdk/commit/51a25015eb6854fe06c16a2bc04c58a0ed7dedd1))

# [1.5.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.4.0...v1.5.0) (2022-12-12)


### Features

* Appended asynchronous SDK version ([#33](https://github.com/casdoor/casdoor-python-sdk/issues/33)) ([92a6010](https://github.com/casdoor/casdoor-python-sdk/commit/92a601053fd3c3bea18596185ea63c013cae3642))

# [1.4.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.3.0...v1.4.0) (2022-12-07)


### Features

* add refresh_oauth_token() API ([#32](https://github.com/casdoor/casdoor-python-sdk/issues/32)) ([352d47e](https://github.com/casdoor/casdoor-python-sdk/commit/352d47ebc69f86287364da14217acbad2c88057d))

# [1.3.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.2.1...v1.3.0) (2022-12-04)


### Features

* fix init imports ([#31](https://github.com/casdoor/casdoor-python-sdk/issues/31)) ([fbb2756](https://github.com/casdoor/casdoor-python-sdk/commit/fbb2756d8312efede6c5e27f16c2e6615b6e51f0))

# Change import

* fix init imports

# Semantic Versioning Changelog

## [1.2.1](https://github.com/casdoor/casdoor-python-sdk/compare/v1.2.0...v1.2.1) (2022-08-19)


### Bug Fixes

* fix init syntax errer ([#25](https://github.com/casdoor/casdoor-python-sdk/issues/25)) ([d6b7952](https://github.com/casdoor/casdoor-python-sdk/commit/d6b79529d247631ca866f27fea5e9fd5745af3d1))

# [1.2.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.1.5...v1.2.0) (2022-08-12)


### Features

* add parameter 'application_name' to init sdk ([#24](https://github.com/casdoor/casdoor-python-sdk/issues/24)) ([49b5599](https://github.com/casdoor/casdoor-python-sdk/commit/49b5599cc2d93b2c05c36aa7b20dbe26352d554a))

## [1.1.5](https://github.com/casdoor/casdoor-python-sdk/compare/v1.1.4...v1.1.5) (2022-07-17)


### Bug Fixes

* modify keyword argument in get_sdk() of test_oauth.TestOAuth ([#23](https://github.com/casdoor/casdoor-python-sdk/issues/23)) ([21614c7](https://github.com/casdoor/casdoor-python-sdk/commit/21614c77a02934a8e98031373f6f3d9c200bdeda))

## [1.1.4](https://github.com/casdoor/casdoor-python-sdk/compare/v1.1.3...v1.1.4) (2022-07-07)


### Bug Fixes

* certificate convert to bytes to meet algorithm need ([#21](https://github.com/casdoor/casdoor-python-sdk/issues/21)) ([7f20151](https://github.com/casdoor/casdoor-python-sdk/commit/7f20151ce5983d0ff10a56c361a5a841865f8cd0))

## [1.1.3](https://github.com/casdoor/casdoor-python-sdk/compare/v1.1.2...v1.1.3) (2022-03-20)


### Bug Fixes

* Fix self.algorithms data type ([#17](https://github.com/casdoor/casdoor-python-sdk/issues/17)) ([5f49189](https://github.com/casdoor/casdoor-python-sdk/commit/5f4918961116325e395eeb792a5718b56af20674))

## [1.1.2](https://github.com/casdoor/casdoor-python-sdk/compare/v1.1.1...v1.1.2) (2022-03-20)


### Bug Fixes

* hardcode front_endpoint ([#16](https://github.com/casdoor/casdoor-python-sdk/issues/16)) ([ef17ce6](https://github.com/casdoor/casdoor-python-sdk/commit/ef17ce6a172066b0847a109609ce0131b5765bf8))

## [1.1.1](https://github.com/casdoor/casdoor-python-sdk/compare/v1.1.0...v1.1.1) (2022-03-18)


### Bug Fixes

* correct the decryption algorithm to rs256 ([#15](https://github.com/casdoor/casdoor-python-sdk/issues/15)) ([bcb0657](https://github.com/casdoor/casdoor-python-sdk/commit/bcb0657009142e10dd4fbb7c53436d92640b5c0d))

# [1.1.0](https://github.com/casdoor/casdoor-python-sdk/compare/v1.0.0...v1.1.0) (2022-03-11)


### Features

* add badges ([#14](https://github.com/casdoor/casdoor-python-sdk/issues/14)) ([7cd6735](https://github.com/casdoor/casdoor-python-sdk/commit/7cd673552bdd43f4170df6ffd8384181bdcbe013))

# 1.0.0 (2022-03-11)


### Bug Fixes

* change package name and update readme ([#12](https://github.com/casdoor/casdoor-python-sdk/issues/12)) ([1d521c6](https://github.com/casdoor/casdoor-python-sdk/commit/1d521c6ac3417cc139c4618df81ef59f38441169))


### Features

* add auto-release ([#11](https://github.com/casdoor/casdoor-python-sdk/issues/11)) ([6b088bb](https://github.com/casdoor/casdoor-python-sdk/commit/6b088bb5525ae738e298b3fc5dc4fe227312408f))
* general implement ([#1](https://github.com/casdoor/casdoor-python-sdk/issues/1)) ([d713fd3](https://github.com/casdoor/casdoor-python-sdk/commit/d713fd3a4ee83540e19f9bf046f1520173658d46))
* modify_user functions added ([#2](https://github.com/casdoor/casdoor-python-sdk/issues/2)) ([dae1fd8](https://github.com/casdoor/casdoor-python-sdk/commit/dae1fd8a7ecb1372ce5411653b9d37463769b196))
