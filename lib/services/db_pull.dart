import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:hungry/models/helper/recipe_helper.dart';

import '../models/core/recipe.dart';

final FirebaseFirestore _firestore = FirebaseFirestore.instance;

class DbPull {
  final CollectionReference _lidlCollection = _firestore.collection('lidl');

  final CollectionReference _recipesCollection =
      _firestore.collection('recipes');

  Future<void> fetchRecipes() async {
    final QuerySnapshot snapshot = await _recipesCollection.get();

    // Get the string from the Firestore database
    for (final DocumentSnapshot document in snapshot.docs) {
      // Get the data map from the snapshot
      Map<String, dynamic> data = document.data();

      // Use the data map to create a new MyObject instance
      Recipe myRecipe = Recipe.fromMap(data);
      RecipeHelper.addToRecipeData(myRecipe);
    }
  }

  Future<String> fetchTestDataFromFirestore() async {
    DocumentSnapshot<Object> doc =
        await _lidlCollection.doc('24.12.2022-31.12.2022').get();
    // Get the string from the Firestore database
    if (doc.exists) {
      // Access the data of the document
      Map<String, dynamic> data = doc.data();

      // Get the 'test' field from the data
      String testField = "";
      if (data['test'] != null) {
        testField = data['test'];
      } else {
        testField = "Data is null";
      }

      return testField;
    }
    return "";
  }
}
