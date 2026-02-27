import 'package:shared_preferences/shared_preferences.dart';

class Store {
  static const _countryId = 'countryId';
  static const _countryName = 'countryName';
  static const _cityId = 'cityId';
  static const _cityName = 'cityName';

  Future<void> saveDest(int countryId, String countryName, int cityId, String cityName) async {
    final sp = await SharedPreferences.getInstance();
    await sp.setInt(_countryId, countryId);
    await sp.setString(_countryName, countryName);
    await sp.setInt(_cityId, cityId);
    await sp.setString(_cityName, cityName);
  }

  Future<Map<String,dynamic>?> loadDest() async {
    final sp = await SharedPreferences.getInstance();
    final cid = sp.getInt(_countryId);
    final cityId = sp.getInt(_cityId);
    if (cid == null || cityId == null) return null;
    return {
      'countryId': cid,
      'countryName': sp.getString(_countryName) ?? '',
      'cityId': cityId,
      'cityName': sp.getString(_cityName) ?? '',
    };
  }

  Future<void> clearDest() async {
    final sp = await SharedPreferences.getInstance();
    await sp.remove(_countryId);
    await sp.remove(_countryName);
    await sp.remove(_cityId);
    await sp.remove(_cityName);
  }
}
