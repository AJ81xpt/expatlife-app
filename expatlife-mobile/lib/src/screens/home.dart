import 'package:flutter/material.dart';
import '../api.dart';
import '../store.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final api = Api();
  final store = Store();

  Map<String,dynamic>? dest;
  List<dynamic> countries = [];
  List<dynamic> cities = [];
  int? countryId;
  String? countryName;
  int? cityId;
  String? cityName;

  bool loading = true;

  @override
  void initState() {
    super.initState();
    _init();
  }

  Future<void> _init() async {
    dest = await store.loadDest();
    countries = await api.countries();
    setState(() { loading = false; });
  }

  Future<void> _loadCities() async {
    if (countryId == null) return;
    cities = await api.cities(countryId!);
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: loading ? const Center(child: CircularProgressIndicator()) : Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(dest == null ? 'Select destination' : '${dest!['cityName']} · ${dest!['countryName']}',
              style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 12),
            if (dest == null) ...[
              DropdownButtonFormField<int>(
                decoration: const InputDecoration(labelText: 'Country'),
                items: countries.map((c)=>DropdownMenuItem<int>(value:c['id'], child: Text(c['name']))).toList(),
                onChanged: (v) async {
                  final c = countries.firstWhere((x)=>x['id']==v);
                  setState(() {
                    countryId = v;
                    countryName = c['name'];
                    cityId = null;
                    cityName = null;
                    cities = [];
                  });
                  await _loadCities();
                },
              ),
              const SizedBox(height: 12),
              DropdownButtonFormField<int>(
                decoration: const InputDecoration(labelText: 'City'),
                items: cities.map((c)=>DropdownMenuItem<int>(value:c['id'], child: Text(c['name']))).toList(),
                onChanged: (v) {
                  final c = cities.firstWhere((x)=>x['id']==v);
                  setState(() { cityId = v; cityName = c['name']; });
                },
              ),
              const SizedBox(height: 12),
              FilledButton(
                onPressed: (countryId!=null && cityId!=null) ? () async {
                  await store.saveDest(countryId!, countryName ?? '', cityId!, cityName ?? '');
                  dest = await store.loadDest();
                  setState(() {});
                } : null,
                child: const Text('Continue'),
              )
            ] else ...[
              Expanded(child: ListView(
                children: [
                  _card(Icons.checklist, 'Settle in', 'Go to Checklist tab to view tasks'),
                  _card(Icons.explore, 'Essentials near you', 'Go to Explore tab to browse'),
                  _card(Icons.euro, 'Cost snapshot', 'Go to Cost tab'),
                  const SizedBox(height: 8),
                  TextButton.icon(
                    onPressed: () async { await store.clearDest(); dest=null; setState(() {}); },
                    icon: const Icon(Icons.swap_horiz),
                    label: const Text('Change destination'),
                  )
                ],
              ))
            ]
          ],
        ),
      ),
    );
  }

  Widget _card(IconData icon, String title, String subtitle) => Card(
    child: ListTile(leading: Icon(icon), title: Text(title), subtitle: Text(subtitle)),
  );
}
