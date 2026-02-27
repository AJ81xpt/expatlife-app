import 'package:flutter/material.dart';
import '../api.dart';
import '../store.dart';

class CostScreen extends StatefulWidget {
  const CostScreen({super.key});
  @override
  State<CostScreen> createState() => _CostScreenState();
}

class _CostScreenState extends State<CostScreen> {
  final api = Api();
  final store = Store();
  Map<String,dynamic>? dest;
  Map<String,dynamic>? cost;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    dest = await store.loadDest();
    if (dest == null) { setState(() { loading=false; }); return; }
    cost = await api.cost(dest!['cityId']);
    setState(() { loading=false; });
  }

  @override
  Widget build(BuildContext context) {
    if (loading) return const SafeArea(child: Center(child: CircularProgressIndicator()));
    if (dest == null) return const SafeArea(child: Center(child: Text('Select destination on Home')));
    final c = cost ?? {};
    return SafeArea(child: Padding(
      padding: const EdgeInsets.all(16),
      child: ListView(
        children: [
          Text('Cost of living', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 12),
          _row('Rent (1BR)', '€${c['rent_1br_min']}–€${c['rent_1br_max']}'),
          _row('Rent (3BR)', '€${c['rent_3br_min']}–€${c['rent_3br_max']}'),
          _row('Utilities', '€${c['utilities_min']}–€${c['utilities_max']}'),
          _row('Transport (monthly)', '€${c['transport_monthly_min']}–€${c['transport_monthly_max']}'),
          _row('Groceries (monthly)', '€${c['groceries_monthly_min']}–€${c['groceries_monthly_max']}'),
          const SizedBox(height: 12),
          Text('Last updated: ${c['last_updated_at'] ?? ''}', style: Theme.of(context).textTheme.bodySmall),
        ],
      ),
    ));
  }

  Widget _row(String k, String v) => Card(child: ListTile(title: Text(k), trailing: Text(v)));
}
