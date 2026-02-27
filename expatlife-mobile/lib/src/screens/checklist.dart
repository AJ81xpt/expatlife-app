import 'package:flutter/material.dart';
import '../api.dart';
import '../store.dart';
import 'task_detail.dart';

class ChecklistScreen extends StatefulWidget {
  const ChecklistScreen({super.key});
  @override
  State<ChecklistScreen> createState() => _ChecklistScreenState();
}

class _ChecklistScreenState extends State<ChecklistScreen> {
  final api = Api();
  final store = Store();
  Map<String,dynamic>? dest;
  List<dynamic> tasks = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    dest = await store.loadDest();
    if (dest == null) { setState(() { loading=false; }); return; }
    tasks = await api.tasks(dest!['countryId']);
    setState(() { loading=false; });
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: loading ? const Center(child: CircularProgressIndicator()) :
          (dest==null) ? const Center(child: Text('Select destination on Home')) :
          ListView(
            children: [
              Text('Checklist', style: Theme.of(context).textTheme.headlineSmall),
              const SizedBox(height: 8),
              ...tasks.map((t)=>Card(
                child: ListTile(
                  title: Text(t['title']),
                  subtitle: Text(t['summary']),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: ()=>Navigator.of(context).push(MaterialPageRoute(builder: (_)=>TaskDetail(task: t))),
                ),
              ))
            ],
          ),
      ),
    );
  }
}
