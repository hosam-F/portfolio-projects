<?php
declare(strict_types=1);
require __DIR__ . '/db.php';
$pdo = db();
$products = [];
$announcements = [];
if ($pdo) {
    $products = $pdo->query('SELECT name, category, description, price, image_url FROM products WHERE is_active = 1 ORDER BY created_at DESC')->fetchAll();
    $announcements = $pdo->query('SELECT title, body, image_url FROM announcements WHERE is_active = 1 ORDER BY published_at DESC LIMIT 6')->fetchAll();
}
if (!$products) {
    $products = [
        ['name' => 'الأدوات المدرسية', 'category' => 'الأدوات المدرسية', 'description' => 'دفاتر وأقلام ومستلزمات الدراسة.', 'price' => null, 'image_url' => null],
        ['name' => 'مستلزمات الجوال', 'category' => 'الجوال', 'description' => 'توصيلات وذواكر وإكسسوارات متنوعة.', 'price' => null, 'image_url' => null],
        ['name' => 'خدمات الطباعة', 'category' => 'الطباعة', 'description' => 'طباعة وإخراج وتجهيز الصور والوثائق.', 'price' => null, 'image_url' => null],
    ];
}
?><!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>مكتبة ون بيس | مستلزمات دراسية وجوال وحفلات</title>
<meta name="description" content="مكتبة ون بيس في مدينة جبلة: مستلزمات مدرسية، طباعة، هدايا، تجهيز مناسبات، ومستلزمات جوال.">
<link rel="canonical" href="https://YOUR-DOMAIN.example/">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header><div class="container"><nav><a href="#about">عن المكتبة</a><a href="#products">المنتجات</a><a href="#announcements">الإعلانات</a><a href="#services">الخدمات</a><a href="#contact">تواصل</a></nav></div></header>
<main>
<section id="about" class="hero container"><img src="images/alshear.jpg" alt="شعار مكتبة ون بيس"><div><p class="eyebrow">مكتبة ون بيس — مدينة جبلة</p><h1>كل ما تحتاجه للدراسة والهدايا والمناسبات</h1><p>مستلزمات مدرسية، طباعة وإخراج، هدايا، تجهيز حفلات، ومستلزمات جوال في مكان واحد.</p></div></section>
<?php if ($announcements): ?><section id="announcements" class="section"><div class="container"><h2>آخر الإعلانات</h2><div class="card-grid"><?php foreach ($announcements as $item): ?><article class="card"><?php if (!empty($item['image_url'])): ?><img src="<?= h($item['image_url']) ?>" alt=""><?php endif; ?><h3><?= h($item['title']) ?></h3><p><?= nl2br(h($item['body'])) ?></p></article><?php endforeach; ?></div></div></section><?php endif; ?>
<section id="products" class="section"><div class="container"><h2>المنتجات والخدمات</h2><div class="card-grid"><?php foreach ($products as $item): ?><article class="card"><?php if (!empty($item['image_url'])): ?><img src="<?= h($item['image_url']) ?>" alt="<?= h($item['name']) ?>"><?php endif; ?><span class="tag"><?= h($item['category']) ?></span><h3><?= h($item['name']) ?></h3><p><?= nl2br(h($item['description'])) ?></p><?php if ($item['price'] !== null): ?><strong><?= h((string)$item['price']) ?></strong><?php endif; ?></article><?php endforeach; ?></div></div></section>
<section id="services" class="section"><div class="container"><h2>خدمات المكتبة</h2><div class="feature-list"><div>طباعة وإخراج</div><div>تجهيز مناسبات</div><div>هدايا وثيمات</div><div>مستلزمات الجوال</div></div></div></section>
<section id="contact" class="section"><div class="container"><h2>تواصل معنا</h2><p>تُضاف بيانات التواصل العامة المعتمدة من مالك المكتبة في ملف الإعداد أو هذه الصفحة قبل النشر النهائي.</p></div></section>
</main><footer><p>© مكتبة ون بيس — مدينة جبلة</p></footer>
</body></html>
