import 'package:flutter/material.dart';
import 'package:oiyajiapp/utils/colors.dart';

class AppDrawer extends StatelessWidget {
  const AppDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          DrawerHeader(
            decoration: BoxDecoration(
              color: AppColors.primaryColor,
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const CircleAvatar(
                  radius: 30,
                  backgroundColor: Colors.white,
                  child: Icon(
                    Icons.person,
                    size: 40,
                    color: AppColors.primaryColor,
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  'خطب ودروس',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  'الشيخ محمد الجرافي',
                  style: TextStyle(
                    color: Colors.white.withOpacity(0.9),
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ),
          ListTile(
            leading: const Icon(Icons.home),
            title: const Text('الرئيسية'),
            onTap: () {
              Navigator.pop(context);
              Navigator.pushReplacementNamed(context, '/');
            },
          ),
          ListTile(
            leading: const Icon(Icons.menu_book),
            title: const Text('كتاب غاية المريد'),
            onTap: () {
              Navigator.pop(context);
              Navigator.pushNamed(context, '/books');
            },
          ),
          ListTile(
            leading: const Icon(Icons.mic),
            title: const Text('أسماء الله الحسنى'),
            onTap: () {
              Navigator.pop(context);
              Navigator.pushNamed(context, '/sermons');
            },
          ),
          ListTile(
            leading: const Icon(Icons.video_library),
            title: const Text('الدروس الرمضانية'),
            onTap: () {
              Navigator.pop(context);
              Navigator.pushNamed(context, '/videos');
            },
          ),
          ListTile(
            leading: const Icon(Icons.lightbulb),
            title: const Text('من وحي القرآن'),
            onTap: () {
              Navigator.pop(context);
              Navigator.pushNamed(context, '/inspirations');
            },
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.info),
            title: const Text('عن التطبيق'),
            onTap: () {
              // عرض معلومات عن التطبيق
            },
          ),
          ListTile(
            leading: const Icon(Icons.share),
            title: const Text('مشاركة التطبيق'),
            onTap: () {
              // مشاركة التطبيق
            },
          ),
          ListTile(
            leading: const Icon(Icons.settings),
            title: const Text('الإعدادات'),
            onTap: () {
              // فتح الإعدادات
            },
          ),
        ],
      ),
    );
  }
}