import 'book.dart';
import 'chapter.dart';

class BookContent {
  // كتاب غاية المريد - الجزء الأول
  static Book getBook1() {
    return Book(
      id: '1',
      title: 'غاية المريد في الخطب والوعظ الرشيد',
      subtitle: 'الجزء الأول',
      description: 'مجموعة خطب ودروس قيمة للشيخ محمد الجرافي، تتناول مواضيع متنوعة في العقيدة والعبادات والأخلاق',
      coverImage: 'assets/books/book1_cover.jpg',
      pages: 400,
      author: 'الشيخ محمد الجرافي',
      publishDate: '2023',
      filePath: 'assets/books/book1.pdf',
      chapters: _getBook1Chapters(),
      addedDate: DateTime(2024, 1, 1), // المطلوب
      category: 'خطب ودروس',
      language: 'العربية',
      rating: 4.8,
      downloadCount: 1250,
      isFeatured: true,
      isDownloaded: false,
    );
  }

  // كتاب غاية المريد - الجزء الثاني
  static Book getBook2() {
    return Book(
      id: '2',
      title: 'غاية المريد في الخطب والوعظ الرشيد',
      subtitle: 'الجزء الثاني',
      description: 'تكملة لمجموعة الخطب والدروس، يتناول مواضيع جديدة في السيرة والقصص القرآني',
      coverImage: 'assets/books/book2_cover.jpg',
      pages: 380,
      author: 'الشيخ محمد الجرافي',
      publishDate: '2023',
      filePath: 'assets/books/book2.pdf',
      chapters: _getBook2Chapters(),
      addedDate: DateTime(2024, 1, 15), // المطلوب
      category: 'خطب ودروس',
      language: 'العربية',
      rating: 4.7,
      downloadCount: 980,
      isFeatured: true,
      isDownloaded: false,
    );
  }

  static List<Book> getAllBooks() {
    return [getBook1(), getBook2()];
  }

  // فصول الجزء الأول
  static List<BookChapter> _getBook1Chapters() {
    return const [
      BookChapter(
        id: 'intro',
        title: 'المقدمة',
        startPage: 1,
        endPage: 3,
        content: 'بسم الله الرحمن الرحيم، الحمد لله رب العالمين...',
      ),
      BookChapter(
        id: 'toc',
        title: 'فهرس المحتويات',
        startPage: 4,
        endPage: 6,
      ),
      BookChapter(
        id: '1',
        title: 'الأم أيتها الغالية',
        subtitle: 'خطبة عن بر الأم',
        startPage: 14,
        endPage: 19,
        content: 'عن أبي هريرة رضي الله عنه قال: جاء رجل إلى رسول الله صلى الله عليه وسلم...',
      ),
      BookChapter(
        id: '2',
        title: 'الإسراء والمعراج',
        subtitle: 'معجزة الإسراء والمعراج',
        startPage: 20,
        endPage: 25,
        content: 'سبحان الذي أسرى بعبده ليلاً من المسجد الحرام إلى المسجد الأقصى...',
      ),
      BookChapter(
        id: '3',
        title: 'فضل شعبان',
        subtitle: 'التعريف بشهر شعبان',
        startPage: 26,
        endPage: 31,
        content: 'كان رسول الله صلى الله عليه وسلم يصوم أكثر شعبان...',
      ),
      BookChapter(
        id: '4',
        title: 'الإعداد لرمضان',
        subtitle: 'الاستعداد لشهر الصيام',
        startPage: 32,
        endPage: 37,
      ),
      BookChapter(
        id: '5',
        title: 'بين يدي رمضان',
        subtitle: 'التهيئة لشهر رمضان',
        startPage: 38,
        endPage: 43,
      ),
      BookChapter(
        id: '6',
        title: 'رمضان شهر التغيير',
        subtitle: 'دور رمضان في تغيير النفس',
        startPage: 44,
        endPage: 49,
      ),
      BookChapter(
        id: '7',
        title: 'أول جمعة من رمضان',
        subtitle: 'فضائل ومسائل',
        startPage: 50,
        endPage: 55,
      ),
      BookChapter(
        id: '8',
        title: 'رمضان شهر الأخلاق',
        subtitle: 'الأخلاق في رمضان',
        startPage: 56,
        endPage: 65,
      ),
      BookChapter(
        id: '9',
        title: 'العشر وليلة القدر',
        subtitle: 'فضائل العشر الأواخر',
        startPage: 66,
        endPage: 72,
      ),
      BookChapter(
        id: '10',
        title: 'في وداع رمضان',
        subtitle: 'خاتمة الشهر الفضيل',
        startPage: 73,
        endPage: 79,
      ),
      BookChapter(
        id: '11',
        title: 'وجوب الاستقامة',
        subtitle: 'الاستقامة على الطاعات',
        startPage: 80,
        endPage: 86,
      ),
      BookChapter(
        id: '12',
        title: 'أسباب قبول الأعمال',
        subtitle: 'شروط القبول',
        startPage: 87,
        endPage: 93,
      ),
      BookChapter(
        id: '13',
        title: 'خصومات الكبار',
        subtitle: 'أخلاقيات الخلاف',
        startPage: 94,
        endPage: 101,
      ),
      BookChapter(
        id: '14',
        title: 'العفة والعفاف',
        subtitle: 'قيم الإسلام',
        startPage: 102,
        endPage: 108,
      ),
      BookChapter(
        id: '15',
        title: 'الميراث',
        subtitle: 'حقوق ومخالفات',
        startPage: 109,
        endPage: 116,
      ),
      BookChapter(
        id: '16',
        title: 'السنون الخداعة',
        subtitle: 'التفكر في الزمن',
        startPage: 117,
        endPage: 124,
      ),
      BookChapter(
        id: '17',
        title: 'الشوق إلى الله',
        subtitle: 'الرحلة الروحية',
        startPage: 125,
        endPage: 131,
      ),
      BookChapter(
        id: '18',
        title: 'العشر من ذي الحجة (1)',
        subtitle: 'فضل الأيام العشر',
        startPage: 132,
        endPage: 138,
      ),
      BookChapter(
        id: '19',
        title: 'العشر من ذي الحجة (2)',
        subtitle: 'العمل الصالح',
        startPage: 139,
        endPage: 144,
      ),
      BookChapter(
        id: '20',
        title: 'يوم عرفة',
        subtitle: 'قفات وفضل',
        startPage: 145,
        endPage: 154,
      ),
    ];
  }

  // فصول الجزء الثاني
  static List<BookChapter> _getBook2Chapters() {
    return const [
      BookChapter(
        id: '1',
        title: 'ضيف كريم يقرع الباب',
        subtitle: 'والصيام بين الجوع والخشوع',
        startPage: 2,
        endPage: 11,
      ),
      BookChapter(
        id: '2',
        title: 'رمضان تخفيضات بالأسواق',
        subtitle: 'ربح وتجارة',
        startPage: 12,
        endPage: 18,
      ),
      BookChapter(
        id: '3',
        title: 'رمضان دورة للصادات السبع',
        subtitle: 'الصوم - الصلاة - الصدقة',
        startPage: 19,
        endPage: 26,
      ),
      BookChapter(
        id: '4',
        title: 'رمضان تاريخ أمة',
        subtitle: 'بدر وجهاد',
        startPage: 27,
        endPage: 33,
      ),
      BookChapter(
        id: '5',
        title: 'العشر وليلة القدر',
        startPage: 34,
        endPage: 41,
      ),
      BookChapter(
        id: '6',
        title: 'وداعاً رمضان',
        startPage: 42,
        endPage: 50,
      ),
      BookChapter(
        id: '7',
        title: 'ما بعد رمضان',
        subtitle: 'عطاء واستمرار',
        startPage: 51,
        endPage: 57,
      ),
      BookChapter(
        id: '8',
        title: 'انطلقت الشياطين',
        subtitle: 'فكانت صلاة الفجر أول الضحايا',
        startPage: 58,
        endPage: 64,
      ),
      BookChapter(
        id: '9',
        title: 'غزوة أحد - دروس وعبر (1)',
        startPage: 65,
        endPage: 72,
      ),
      BookChapter(
        id: '10',
        title: 'غزوة أحد - دروس وعبر (2)',
        startPage: 73,
        endPage: 80,
      ),
      BookChapter(
        id: '11',
        title: 'المسجد الأقصى',
        subtitle: 'واجب المسلمين',
        startPage: 81,
        endPage: 89,
      ),
      BookChapter(
        id: '12',
        title: 'الحج شوق ومحبة',
        subtitle: 'وعوض ورحمة',
        startPage: 90,
        endPage: 97,
      ),
      BookChapter(
        id: '13',
        title: 'الحج المبرور',
        startPage: 98,
        endPage: 105,
      ),
      BookChapter(
        id: '14',
        title: 'الحج مقاصد وأسرار',
        subtitle: 'ومنافع',
        startPage: 106,
        endPage: 113,
      ),
      BookChapter(
        id: '15',
        title: 'العشر وعرفة',
        startPage: 114,
        endPage: 125,
      ),
      BookChapter(
        id: '16',
        title: 'ماذا بعد الحج',
        subtitle: 'صلاح وذكر',
        startPage: 126,
        endPage: 132,
      ),
      BookChapter(
        id: '17',
        title: 'نهاية العام',
        subtitle: 'محاسبة وتوبة',
        startPage: 133,
        endPage: 140,
      ),
      BookChapter(
        id: '18',
        title: 'سلسلة خطب عن الهجرة (1)',
        subtitle: 'الهجرة عظمة ومعنى',
        startPage: 141,
        endPage: 147,
      ),
      BookChapter(
        id: '19',
        title: 'سلسلة خطب عن الهجرة (2)',
        subtitle: 'الهجرة وعاشوراء',
        startPage: 148,
        endPage: 155,
      ),
      BookChapter(
        id: '20',
        title: 'شرح آية الهجرة (1)',
        subtitle: 'في الغار',
        startPage: 156,
        endPage: 162,
      ),
    ];
  }
}