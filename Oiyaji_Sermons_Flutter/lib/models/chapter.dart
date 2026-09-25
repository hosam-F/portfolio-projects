class BookChapter {
  final String id;
  final String title;
  final String? subtitle;
  final int startPage;
  final int endPage;
  final String? content;
  final String? duration;
  final String? audioUrl;
  final String? videoUrl;

  const BookChapter({
    required this.id,
    required this.title,
    this.subtitle,
    required this.startPage,
    required this.endPage,
    this.content,
    this.duration,
    this.audioUrl,
    this.videoUrl,
  });
}