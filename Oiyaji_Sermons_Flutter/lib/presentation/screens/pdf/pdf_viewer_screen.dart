import 'package:flutter/material.dart';
import 'package:advance_pdf_viewer/advance_pdf_viewer.dart';

class PDFViewerScreen extends StatefulWidget {
  final String pdfPath;
  final String bookTitle;

  const PDFViewerScreen({
    Key? key,
    required this.pdfPath,
    required this.bookTitle,
  }) : super(key: key);

  @override
  State<PDFViewerScreen> createState() => _PDFViewerScreenState();
}

class _PDFViewerScreenState extends State<PDFViewerScreen> {
  PDFDocument? _document;
  bool _isLoading = true;
  int _currentPage = 0;
  int? _totalPages;

  @override
  void initState() {
    super.initState();
    _loadPDF();
  }

  Future<void> _loadPDF() async {
    try {
      final document = await PDFDocument.fromAsset(widget.pdfPath);
      setState(() {
        _document = document;
        _totalPages = document.count;
        _isLoading = false;
      });
    } catch (e) {
      // إذا فشل تحميل الملف من الأصول، جرب طريقة بديلة
      _showAlternativeView();
    }
  }

  void _showAlternativeView() {
    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          widget.bookTitle,
          style: const TextStyle(fontSize: 16),
        ),
        backgroundColor: const Color(0xFF1B5E20),
        actions: [
          if (_totalPages != null)
            Padding(
              padding: const EdgeInsets.only(right: 16, top: 16),
              child: Text(
                '$_currentPage / $_totalPages',
                style: const TextStyle(fontSize: 14),
              ),
            ),
        ],
      ),
      body: _buildBody(),
      bottomNavigationBar: _buildBottomBar(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(
        child: CircularProgressIndicator(
          color: Color(0xFF1B5E20),
        ),
      );
    }

    if (_document != null) {
      return PDFViewer(
        document: _document!,
        zoomSteps: 1,
        scrollDirection: Axis.vertical,
        onPageChanged: (page) {
          setState(() {
            _currentPage = page + 1;
          });
        },
        progressIndicator: const CircularProgressIndicator(
          color: Color(0xFF1B5E20),
        ),
        pickerButtonColor: const Color(0xFF1B5E20),
      );
    }

    // عرض بديل إذا لم يتم تحميل PDF
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.picture_as_pdf,
              size: 100,
              color: Color(0xFF1B5E20),
            ),
            const SizedBox(height: 20),
            Text(
              widget.bookTitle,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Color(0xFF1B5E20),
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 10),
            const Text(
              'ملف PDF',
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey,
              ),
            ),
            const SizedBox(height: 30),
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 20),
              child: Text(
                'لقراءة الكتاب، يمكنك فتح ملف PDF باستخدام تطبيق قارئ PDF الموجود على جهازك',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 14),
              ),
            ),
            const SizedBox(height: 40),
            ElevatedButton.icon(
              onPressed: () {
                // افتح الملف باستخدام تطبيق خارجي
              },
              icon: const Icon(Icons.open_in_browser),
              label: const Text('فتح في تطبيق خارجي'),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF1B5E20),
                padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 15),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget? _buildBottomBar() {
    if (_document == null) return null;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border(top: BorderSide(color: Colors.grey[300]!)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          IconButton(
            icon: const Icon(Icons.zoom_in),
            onPressed: () {
              // تكبير
            },
          ),
          IconButton(
            icon: const Icon(Icons.zoom_out),
            onPressed: () {
              // تصغير
            },
          ),
          IconButton(
            icon: const Icon(Icons.bookmark),
            onPressed: () {
              // إضافة علامة
            },
          ),
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: () {
              // مشاركة
            },
          ),
        ],
      ),
    );
  }
}