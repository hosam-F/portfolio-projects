import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DatabaseHelper {
  static final DatabaseHelper _instance = DatabaseHelper._internal();
  factory DatabaseHelper() => _instance;
  DatabaseHelper._internal();

  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    String path = join(await getDatabasesPath(), 'sheikh_app.db');
    return await openDatabase(
      path,
      version: 1,
      onCreate: _onCreate,
    );
  }

  Future<void> _onCreate(Database db, int version) async {
    // جدول المستخدمين
    await db.execute('''
      CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        language TEXT DEFAULT 'ar',
        isLoggedIn INTEGER DEFAULT 0,
        createdAt TEXT DEFAULT CURRENT_TIMESTAMP
      )
    ''');

    // جدول الكتب (الجزء الأول والثاني)
    await db.execute('''
      CREATE TABLE books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        subtitle TEXT NOT NULL,
        description TEXT,
        author TEXT NOT NULL,
        pages INTEGER,
        cover_image TEXT,
        file_path TEXT,
        category TEXT,
        language TEXT DEFAULT 'ar',
        rating REAL DEFAULT 0.0,
        download_count INTEGER DEFAULT 0,
        is_favorite INTEGER DEFAULT 0,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
      )
    ''');

    // جدول الفصول
    await db.execute('''
      CREATE TABLE chapters(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        subtitle TEXT,
        start_page INTEGER,
        end_page INTEGER,
        content TEXT,
        is_read INTEGER DEFAULT 0,
        read_progress INTEGER DEFAULT 0,
        last_read TEXT,
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
      )
    ''');

    // جدول التنزيلات
    await db.execute('''
      CREATE TABLE downloads(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        downloaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
        file_path TEXT,
        file_size INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
      )
    ''');

    // جدول المفضلة
    await db.execute('''
      CREATE TABLE favorites(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        added_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (book_id) REFERENCES books(id),
        UNIQUE(user_id, book_id)
      )
    ''');

    // إدخال بيانات تجريبية
    await _insertSampleData(db);
  }

  Future<void> _insertSampleData(Database db) async {
    // إدخال المستخدم الافتراضي
    await db.insert('users', {
      'name': 'مستخدم تجريبي',
      'email': 'test@example.com',
      'password': '123456',
      'language': 'ar',
      'isLoggedIn': 1,
    });

    // إدخال كتب الشيخ محمد الجرافي
    final book1Id = await db.insert('books', {
      'title': 'غاية المريد في الخطب والوعظ الرشيد',
      'subtitle': 'الجزء الأول',
      'description': 'مجموعة خطب ودروس قيمة للشيخ محمد الجرافي',
      'author': 'الشيخ محمد الجرافي',
      'pages': 400,
      'cover_image': 'assets/books/book1.jpg',
      'file_path': 'assets/books/book1.pdf',
      'category': 'خطب ودروس',
      'language': 'ar',
      'rating': 4.8,
      'download_count': 1250,
      'is_favorite': 0,
      'user_id': 1,
    });

    final book2Id = await db.insert('books', {
      'title': 'غاية المريد في الخطب والوعظ الرشيد',
      'subtitle': 'الجزء الثاني',
      'description': 'تكملة لمجموعة الخطب والدروس للشيخ محمد الجرافي',
      'author': 'الشيخ محمد الجرافي',
      'pages': 380,
      'cover_image': 'assets/books/book2.jpg',
      'file_path': 'assets/books/book2.pdf',
      'category': 'خطب ودروس',
      'language': 'ar',
      'rating': 4.7,
      'download_count': 980,
      'is_favorite': 0,
      'user_id': 1,
    });

    // إدخال فصول الكتاب الأول
    final chapters1 = [
      {'title': 'المقدمة', 'subtitle': null, 'start_page': 1, 'end_page': 3},
      {'title': 'الأم أيتها الغالية', 'subtitle': 'خطبة عن بر الأم', 'start_page': 14, 'end_page': 19},
      {'title': 'الإسراء والمعراج', 'subtitle': 'معجزة الإسراء والمعراج', 'start_page': 20, 'end_page': 25},
      {'title': 'فضل شعبان', 'subtitle': 'التعريف بشهر شعبان', 'start_page': 26, 'end_page': 31},
      {'title': 'الإعداد لرمضان', 'subtitle': 'الاستعداد لشهر الصيام', 'start_page': 32, 'end_page': 37},
    ];

    for (var chapter in chapters1) {
      await db.insert('chapters', {
        'book_id': book1Id,
        ...chapter,
      });
    }

    // إدخال فصول الكتاب الثاني
    final chapters2 = [
      {'title': 'ضيف كريم يقرع الباب', 'subtitle': 'والصيام بين الجوع والخشوع', 'start_page': 2, 'end_page': 11},
      {'title': 'رمضان تخفيضات بالأسواق', 'subtitle': 'ربح وتجارة', 'start_page': 12, 'end_page': 18},
      {'title': 'رمضان دورة للصادات السبع', 'subtitle': 'الصوم - الصلاة - الصدقة', 'start_page': 19, 'end_page': 26},
      {'title': 'رمضان تاريخ أمة', 'subtitle': 'بدر وجهاد', 'start_page': 27, 'end_page': 33},
      {'title': 'العشر وليلة القدر', 'subtitle': null, 'start_page': 34, 'end_page': 41},
    ];

    for (var chapter in chapters2) {
      await db.insert('chapters', {
        'book_id': book2Id,
        ...chapter,
      });
    }
  }

  // دوال CRUD للمستخدمين
  Future<int> createUser(Map<String, dynamic> user) async {
    final db = await database;
    return await db.insert('users', user);
  }

  Future<Map<String, dynamic>?> getUserByEmail(String email) async {
    final db = await database;
    final result = await db.query(
      'users',
      where: 'email = ?',
      whereArgs: [email],
    );
    return result.isNotEmpty ? result.first : null;
  }

  Future<List<Map<String, dynamic>>> getAllBooks() async {
    final db = await database;
    return await db.query('books');
  }

  Future<List<Map<String, dynamic>>> getChaptersByBook(int bookId) async {
    final db = await database;
    return await db.query(
      'chapters',
      where: 'book_id = ?',
      whereArgs: [bookId],
    );
  }

  Future<void> addToFavorites(int userId, int bookId) async {
    final db = await database;
    await db.insert('favorites', {
      'user_id': userId,
      'book_id': bookId,
    });
    await db.update(
      'books',
      {'is_favorite': 1},
      where: 'id = ?',
      whereArgs: [bookId],
    );
  }

  Future<void> updateReadProgress(int chapterId, int progress) async {
    final db = await database;
    await db.update(
      'chapters',
      {
        'read_progress': progress,
        'last_read': DateTime.now().toIso8601String(),
      },
      where: 'id = ?',
      whereArgs: [chapterId],
    );
  }
}