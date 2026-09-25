import 'package:flutter/material.dart';
import 'package:oiyajiapp/core/constants/languages.dart';
import 'package:oiyajiapp/data/models/database.dart';

class AppProvider extends ChangeNotifier {
  // حالة المستخدم
  Map<String, dynamic>? _currentUser;
  bool _isLoggedIn = false;
  String _language = 'ar';
  ThemeMode _themeMode = ThemeMode.light;

  // حالة الكتب
  List<Map<String, dynamic>> _books = [];
  List<Map<String, dynamic>> _favorites = [];
  List<Map<String, dynamic>> _downloads = [];

  // حالة التحميل
  bool _isLoading = false;

  // Getters
  Map<String, dynamic>? get currentUser => _currentUser;
  bool get isLoggedIn => _isLoggedIn;
  String get language => _language;
  ThemeMode get themeMode => _themeMode;
  List<Map<String, dynamic>> get books => _books;
  List<Map<String, dynamic>> get favorites => _favorites;
  List<Map<String, dynamic>> get downloads => _downloads;
  bool get isLoading => _isLoading;

  final DatabaseHelper _dbHelper = DatabaseHelper();

  // تهيئة التطبيق
  Future<void> initializeApp() async {
    _setLoading(true);

    try {
      // تحميل الكتب من قاعدة البيانات
      _books = await _dbHelper.getAllBooks();

      // التحقق من حالة تسجيل الدخول
      final user = await _getCurrentUser();
      if (user != null) {
        _currentUser = user;
        _isLoggedIn = true;
        _language = user['language'] ?? 'ar';
      }

      notifyListeners();
    } catch (e) {
      print('Error initializing app: $e');
    } finally {
      _setLoading(false);
    }
  }

  // تسجيل الدخول
  Future<bool> login(String email, String password) async {
    _setLoading(true);

    try {
      final user = await _dbHelper.getUserByEmail(email);

      if (user != null && user['password'] == password) {
        _currentUser = user;
        _isLoggedIn = true;

        // تحديث حالة تسجيل الدخول في قاعدة البيانات
        await _updateUserLoginStatus(user['id'], true);

        notifyListeners();
        return true;
      }
      return false;
    } catch (e) {
      print('Login error: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // تسجيل مستخدم جديد
  Future<bool> register(String name, String email, String password) async {
    _setLoading(true);

    try {
      // التحقق من عدم وجود المستخدم مسبقاً
      final existingUser = await _dbHelper.getUserByEmail(email);
      if (existingUser != null) {
        return false; // المستخدم موجود مسبقاً
      }

      // إنشاء مستخدم جديد
      final userId = await _dbHelper.createUser({
        'name': name,
        'email': email,
        'password': password,
        'language': 'ar',
        'isLoggedIn': 1,
      });

      if (userId > 0) {
        _currentUser = {'id': userId, 'name': name, 'email': email, 'language': 'ar'};
        _isLoggedIn = true;
        notifyListeners();
        return true;
      }
      return false;
    } catch (e) {
      print('Register error: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // تسجيل الخروج
  Future<void> logout() async {
    if (_currentUser != null) {
      await _updateUserLoginStatus(_currentUser!['id'], false);
    }

    _currentUser = null;
    _isLoggedIn = false;
    notifyListeners();
  }

  // تغيير اللغة
  Future<void> changeLanguage(String newLanguage) async {
    _language = newLanguage;
    LanguageManager.setLanguage(newLanguage);

    if (_currentUser != null) {
      // تحديث لغة المستخدم في قاعدة البيانات
      // (ستحتاج لإضافة دالة updateUser في DatabaseHelper)
    }

    notifyListeners();
  }

  // تغيير الوضع
  void changeTheme(ThemeMode mode) {
    _themeMode = mode;
    notifyListeners();
  }

  // إضافة إلى المفضلة
  Future<void> addToFavorites(int bookId) async {
    if (_currentUser != null) {
      await _dbHelper.addToFavorites(_currentUser!['id'], bookId);
      _loadFavorites();
    }
  }

  // تحميل المفضلة
  Future<void> _loadFavorites() async {
    // تنفيذ دالة جلب المفضلة من قاعدة البيانات
    notifyListeners();
  }

  // دوال مساعدة
  Future<Map<String, dynamic>?> _getCurrentUser() async {
    final db = await _dbHelper.database;
    final result = await db.query(
      'users',
      where: 'isLoggedIn = ?',
      whereArgs: [1],
    );
    return result.isNotEmpty ? result.first : null;
  }

  Future<void> _updateUserLoginStatus(int userId, bool isLoggedIn) async {
    final db = await _dbHelper.database;
    await db.update(
      'users',
      {'isLoggedIn': isLoggedIn ? 1 : 0},
      where: 'id = ?',
      whereArgs: [userId],
    );
  }

  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }
}