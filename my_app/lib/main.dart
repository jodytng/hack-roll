import 'package:flutter/material.dart';
import 'package:hovering/hovering.dart';
import 'package:my_app/animated_cursor.dart';

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
        home: AnimatedCursor(
            child: MyHomePage(
          title: 'Everybody Dies',
        )));
  }
}

class MyHomePage extends StatelessWidget {
  final String title;

  const MyHomePage({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    double height = MediaQuery.of(context).size.height;
    double width = MediaQuery.of(context).size.width;
    return Scaffold(
      resizeToAvoidBottomInset: false,
      appBar: AppBar(
          toolbarHeight: 100,
          backgroundColor: Theme.of(context).backgroundColor,
          flexibleSpace: Column(children: [
            const SizedBox(
              height: 16,
            ),
            Text('everybody dies',
                style: Theme.of(context).textTheme.titleLarge),
            Text('in loving memory of XXX',
                style: Theme.of(context)
                    .textTheme
                    .labelMedium!
                    .copyWith(color: Theme.of(context).secondaryHeaderColor)),
          ])),
      body: Container(
        constraints: const BoxConstraints.expand(),
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage("images/backgrounds/Untitled.png"),
            fit: BoxFit.cover,
          ),
        ),
        child: Stack(children: [
          Column(
              mainAxisAlignment: MainAxisAlignment.end,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                HoverWidget(
                  hoverChild: Image.asset(
                    scale: height * 0.0038,
                    'images/placeholder.png',
                  ),
                  onHover: (event) {
                    showDialog(context: context, builder: (_) => ShowPhoto());
                  },
                  child: Image.asset(
                    scale: height * 0.0038,
                    'images/placeholder.png',
                  ),
                ),
                const SizedBox(height: 3),
                Image.asset(
                  scale: height * 0.002,
                  'images/caskets/casket1.png',
                ),
                const SizedBox(
                  width: 1600,
                  height: 204,
                ),
              ]),
          Column(children: [
            const SizedBox(
              width: 10,
              height: 500,
            ),
            Row(mainAxisAlignment: MainAxisAlignment.center, children: [
              AnimatedCursorMouseRegion(
                  child: Image.asset(
                scale: width * 0.0016,
                'images/floralarrangements/Colorful-L.png',
              )),
              const SizedBox(width: 80),
              ElevatedButton(
                onPressed: () {},
                style: ButtonStyle(
                    backgroundColor: MaterialStateProperty.all<Color>(
                        const Color.fromARGB(255, 234, 224, 213)),
                    shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                        RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10.0),
                            side: const BorderSide(
                                width: 3,
                                color: Color.fromARGB(255, 10, 9, 8))))),
                child: Padding(
                    padding: const EdgeInsets.all(8),
                    child: Text('Pay Respects',
                        style: Theme.of(context).textTheme.labelMedium)),
              ),
              const SizedBox(width: 80),
              Image.asset(
                scale: width * 0.0016,
                'images/floralarrangements/Colorful-R.png',
              ),
            ]),
            Align(
                alignment: AlignmentDirectional.bottomStart,
                child: Padding(
                  padding: const EdgeInsets.only(left: 32),
                  child: ElevatedButton(
                    onPressed: () async {
                      await showDialog(
                          context: context, builder: (_) => const ShowMenu());
                    },
                    style: ButtonStyle(
                        backgroundColor: MaterialStateProperty.all<Color>(
                            const Color.fromARGB(255, 234, 224, 213)),
                        shape:
                            MaterialStateProperty.all<RoundedRectangleBorder>(
                                RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(10.0),
                                    side: const BorderSide(
                                        width: 3,
                                        color:
                                            Color.fromARGB(255, 10, 9, 8))))),
                    child: Padding(
                        padding: const EdgeInsets.all(8),
                        child: Text('View Food',
                            style: Theme.of(context).textTheme.labelMedium)),
                  ),
                ))
          ]),
        ]),
      ),
    );
  }
}

class ShowMenu extends StatelessWidget {
  const ShowMenu({super.key});

  @override
  Widget build(BuildContext context) {
    return Dialog(
      child: Container(
        height: 400,
        width: 200,
        decoration: const BoxDecoration(
            image: DecorationImage(
                scale: 0.001,
                image: AssetImage('images/menus/Chinese.png'),
                fit: BoxFit.fill)),
      ),
    );
  }
}

class ShowPhoto extends StatelessWidget {
  const ShowPhoto({super.key});

  @override
  Widget build(BuildContext context) {
    return Dialog(
      child: Container(
        height: 300,
        width: 100,
        decoration: const BoxDecoration(
            image: DecorationImage(
                scale: 0.02,
                image: AssetImage('images/placeholder.png'),
                fit: BoxFit.cover)),
      ),
    );
  }
}
