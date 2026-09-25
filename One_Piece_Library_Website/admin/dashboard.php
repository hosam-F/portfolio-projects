<?php
declare(strict_types=1);
session_start();
require __DIR__ . '/../db.php';
if (empty($_SESSION['admin_id'])) { header('Location: login.php'); exit; }
$pdo = db();
if (!$pdo) { exit('Database is not configured.'); }
if (empty($_SESSION['csrf'])) { $_SESSION['csrf'] = bin2hex(random_bytes(32)); }
$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST' && hash_equals($_SESSION['csrf'], (string)($_POST['csrf'] ?? ''))) {
    $type = $_POST['type'] ?? '';
    if ($type === 'product') {
        $statement = $pdo->prepare('INSERT INTO products (name, category, description, price, image_url) VALUES (?, ?, ?, ?, ?)');
        $price = trim((string)($_POST['price'] ?? ''));
        $statement->execute([trim((string)$_POST['name']), trim((string)$_POST['category']), trim((string)$_POST['description']), $price === '' ? null : $price, trim((string)$_POST['image_url'])]);
        $message = 'تمت إضافة المنتج.';
    } elseif ($type === 'announcement') {
        $statement = $pdo->prepare('INSERT INTO announcements (title, body, image_url) VALUES (?, ?, ?)');
        $statement->execute([trim((string)$_POST['title']), trim((string)$_POST['body']), trim((string)$_POST['image_url'])]);
        $message = 'تمت إضافة الإعلان.';
    }
}
?><!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>لوحة الإدارة</title><link rel="stylesheet" href="../styles.css"></head><body><main class="section"><div class="container admin-box"><p><a href="logout.php">تسجيل الخروج</a></p><h1>إدارة المحتوى</h1><?php if ($message): ?><p class="success"><?= h($message) ?></p><?php endif; ?><h2>إضافة منتج</h2><form method="post"><input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>"><input type="hidden" name="type" value="product"><label>الاسم<input name="name" required></label><label>التصنيف<input name="category" required></label><label>الوصف<textarea name="description" required></textarea></label><label>السعر (اختياري)<input name="price" inputmode="decimal"></label><label>مسار الصورة (اختياري)<input name="image_url"></label><button type="submit">حفظ المنتج</button></form><h2>إضافة إعلان</h2><form method="post"><input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>"><input type="hidden" name="type" value="announcement"><label>العنوان<input name="title" required></label><label>النص<textarea name="body" required></textarea></label><label>مسار الصورة (اختياري)<input name="image_url"></label><button type="submit">حفظ الإعلان</button></form></div></main></body></html>
