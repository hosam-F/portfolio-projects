class Lesson {
  final String id;
  final String title;
  final String description;
  final String date;
  final String duration;
  final String videoUrl;
  final String? audioUrl;

  Lesson({
    required this.id,
    required this.title,
    required this.description,
    required this.date,
    required this.duration,
    required this.videoUrl,
    this.audioUrl,
  });
}