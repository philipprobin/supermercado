class Recipe {
  String title;
  String image;
  String calories;
  String time;
  String instructions;
  List<String> ingredients;

  Recipe({this.title, this.image, this.time, this.instructions, this.ingredients,});

  Recipe.fromMap(Map<String, dynamic> data){
      this.title = data['title'] as String;
      this.image = data['image'] as String;
      this.time = data['time'].toString();
      this.instructions = data['instructions'] as String;
      var tmp = data['ingredients'] as List<dynamic>;
      this.ingredients = tmp.map((e) => e.toString()).toList();
  }

  factory Recipe.fromJson(Map<String, Object> json) {
    return Recipe(
      title: json['title'],
      image: json['image'],
      time: json['time'],
      ingredients: json['ingredients'],
      instructions: json['instructions'],

    );
  }
}
