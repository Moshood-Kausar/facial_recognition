import 'package:flutter/material.dart';
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'package:tflite/tflite.dart';

void main() {
  runApp(MyApp());
  _loadModel();
}

void _loadModel() async {
  try {
    await Tflite.loadModel(
      model: 'assets/model.tflite',
      labels: 'assets/labels.txt',
    );
  } catch (e) {
    print('Error loading model: $e');
  }
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Emotion Detection',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Emotion Detection'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key? key, required this.title}) : super(key: key);
  final String title;
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  //final picker = ImagePicker();
  ImagePicker picker = ImagePicker();
  XFile? image;

  File? _imageFile;
  String? _predictedEmotion;
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ElevatedButton(
            onPressed: () async {
              image = await picker.pickImage(source: ImageSource.gallery);
              setState(() {
                
              });
            },
            child: Text("Pick Image")),
        image == null ? Container() : Image.file(File(image!.path))
      ],
    );
  }
}

// Future<String> predictEmotion(List<int> imageBytes) async {
//   try {
//     final image = ImageUtils.convertListToImage(imageBytes);
//     final preprocessedImage = preprocessImage(image);
//     final output = await runInference(preprocessedImage);
//     final predictedIndex = output.argmax();
//     return EMOTIONS[predictedIndex];
//   } catch (e) {
//     throw Exception('Failed to predict emotion: ${e.toString()}');
//   }
// }
