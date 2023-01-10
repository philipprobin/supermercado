import 'package:flutter/material.dart';
import 'package:hungry/models/core/recipe.dart';
import 'package:hungry/models/helper/recipe_helper.dart';
import 'package:hungry/views/screens/profile_page.dart';
import 'package:hungry/views/widgets/custom_app_bar.dart';
import 'package:hungry/views/widgets/recommendation_recipe_card.dart';

class HomePage extends StatefulWidget {
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final List<Recipe> featuredRecipe = RecipeHelper.featuredRecipe;

  List<Recipe> recommendationRecipe = [];

  final List<Recipe> newlyPostedRecipe = RecipeHelper.featuredRecipe;

  @override
  void initState() {
    super.initState();
    fillList();
  }

  Future<void> fillList() async {
    recommendationRecipe = await RecipeHelper.fetchRecipes();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: Text('Supermercado',
            style: TextStyle(fontFamily: 'inter', fontWeight: FontWeight.w700)),
        showProfilePhoto: true,
        profilePhoto: AssetImage('assets/images/pp.png'),
        profilePhotoOnPressed: () {
          Navigator.of(context)
              .push(MaterialPageRoute(builder: (context) => ProfilePage()));
        },
      ),
      body: ListView(
        shrinkWrap: true,
        physics: BouncingScrollPhysics(),
        children: [
          // Section 2 - Recommendation Recipe
          Container(
            margin: EdgeInsets.only(top: 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header
                Container(
                  margin: EdgeInsets.only(bottom: 16),
                  padding: EdgeInsets.symmetric(horizontal: 16),
                  child: Text(
                    'Ein paar Rezepte, die dir gefallen könnten...',
                    style: TextStyle(color: Colors.grey),
                  ),
                ),
                // Content
                Container(
                  height: 250,
                  child: FutureBuilder<List<Recipe>>(
                    future: RecipeHelper.fetchRecipes(),
                    builder: (context, snapshot) {
                      if (snapshot.hasData) {
                        return ListView.separated(
                          shrinkWrap: true,
                          physics: BouncingScrollPhysics(),
                          scrollDirection: Axis.horizontal,
                          itemCount: snapshot.data.length,
                          padding: EdgeInsets.symmetric(horizontal: 16),
                          separatorBuilder: (context, index) {
                            return SizedBox(width: 16);
                          },
                          itemBuilder: (context, index) {
                            return RecommendationRecipeCard(
                                data: snapshot.data[index]);
                          },
                        );
                      } else if (snapshot.hasError) {
                        return Text("${snapshot.error}");
                      }
                      return CircularProgressIndicator();
                    },
                  ),
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
