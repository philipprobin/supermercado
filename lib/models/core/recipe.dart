import 'package:flutter/cupertino.dart';

class Recipe {
  String title;
  String image;
  String calories;
  String time;
  List<TutorialStep> tutorial;
  List<Ingredient> ingredients;
  String emissions;
  String nutri_score;
  String price;


  Recipe({
    this.title,
    this.image,
    this.time,
    this.tutorial,
    this.ingredients,
    this.emissions,
    this.calories,
    this.nutri_score,
    this.price

  });

  Recipe.fromMap(Map<String, dynamic> data) {
    this.title = data['title'] as String;
    this.image = data['image'] as String;
    this.time = data['time'].toString();
    var tutorialMap = data['instructions'];
    this.tutorial = TutorialStep.toList(tutorialMap);
    var ingredientMap = data['ingredients'];
    this.ingredients = Ingredient.toList(ingredientMap);
    this.emissions = data['emissions'] as String;
    this.calories = data['energy'] as String;
    this.price = data['price'] as String;
    this.nutri_score = data['nutri_score'] as String;
  }
}

class TutorialStep {
  String step;
  String description;
  TutorialStep({this.step, this.description});

  Map<String, Object> toMap() {
    return {
      'step': step,
      'description': description,
    };
  }

  factory TutorialStep.fromJson(Map<String, Object> json) => TutorialStep(
    step: json['step'],
    description: json['description'],
  );

  static List<TutorialStep> toList(var entries) {
    List<TutorialStep> list = [];
    for (var entry in entries) {
      if (entry['step'] != null && entry['description'] != null) {
        TutorialStep tutorialStep = new TutorialStep(
            step: entry['step'] as String, description: entry['description'] as String);
        list.add(tutorialStep);
      }
    }
    return list;
  }
}


class Ingredient {
  String name;
  String size;

  Ingredient({this.name, this.size});

  Map<String, Object> toMap() {
    return {
      'name': name,
      'size': size,
    };
  }

  static List<Ingredient> toList(var entries) {
    List<Ingredient> list = [];
    for (var entry in entries) {
      if (entry['name'] != null && entry['size'] != null) {
        Ingredient ingredient = new Ingredient(
            name: entry['name'] as String, size: entry['size'] as String);
        list.add(ingredient);
      }
    }
    return list;
  }
}
