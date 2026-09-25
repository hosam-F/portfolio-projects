class AppStrings {
  static Map<String, Map<String, String>> translations = {
    'ar': {
      'app_title': 'خطب ودروس الشيخ محمد الجرافي',
      'login': 'تسجيل الدخول',
      'register': 'إنشاء حساب',
      'email': 'البريد الإلكتروني',
      'password': 'كلمة المرور',
      'name': 'الاسم',
      'confirm_password': 'تأكيد كلمة المرور',
      'home': 'الرئيسية',
      'books': 'الكتب',
      'lessons': 'الدروس',
      'favorites': 'المفضلة',
      'downloads': 'الملفات المحملة',
      'settings': 'الإعدادات',
      'about': 'عن التطبيق',
      'logout': 'تسجيل الخروج',
      'language': 'اللغة',
      'arabic': 'العربية',
      'english': 'الإنجليزية',
      'theme': 'الوضع',
      'dark': 'داكن',
      'light': 'فاتح',
      'search': 'بحث',
      'read': 'قراءة',
      'download': 'تنزيل',
      'share': 'مشاركة',
      'author': 'المؤلف',
      'pages': 'صفحات',
      'chapters': 'فصول',
      'no_internet': 'لا يوجد اتصال بالإنترنت',
      'error': 'حدث خطأ',
      'try_again': 'حاول مرة أخرى',
      'welcome': 'مرحباً',
      'sheikh_name': 'الشيخ محمد الجرافي',
      'sheikh_title': 'داعية ومؤلف إسلامي',
    },
    'en': {
      'app_title': 'Sheikh Muhammad Al-Jarafi - Sermons & Lessons',
      'login': 'Login',
      'register': 'Register',
      'email': 'Email',
      'password': 'Password',
      'name': 'Name',
      'confirm_password': 'Confirm Password',
      'home': 'Home',
      'books': 'Books',
      'lessons': 'Lessons',
      'favorites': 'Favorites',
      'downloads': 'Downloads',
      'settings': 'Settings',
      'about': 'About',
      'logout': 'Logout',
      'language': 'Language',
      'arabic': 'Arabic',
      'english': 'English',
      'theme': 'Theme',
      'dark': 'Dark',
      'light': 'Light',
      'search': 'Search',
      'read': 'Read',
      'download': 'Download',
      'share': 'Share',
      'author': 'Author',
      'pages': 'Pages',
      'chapters': 'Chapters',
      'no_internet': 'No Internet Connection',
      'error': 'Error',
      'try_again': 'Try Again',
      'welcome': 'Welcome',
      'sheikh_name': 'Sheikh Muhammad Al-Jarafi',
      'sheikh_title': 'Islamic Scholar & Author',
    },
  };
}

class LanguageManager {
  static String currentLanguage = 'ar';

  static String get(String key) {
    return translations[currentLanguage]?[key] ?? key;
  }

  static void setLanguage(String lang) {
    currentLanguage = lang;
  }
}