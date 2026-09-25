<?php
declare(strict_types=1);
session_start();
require __DIR__ . '/../db.php';
$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim((string)($_POST['email'] ?? ''));
    $password = (string)($_POST['password'] ?? '');
    $pdo = db();
    if ($pdo && filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $statement = $pdo->prepare('SELECT id, email, password_hash FROM admins WHERE email = ? LIMIT 1');
        $statement->execute([$email]);
        $admin = $statement->fetch();
        if ($admin && password_verify($password, $admin['password_hash'])) {
            session_regenerate_id(true);
            $_SESSION['admin_id'] = (int)$admin['id'];
            header('Location: dashboard.php');
            exit;
        }
    }
    $error = 'بيانات الدخول غير صحيحة أو قاعدة البيانات غير مهيأة.';
}
?><!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>دخول الإدارة</title><link rel="stylesheet" href="../styles.css"></head><body><main class="section"><div class="container admin-box"><h1>إدارة مكتبة ون بيس</h1><?php if ($error): ?><p class="error"><?= h($error) ?></p><?php endif; ?><form method="post"><label>البريد الإلكتروني<input type="email" name="email" required autocomplete="username"></label><label>كلمة المرور<input type="password" name="password" required autocomplete="current-password"></label><button type="submit">دخول</button></form></div></main></body></html>
