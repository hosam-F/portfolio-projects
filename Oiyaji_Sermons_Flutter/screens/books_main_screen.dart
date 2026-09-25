import 'package:flutter/material.dart';

// استيراد نموذج الكتاب الصحيح
import '../models/book.dart';
import '../data/dummy_data.dart';
import 'book_detail_screen.dart';

class BooksMainScreen extends StatelessWidget {
  const BooksMainScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Book> books = DummyData.getBooks();

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'كتاب غاية المريد',
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            fontFamily: 'Tajawal',
          ),
        ),
        backgroundColor: const Color(0xFF1B5E20),
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: () => _showSearch(context, books),
            tooltip: 'بحث في الكتب',
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildHeaderSection(),
          const SizedBox(height: 20),
          _buildBooksGrid(books, context),
          const SizedBox(height: 30),
          _buildInfoSection(),
        ],
      ),
    );
  }

  Widget _buildHeaderSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'مؤلفات الشيخ محمد الجرافي',
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.bold,
            color: Color(0xFF1B5E20),
            fontFamily: 'Tajawal',
          ),
        ),
        const SizedBox(height: 8),
        const Text(
          'مجموعة الكتب والمؤلفات المتاحة للقراءة والاستماع',
          style: TextStyle(
            fontSize: 14,
            color: Color(0xFF757575),
            fontFamily: 'Tajawal',
          ),
        ),
        const SizedBox(height: 15),
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: const Color(0xFFE8F5E9),
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: const Color(0xFFC8E6C9)),
          ),
          child: const Row(
            children: [
              Icon(Icons.info_outline, color: Color(0xFF1B5E20), size: 20),
              SizedBox(width: 10),
              Expanded(
                child: Text(
                  'جميع الكتب متاحة للقراءة والتنزيل',
                  style: TextStyle(
                    fontSize: 13,
                    color: Color(0xFF1B5E20),
                    fontFamily: 'Tajawal',
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildBooksGrid(List<Book> books, BuildContext context) {
    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 15,
        mainAxisSpacing: 15,
        childAspectRatio: 0.75,
      ),
      itemCount: books.length,
      itemBuilder: (context, index) {
        return _buildBookCard(books[index], context);
      },
    );
  }

  Widget _buildBookCard(Book book, BuildContext context) {
    return Card(
      elevation: 3,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: InkWell(
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => BookDetailScreen(book: book),
            ),
          );
        },
        borderRadius: BorderRadius.circular(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // غلاف الكتاب
            Container(
              height: 140,
              decoration: const BoxDecoration(
                color: Color(0xFFE8F5E9),
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(12),
                  topRight: Radius.circular(12),
                ),
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    Color(0xFF1B5E20),
                    Color(0xFF4CAF50),
                  ],
                ),
              ),
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(
                      Icons.menu_book,
                      size: 50,
                      color: Colors.white,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      book.subtitle,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                        fontFamily: 'Tajawal',
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // معلومات الكتاب
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      book.title,
                      style: const TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF212121),
                        fontFamily: 'Tajawal',
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 5),
                    Text(
                      book.author,
                      style: const TextStyle(
                        fontSize: 12,
                        color: Color(0xFF757575),
                        fontFamily: 'Tajawal',
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      book.description,
                      style: const TextStyle(
                        fontSize: 11,
                        color: Color(0xFF616161),
                        fontFamily: 'Tajawal',
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const Spacer(),
                    Row(
                      children: [
                        const Icon(
                          Icons.menu_book,
                          size: 12,
                          color: Color(0xFF9E9E9E),
                        ),
                        const SizedBox(width: 4),
                        Text(
                          '${book.pages} صفحة',
                          style: const TextStyle(
                            fontSize: 11,
                            color: Color(0xFF757575),
                            fontFamily: 'Tajawal',
                          ),
                        ),
                        const Spacer(),
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 6,
                            vertical: 2,
                          ),
                          decoration: BoxDecoration(
                            color: const Color(0xFFE8F5E9),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: const Text(
                            'PDF',
                            style: TextStyle(
                              fontSize: 10,
                              color: Color(0xFF1B5E20),
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoSection() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFFF5F5F5),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFE0E0E0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'معلومات عن سلسلة غاية المريد',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Color(0xFF1B5E20),
              fontFamily: 'Tajawal',
            ),
          ),
          const SizedBox(height: 10),
          const Text(
            '"غاية المريد في الخطب والوعظ الرشيد" هي سلسلة تضم مجموعة من الخطب والدروس التي ألقاها الشيخ محمد الجرافي في مساجد مختلفة، تتناول مواضيع متنوعة في العقيدة والعبادات والأخلاق.',
            style: TextStyle(
              fontSize: 14,
              color: Color(0xFF616161),
              fontFamily: 'Tajawal',
              height: 1.6,
            ),
          ),
          const SizedBox(height: 15),
          _buildFeatureItem('متاحة للقراءة مباشرة'),
          _buildFeatureItem('قابلة للتنزيل للقراءة بدون إنترنت'),
          _buildFeatureItem('نصوص كاملة مع فهرس تفصيلي'),
          _buildFeatureItem('تصفح سهل ومنظم'),
        ],
      ),
    );
  }

  Widget _buildFeatureItem(String text) {
    return Padding(
        padding: const EdgeInsets.only(bottom: 8),
        child: Row(
          children: [
            const Icon(
              Icons.check_circle,
              size: 16,
              color: Color(0xFF4CAF50),
            ),
            const SizedBox(width: 8),
            Text(
              text,
              style: const TextStyle(
                fontSize: 13,
                color: Color(0xFF616161),
                fontFamily: 'Tajawal',
              ),
            ),
          ],
        )
    );
  }

  void _showSearch(BuildContext context, List<Book> books) {
    showSearch(
      context: context,
      delegate: _BookSearchDelegate(books: books),
    );
  }
}

class _BookSearchDelegate extends SearchDelegate {
  final List<Book> books;

  _BookSearchDelegate({required this.books});

  @override
  List<Widget> buildActions(BuildContext context) {
    return [
      IconButton(
        icon: const Icon(Icons.clear),
        onPressed: () => query = '',
      ),
    ];
  }

  @override
  Widget buildLeading(BuildContext context) {
    return IconButton(
      icon: const Icon(Icons.arrow_back),
      onPressed: () => close(context, null),
    );
  }

  @override
  Widget buildResults(BuildContext context) {
    final results = books.where((book) =>
    book.title.toLowerCase().contains(query.toLowerCase()) ||
        book.subtitle.toLowerCase().contains(query.toLowerCase()) ||
        book.author.toLowerCase().contains(query.toLowerCase()));

    if (results.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.search_off,
              size: 60,
              color: Color(0xFFE0E0E0),
            ),
            SizedBox(height: 20),
            Text(
              'لم يتم العثور على نتائج',
              style: TextStyle(
                fontSize: 18,
                color: Color(0xFF757575),
                fontFamily: 'Tajawal',
              ),
            ),
            SizedBox(height: 10),
            Text(
              'حاول بكلمات بحث مختلفة',
              style: TextStyle(
                fontSize: 14,
                color: Color(0xFFBDBDBD),
                fontFamily: 'Tajawal',
              ),
            ),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: results.length,
      itemBuilder: (context, index) {
        final book = results.elementAt(index);
        return Card(
          margin: const EdgeInsets.only(bottom: 10),
          child: ListTile(
            leading: Container(
              width: 50,
              height: 70,
              decoration: BoxDecoration(
                color: const Color(0xFFE8F5E9),
                borderRadius: BorderRadius.circular(5),
              ),
              child: const Icon(
                Icons.book,
                color: Color(0xFF1B5E20),
              ),
            ),
            title: Text(
              book.title,
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                fontFamily: 'Tajawal',
              ),
            ),
            subtitle: Text(
              book.subtitle,
              style: const TextStyle(
                fontSize: 12,
                color: Color(0xFF757575),
                fontFamily: 'Tajawal',
              ),
            ),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => BookDetailScreen(book: book),
                ),
              );
            },
          ),
        );
      },
    );
  }

  @override
  Widget buildSuggestions(BuildContext context) {
    final suggestions = books.take(3).toList();

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: suggestions.length,
      itemBuilder: (context, index) {
        final book = suggestions[index];
        return ListTile(
          leading: const Icon(Icons.search, color: Color(0xFF757575)),
          title: Text(
            book.title,
            style: const TextStyle(fontFamily: 'Tajawal'),
          ),
          subtitle: Text(
            book.subtitle,
            style: const TextStyle(
              fontSize: 12,
              color: Color(0xFF9E9E9E),
              fontFamily: 'Tajawal',
            ),
          ),
          onTap: () {
            query = book.title;
            showResults(context);
          },
        );
      },
    );
  }
}