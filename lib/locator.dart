import 'package:get_it/get_it.dart';
import 'package:hungry/services/db_pull.dart';

final locator = GetIt.instance;

void setup() {
  // dependency injector
  locator.registerLazySingleton<DbPull>(() => DbPull());
}