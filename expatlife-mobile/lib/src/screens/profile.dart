import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return SafeArea(child: Padding(
      padding: const EdgeInsets.all(16),
      child: ListView(
        children: [
          Text('Profile', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 12),
          const Card(child: ListTile(leading: Icon(Icons.language), title: Text('Languages'), subtitle: Text('EN/PT starter'))),
          const SizedBox(height: 8),
          const Text('Next: add authentication, favorites, reminders, and CMS sync.'),
        ],
      ),
    ));
  }
}
