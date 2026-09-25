import 'package:flutter/material.dart';
import 'chapter_screen.dart';
import 'pdf_viewer_screen.dart';
import 'package:oiyajiapp/models/book.dart';

class BookDetailScreen extends StatelessWidget {
  final Book book;

  const BookDetailScreen({super.key, required this.book});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(book.title),
        backgroundColor: const Color(0xFF1B5E20),
        actions: [
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: () => _shareBook(context),
          ),
          PopupMenuButton(
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'download',
                child: ListTile(
                  leading: Icon(Icons.download),
                  title: Text('تنزيل الكتاب'),
                ),
              ),
              const PopupMenuItem(
                value: 'favorite',
                child: ListTile(
                  leading: Icon(Icons.favorite_border),
                  title: Text('إضافة للمفضلة'),
                ),
              ),
            ],
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // غلاف الكتاب
            Container(
              height: 220,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    const Color(0xFF1B5E20).withOpacity(0.9),
                    const Color(0xFF4CAF50).withOpacity(0.7),
                  ],
                ),
              ),
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.menu_book, size: 80, color: Colors.white),
                    const SizedBox(height: 15),
                    Text(
                      book.subtitle,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 5),
                    Text(
                      '${book.pages} صفحة',
                      style: const TextStyle(color: Colors.white70),
                    ),
                  ],
                ),
              ),
            ),

            // معلومات الكتاب
            Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // وصف الكتاب
                  Text(
                    'عن الكتاب',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.grey[800],
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    book.description,
                    style: const TextStyle(fontSize: 15, height: 1.6),
                  ),
                  const SizedBox(height: 20),

                  // معلومات تفصيلية
                  _buildInfoRow('المؤلف:', book.author),
                  _buildInfoRow('تاريخ النشر:', book.publishDate),
                  _buildInfoRow('عدد الصفحات:', '${book.pages} صفحة'),
                  _buildInfoRow('عدد الفصول:', '${book.chapters.length} فصل'),

                  const SizedBox(height: 30),

                  // أزرار الإجراءات
                  Row(
                    children: [
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () => _openPDF(context),
                          icon: const Icon(Icons.picture_as_pdf),
                          label: const Text('فتح PDF'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF1B5E20),
                            padding: const EdgeInsets.symmetric(vertical: 15),
                          ),
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: OutlinedButton.icon(
                          onPressed: () => _downloadBook(),
                          icon: const Icon(Icons.download),
                          label: const Text('تنزيل'),
                          style: OutlinedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 15),
                            side: const BorderSide(color: Color(0xFF1B5E20)),
                          ),
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 30),

                  // فهرس المحتويات
                  Text(
                    'فهرس المحتويات',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.grey[800],
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    'إجمالي ${book.chapters.length} فصل',
                    style: const TextStyle(color: Colors.grey),
                  ),
                  const SizedBox(height: 15),

                  // قائمة الفصول
                  ...book.chapters.map((chapter) {
                    return Card(
                      margin: const EdgeInsets.only(bottom: 10),
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: const Color(0xFFE8F5E9),
                          child: Text(
                            chapter.id.length <= 2 ? chapter.id : 'ف',
                            style: const TextStyle(color: Color(0xFF1B5E20)),
                          ),
                        ),
                        title: Text(chapter.title),
                        subtitle: chapter.subtitle != null
                            ? Text('${chapter.subtitle} - الصفحات ${chapter.startPage}-${chapter.endPage}')
                            : Text('الصفحات ${chapter.startPage}-${chapter.endPage}'),
                        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => ChapterScreen(
                                chapter: chapter,
                                bookTitle: book.title,
                              ),
                            ),
                          );
                        },
                      ),
                    );
                  }).toList(),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 100,
            child: Text(
              label,
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                color: Colors.grey,
              ),
            ),
          ),
          Expanded(child: Text(value)),
        ],
      ),
    );
  }

  void _openPDF(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => PDFViewerScreen(
          pdfPath: book.filePath,
          bookTitle: book.title,
        ),
      ),
    );
  }

  void _downloadBook() {
    // تنزيل الكتاب
    // يمكن إضافة منطق التنزيل هنا
  }

  void _shareBook(BuildContext context) {
    // مشاركة الكتاب
  }
}