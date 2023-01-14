import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'Everybody Dies',
        theme: ThemeData(
          backgroundColor: const Color.fromARGB(255, 234, 224, 213),
          primaryColor: const Color.fromARGB(255, 10, 9, 8),
          secondaryHeaderColor: const Color.fromARGB(255, 94, 80, 63),
          fontFamily: 'Vollkorn',
          textTheme: const TextTheme(
              titleLarge: TextStyle(
                  fontSize: 32.0,
                  fontStyle: FontStyle.italic,
                  fontWeight: FontWeight.bold),
              labelMedium:
                  TextStyle(fontSize: 16.0, fontWeight: FontWeight.w700)),
        ),
        debugShowCheckedModeBanner: false,
        home: const MyHomePage(
          title: 'Everybody Dies',
        ));
  }
}

class MyHomePage extends StatelessWidget {
  final String title;

  const MyHomePage({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      body: Column(children: <Widget>[
        Container(
            color: Theme.of(context).backgroundColor,
            padding: const EdgeInsets.symmetric(vertical: 10),
            child: Center(
                child: Column(children: [
              Text('everybody dies',
                  style: Theme.of(context).textTheme.titleLarge),
              Text('in loving memory of XXX',
                  style: Theme.of(context)
                      .textTheme
                      .labelMedium!
                      .copyWith(color: Theme.of(context).secondaryHeaderColor)),
            ]))),
        Expanded(
            child: Container(
                decoration: const BoxDecoration(
          image: DecorationImage(
              image: AssetImage('images/backgrounds/Default.png'),
              fit: BoxFit.cover),
        ))),
      ]),
    );
  }
}
