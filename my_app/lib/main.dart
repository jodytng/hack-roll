import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        resizeToAvoidBottomInset: false,
        appBar: AppBar(
          backgroundColor: const Color(0xEAE0D500),
          title: const Text('Everybody dies',
              style: TextStyle(
                  fontFamily: 'Vollkorn',
                  fontSize: 55,
                  fontStyle: FontStyle.italic)),
        ),
        body: Center(
          child: Column(
            children: <Widget>[
              Image.asset('images/Artwork1.png'),
            ],
          ),
        ),
      ),
    );
  }
}
