import 'package:hungry/models/core/recipe.dart';

import '../../locator.dart';
import '../../services/db_pull.dart';

class RecipeHelper {
  static List<Recipe> featuredRecipe = [];

  static Future<List<Recipe>> fetchRecipes() async {
    await locator.get<DbPull>().fetchRecipes();
    return featuredRecipe;
  }

  static Future<void> addToRecipeData(Recipe recipe) async {
    featuredRecipe.add(recipe);
  }
}
