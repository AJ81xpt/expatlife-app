import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

class TaskDetail extends StatelessWidget {
  final Map task;
  const TaskDetail({super.key, required this.task});

  @override
  Widget build(BuildContext context) {
    final steps = (task['steps'] as List?) ?? [];
    final docs = (task['documents'] as List?) ?? [];
    final links = (task['links'] as List?) ?? [];

    return Scaffold(
      appBar: AppBar(title: Text(task['title'] ?? '')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(task['summary'] ?? '', style: Theme.of(context).textTheme.bodyLarge),
          const SizedBox(height: 12),
          Text('Last reviewed: ${task['last_reviewed_at'] ?? ''}', style: Theme.of(context).textTheme.bodySmall),
          const SizedBox(height: 16),
          if (steps.isNotEmpty) ...[
            Text('Steps', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            ...steps.map((s)=>Card(child: ListTile(title: Text(s['title']), subtitle: Text(s['body'])))),
            const SizedBox(height: 16),
          ],
          if (docs.isNotEmpty) ...[
            Text('Documents', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            ...docs.map((d)=>ListTile(
              leading: Icon((d['required'] ?? true) ? Icons.check_box_outlined : Icons.check_box_outline_blank),
              title: Text(d['name']),
              subtitle: d['notes'] != null ? Text(d['notes']) : null,
            )),
            const SizedBox(height: 16),
          ],
          if (links.isNotEmpty) ...[
            Text('Links', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            ...links.map((l)=>Card(
              child: ListTile(
                leading: const Icon(Icons.link),
                title: Text(l['label']),
                subtitle: Text(l['url']),
                onTap: () async {
                  final uri = Uri.parse(l['url']);
                  await launchUrl(uri, mode: LaunchMode.externalApplication);
                },
              ),
            )),
          ]
        ],
      ),
    );
  }
}
