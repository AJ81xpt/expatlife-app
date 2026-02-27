import 'dart:convert';
import 'package:http/http.dart' as http;

class Api {
  // Android emulator -> host machine
  static const base = 'http://10.0.2.2:8000';

  Future<List<dynamic>> countries({String lang='en'}) async {
    final r = await http.get(Uri.parse('$base/countries?lang=$lang'));
    return json.decode(r.body) as List<dynamic>;
  }

  Future<List<dynamic>> cities(int countryId) async {
    final r = await http.get(Uri.parse('$base/cities?country_id=$countryId'));
    return json.decode(r.body) as List<dynamic>;
  }

  Future<List<dynamic>> tasks(int countryId, {String lang='en'}) async {
    final r = await http.get(Uri.parse('$base/tasks?country_id=$countryId&lang=$lang'));
    return json.decode(r.body) as List<dynamic>;
  }

  Future<List<dynamic>> places(int cityId, {String? type}) async {
    final qs = <String,String>{'city_id': cityId.toString()};
    if (type != null) qs['place_type'] = type;
    final r = await http.get(Uri.parse('$base/places').replace(queryParameters: qs));
    return json.decode(r.body) as List<dynamic>;
  }

  Future<Map<String,dynamic>> cost(int cityId) async {
    final r = await http.get(Uri.parse('$base/cost?city_id=$cityId'));
    return json.decode(r.body) as Map<String,dynamic>;
  }
}
