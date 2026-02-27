import 'package:flutter/material.dart';
import 'src/app.dart';

void main() => runApp(const ExpatLifeApp());

class ExpatLifeApp extends StatelessWidget {
  const ExpatLifeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ExpatLife',
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: const Color(0xFF2BB3A6)),
      home: const AppShell(),
    );
  }
}
