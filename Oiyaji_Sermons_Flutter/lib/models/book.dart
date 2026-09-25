import 'chapter.dart';

class Book {
  final String id;
  final String title;
  final String subtitle;
  final String description;
  final String coverImage;
  final int pages;
  final String author;
  final String publishDate;
  final String filePath;
  final List<BookChapter> chapters;
  final String category;
  final String language;
  final double rating;
  final int downloadCount;
  final DateTime addedDate;
  final bool isFeatured;
  final bool isDownloaded;

  const Book({
    required this.id,
    required this.title,
    required this.subtitle,
    required this.description,
    required this.coverImage,
    required this.pages,
    required this.author,
    required this.publishDate,
    required this.filePath,
    required this.chapters,
    this.category = 'خطب ودروس',
    this.language = 'العربية',
    this.rating = 0.0,
    this.downloadCount = 0,
    required this.addedDate,
    this.isFeatured = false,
    this.isDownloaded = false,
  });
}