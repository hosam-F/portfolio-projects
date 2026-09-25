class Sermon {
  final String id;
  final String title;
  final String description;
  final String duration;
  final String mosque;
  final DateTime date;
  final String url;

  Sermon({
    required this.id,
    required this.title,
    required this.description,
    required this.duration,
    required this.mosque,
    required this.date,
    required this.url,
  });
}