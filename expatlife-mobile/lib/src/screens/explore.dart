import 'package:flutter/material.dart';
import '../api.dart';
import '../store.dart';

class ExploreScreen extends StatefulWidget {
  const ExploreScreen({super.key});
  @override
  State<ExploreScreen> createState() => _ExploreScreenState();
}

class _ExploreScreenState extends State<ExploreScreen> {
  final api = Api();
  final store = Store();
  Map<String,dynamic>? dest;
  String type = 'supermarket';
  List<dynamic> places = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    dest = await store.loadDest();
    if (dest == null) { setState(() { loading=false; }); return; }
    places = await api.places(dest!['cityId'], type: type);
    setState(() { loading=false; });
  }

  Future<void> _setType(String v) async {
    setState(() { type=v; loading=true; });
    if (dest != null) places = await api.places(dest!['cityId'], type: type);
    setState(() { loading=false; });
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(child: Padding(
      padding: const EdgeInsets.all(16),
      child: loading ? const Center(child: CircularProgressIndicator()) :
        (dest==null) ? const Center(child: Text('Select destination on Home')) :
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Explore', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 8),
            SegmentedButton<String>(
              segments: const [
                ButtonSegment(value:'school', label: Text('Schools'), icon: Icon(Icons.school_outlined)),
                ButtonSegment(value:'supermarket', label: Text('Supermarkets'), icon: Icon(Icons.shopping_cart_outlined)),
                ButtonSegment(value:'course', label: Text('Courses'), icon: Icon(Icons.translate_outlined)),
                ButtonSegment(value:'service', label: Text('Services'), icon: Icon(Icons.home_repair_service_outlined)),
              ],
              selected: {type},
              onSelectionChanged: (s)=>_setType(s.first),
            ),
            const SizedBox(height: 12),
            Expanded(child: ListView(
              children: places.map((p)=>Card(
                child: ListTile(
                  title: Text(p['name']),
                  subtitle: Text(p['address']),
                ),
              )).toList(),
            ))
          ],
        ),
    ));
  }
}
