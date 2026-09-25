import '../models/book.dart';
import '../models/chapter.dart';

class DummyData {
  static List<Book> getBooks() {
    return [
      Book(
        id: '1',
        title: 'غاية المريد في الخطب والوعظ الرشيد',
        subtitle: 'الجزء الأول',
        description: 'مجموعة خطب ودروس قيمة للشيخ محمد الجرافي',
        coverImage: 'assets/books/book1_cover.jpg',
        pages: 400,
        author: 'الشيخ محمد الجرافي',
        publishDate: '2023',
        filePath: 'assets/books/book1.pdf',
        chapters: [
          BookChapter(
            id: '1',
            title: 'الأم أيتها الغالية',
            subtitle: 'خطبة عن بر الأم',
            startPage: 14,
            endPage: 19,
          ),
        ],
        category: 'خطب ودروس',
        language: 'العربية',
        rating: 4.8,
        downloadCount: 1250,
        addedDate: DateTime(2024, 1, 1),
        isFeatured: true,
        isDownloaded: false,
      ),
      Book(
        id: '2',
        title: 'غاية المريد في الخطب والوعظ الرشيد',
        subtitle: 'الجزء الثاني',
        description: 'تكملة لمجموعة الخطب والدروس',
        coverImage: 'assets/books/book2_cover.jpg',
        pages: 380,
        author: 'الشيخ محمد الجرافي',
        publishDate: '2023',
        filePath: 'assets/books/book2.pdf',
        chapters: [
          BookChapter(
            id: '1',
            title: 'ضيف كريم يقرع الباب',
            subtitle: 'والصيام بين الجوع والخشوع',
            startPage: 2,
            endPage: 11,
          ),
        ],
        category: 'خطب ودروس',
        language: 'العربية',
        rating: 4.7,
        downloadCount: 980,
        addedDate: DateTime(2024, 1, 15),
        isFeatured: true,
        isDownloaded: false,
      ),
    ];
  }
}