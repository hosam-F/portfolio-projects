import sys
from pathlib import Path

from PySide6.QtCore import QEventLoop, QTimer, Qt
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QBoxLayout,
    QFrame,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QInputDialog,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QDialog,
    QPushButton,
    QScrollArea,
    QSplashScreen,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from quran_educator.presentation.controller import ControlledAppController
from quran_educator.presentation.package_smoke import run_packaged_smoke
from quran_educator.infrastructure.productization import startup_contract, configure_local_logging
from quran_educator.infrastructure.auth import LocalAuthService
from quran_educator.application.authorization import AuthorizationContext, AuthorizationPolicy
from quran_educator.presentation.navigation import NavigationItem, PersistentNavigation, ViewRouter
from quran_educator.presentation.views import (
    AttendanceView,
    AuditView,
    BackupRestoreView,
    CurriculumView,
    DashboardView,
    OrganizationView,
    ProgressObservationView,
    ReportsView,
    StudentsView,
    ViewSpec,
)


PRODUCT_NAME = "دليل المربي القرآني | صُنّاع المربي والمفكر"
PRODUCT_SHORT_NAME = "دليل المربي القرآني"



def _asset_path(name: str) -> Path:
    return Path(__file__).resolve().parent / "assets" / name


class WelcomeSplash(QSplashScreen):
    """شاشة افتتاحية ملكية قصيرة؛ لا تُعرض في مسار controlled-smoke."""

    def __init__(self):
        background = QPixmap(str(_asset_path("royal_educational_background.png")))
        if background.isNull():
            background = QPixmap(820, 460)
            background.fill(Qt.GlobalColor.darkGreen)
        background = background.scaled(820, 460, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        super().__init__(background)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setObjectName("welcomeSplash")
        self.setAccessibleName("شاشة الترحيب بدليل المربي القرآني")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(58, 48, 58, 48)
        layout.addStretch(2)
        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setPixmap(QPixmap(str(_asset_path("quran_educator_royal_icon.png"))).scaled(92, 92, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo.setAccessibleName("شعار دليل المربي القرآني")
        layout.addWidget(logo)
        layout.addSpacing(8)
        title = QLabel("بسم الله الرحمن الرحيم")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color:#fff6dc; font-size:30px; font-weight:700; background:transparent;")
        subtitle = QLabel(PRODUCT_NAME)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color:#e8c86d; font-size:22px; font-weight:700; background:transparent;")
        message = QLabel("نبني الإنسان، ونرعى الأثر، ونقود العمل بالعلم والخُلُق.")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("color:#f7f0df; font-size:16px; background:transparent;")
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(subtitle)
        layout.addSpacing(12)
        layout.addWidget(message)
        layout.addStretch(3)
        footer = QLabel("منظومة محلية تعمل دون اتصال — بيانات الاختبار الاصطناعية منفصلة عن بيانات الإنتاج")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color:#ead9a3; font-size:11px; background:transparent;")
        layout.addWidget(footer)


def show_welcome_splash(app: QApplication) -> None:
    splash = WelcomeSplash()
    splash.show()
    app.processEvents()
    loop = QEventLoop()
    QTimer.singleShot(1400, loop.quit)
    loop.exec()
    splash.close()
    app.processEvents()


class LocalEntryDialog(QDialog):
    """دخول محلي تجريبي قبل لوحة التحكم؛ ليس نظام مصادقة أو حسابات حقيقية."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{PRODUCT_SHORT_NAME} — الدخول المحلي")
        self.setWindowIcon(QIcon(str(_asset_path("quran_educator_royal_icon.png"))))
        self.setModal(True)
        self.setMinimumSize(520, 360)
        self.setAccessibleName("واجهة الدخول المحلي التجريبي")
        self.setStyleSheet("""
            QDialog { background: #082e2b; color: #fff6dc; border: 2px solid #b89552; }
            QLabel#entryTitle { color: #fff6dc; font-size: 26px; font-weight: 700; }
            QLabel#entrySubtitle { color: #e8c86d; font-size: 16px; font-weight: 600; }
            QLabel#entryHint { color: #f7f0df; font-size: 13px; }
            QComboBox { background: #fffdf8; color: #173f3b; border: 1px solid #c8a75e; border-radius: 7px; padding: 10px; }
            QPushButton { background: #c79d4d; color: #173f3b; border: 0; border-radius: 7px; padding: 12px 18px; font-weight: 700; }
            QPushButton:hover { background: #e3bd6b; }
            QPushButton:focus { border: 2px solid #fff6dc; }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(42, 34, 42, 34)
        layout.setSpacing(12)
        layout.addStretch(1)
        title = QLabel("مرحبًا بك")
        title.setObjectName("entryTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = QLabel(PRODUCT_NAME)
        subtitle.setObjectName("entrySubtitle")
        subtitle.setWordWrap(True)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint = QLabel("اختر الحساب التجريبي للمتابعة إلى لوحة التحكم المحلية.")
        hint.setObjectName("entryHint")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setWordWrap(True)
        self.account_choice = QComboBox()
        self.account_choice.addItems(["حساب تجريبي — مربي", "حساب تجريبي — مربي متدرب"])
        self.account_choice.setAccessibleName("اختيار حساب الدخول التجريبي")
        button = QPushButton("الدخول إلى لوحة التحكم")
        button.setAccessibleName("الدخول إلى لوحة التحكم")
        button.clicked.connect(self.accept)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(hint)
        layout.addWidget(self.account_choice)
        layout.addWidget(button)
        layout.addStretch(2)
        footer = QLabel("تشغيل محلي دون اتصال — بيانات اصطناعية لأغراض التحقق فقط")
        footer.setObjectName("entryHint")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)


class ProductionEntryDialog(QDialog):
    """دخول محلي فعلي بحسابات محلية؛ لا يرسل بيانات خارج الجهاز."""

    def __init__(self, auth_database_path: Path):
        super().__init__()
        self.auth_service = LocalAuthService(auth_database_path)
        self.authenticated_session = None
        first_account = self.auth_service.count_accounts() == 0
        self.setWindowTitle(f"{PRODUCT_SHORT_NAME} — {'إنشاء حساب المدير الأول' if first_account else 'تسجيل الدخول'}")
        self.setWindowIcon(QIcon(str(_asset_path("quran_educator_royal_icon.png"))))
        self.setModal(True)
        self.setMinimumSize(560, 420 if first_account else 360)
        self.setAccessibleName("واجهة المصادقة المحلية")
        self.setStyleSheet("""
            QDialog { background: #f7f3e9; color: #173f3b; border: 1px solid #c8a75e; }
            QLabel#entryTitle { color: #103f3c; font-size: 27px; font-weight: 700; }
            QLabel#entrySubtitle { color: #8a6a25; font-size: 16px; font-weight: 600; }
            QLabel#entryHint { color: #5d6d69; font-size: 13px; }
            QLineEdit, QComboBox { background: #fffdf8; color: #173f3b; border: 1px solid #c8d5cf; border-radius: 8px; padding: 11px; min-height: 22px; }
            QLineEdit:focus, QComboBox:focus { border: 2px solid #4c9b93; }
            QPushButton { background: #176b65; color: #ffffff; border: 0; border-radius: 8px; padding: 12px 18px; min-height: 24px; font-weight: 700; }
            QPushButton:hover { background: #0e554f; }
            QPushButton:focus { border: 2px solid #b89552; }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(42, 34, 42, 34)
        layout.setSpacing(12)
        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setPixmap(QPixmap(str(_asset_path("quran_educator_royal_icon.png"))).scaled(72, 72, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo.setAccessibleName("شعار دليل المربي القرآني")
        layout.addWidget(logo)
        title = QLabel("إنشاء حساب المدير الأول" if first_account else "تسجيل الدخول المحلي")
        title.setObjectName("entryTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = QLabel(PRODUCT_NAME)
        subtitle.setObjectName("entrySubtitle")
        subtitle.setWordWrap(True)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        form = QFormLayout()
        self.username = QLineEdit()
        self.username.setPlaceholderText("اسم مستخدم فريد")
        self.username.setAccessibleName("اسم المستخدم")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText("كلمة المرور — عشرة أحرف على الأقل")
        self.password.setAccessibleName("كلمة المرور")
        form.addRow("اسم المستخدم", self.username)
        form.addRow("كلمة المرور", self.password)
        self.display_name = QLineEdit()
        self.display_name.setPlaceholderText("الاسم الظاهر في النظام")
        self.display_name.setAccessibleName("الاسم الظاهر")
        if first_account:
            form.addRow("الاسم الظاهر", self.display_name)
            self.role = QComboBox()
            self.role.addItem("مدير النظام", "ADMIN")
            self.role.addItem("مربي", "TEACHER")
            self.role.setAccessibleName("الدور الأول")
            form.addRow("الدور", self.role)
        layout.addLayout(form)
        hint = QLabel("حساب محلي يعمل داخل الجهاز فقط. لا تُحفظ كلمة المرور بصيغتها الصريحة.")
        hint.setObjectName("entryHint")
        hint.setWordWrap(True)
        layout.addWidget(hint)
        self.error_label = QLabel("")
        self.error_label.setObjectName("entryHint")
        self.error_label.setWordWrap(True)
        layout.addWidget(self.error_label)
        button = QPushButton("إنشاء الحساب والمتابعة" if first_account else "تسجيل الدخول")
        button.setAccessibleName(button.text())
        button.clicked.connect(lambda: self._submit(first_account))
        layout.addWidget(button)

    def _submit(self, first_account: bool):
        try:
            username = self.username.text().strip()
            password = self.password.text()
            if first_account:
                display_name = self.display_name.text().strip()
                role = self.role.currentData()
                self.auth_service.create_account(username, display_name, password, role)
            self.authenticated_session = self.auth_service.authenticate(username, password)
            self.accept()
        except Exception as exc:
            self.error_label.setText(str(exc))
            self.password.clear()


QEDS_TOKENS = {
    "primary": "#176b65",
    "primary_hover": "#0e554f",
    "primary_active": "#0a423e",
    "deep_text": "#103f3c",
    "background": "#f7f8fa",
    "hero_surface": "#e8f3ef",
    "surface": "#ffffff",
    "border": "#dfe5e3",
    "muted": "#64716f",
    "warning_surface": "#fff4d6",
    "focus": "#4c9b93",
}


class MainWindow(QMainWindow):
    """واجهة محلية عربية، واضحة الحالات، ومفصولة عن منطق المجال."""

    def __init__(self, database_path: Path | None = None, authorization_context: AuthorizationContext | None = None):
        super().__init__()
        self.authorization_context = authorization_context
        self.setWindowTitle(PRODUCT_NAME)
        self.setWindowIcon(QIcon(str(_asset_path("quran_educator_royal_icon.png"))))
        self.setAccessibleName("النافذة الرئيسية لدليل المربي القرآني")
        self.setMinimumSize(960, 680)
        self.resize(1180, 780)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.controller = ControlledAppController(database_path or Path("data/controlled_ui.sqlite"))
        self.status = QLabel()
        self.account = QComboBox()
        self.account.addItems([
            "حساب تجريبي — مربي",
            "حساب تجريبي — مربي متدرب",
        ])
        self.account.setAccessibleName("الحساب المحلي المصادق عليه")
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setAccessibleName("سجل آخر العمليات")
        self.log.setPlaceholderText("ستظهر هنا رسائل العمليات والنتائج.")
        self._build_ui()
        self._apply_visual_identity()
        self._announce("جاهز للعمل في بيئة مضبوطة بالبيانات الاصطناعية فقط.")

    def _apply_visual_identity(self):
        self.setProperty("qedsVersion", "1.0")
        self.setStyleSheet("""
            QMainWindow, QWidget { background: #f5f1e8; color: #1f2937; }
            QMainWindow { border: 1px solid #b89552; }
            QLabel#brandTitle { color: #123b3a; font-size: 25px; font-weight: 700; letter-spacing: 0.2px; }
            QLabel#brandSubtitle { color: #52615f; font-size: 15px; }
            QFrame#hero { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0b3f3a, stop:0.55 #155b52, stop:1 #082e2b); border: 2px solid #b89552; border-radius: 18px; }
            QLabel#heroTitle { color: #fff6dc; font-size: 27px; font-weight: 700; letter-spacing: 0.2px; }
            QLabel#heroSubtitle { color: #e8c86d; font-size: 18px; font-weight: 600; }
            QLabel#heroMessage { color: #f7f0df; font-size: 14px; }
            QLabel#sectionTitle { color: #174c49; font-size: 18px; font-weight: 700; }
            QFrame#metricCard { background: #f8fbfa; border: 1px solid #d8e7e1; border-radius: 10px; padding: 8px; }
            QLabel#metricValue { color: #103f3c; font-size: 23px; font-weight: 700; }
            QLabel#metricLabel { color: #52615f; font-size: 12px; font-weight: 600; }
            QFrame#virtueCard { background: #ffffff; border: 1px solid #d8e7e1; border-radius: 9px; padding: 9px; }
            QLabel#virtueTitle { color: #176b65; font-weight: 700; font-size: 14px; }
            QLabel#virtueText { color: #5b6d69; font-size: 12px; }
            QLabel#gateBanner { background: #fff4d6; border: 1px solid #e6c76a; border-radius: 6px; padding: 9px; color: #684f12; font-weight: 600; }
            QGroupBox { background: #fffdf8; border: 1px solid #d6c59b; border-radius: 12px; margin-top: 12px; padding: 14px; font-weight: 700; }
            QGroupBox::title { subcontrol-origin: margin; right: 14px; padding: 0 7px; color: #174c49; background: #f7f8fa; }
            QTabWidget::pane { border: 1px solid #dfe5e3; background: #ffffff; border-radius: 10px; padding: 4px; }
            QTabBar::tab { background: #edf1f0; color: #41524f; padding: 10px 16px; margin-left: 3px; border: 1px solid #dfe5e3; border-top-left-radius: 7px; border-top-right-radius: 7px; min-height: 22px; }
            QTabBar::tab:hover { background: #e3eeeb; color: #174c49; }
            QTabBar::tab:selected { background: #ffffff; color: #0e5a55; font-weight: 700; border-bottom-color: #ffffff; }
            QPushButton { background: #176b65; color: white; border: 0; border-radius: 7px; padding: 10px 17px; min-height: 20px; font-weight: 600; }
            QPushButton:hover { background: #0e554f; }
            QPushButton:pressed { background: #0a423e; padding-top: 11px; }
            QPushButton:focus { outline: none; border: 2px solid #4c9b93; }
            QPushButton#primaryAction { background: #103f3c; padding: 12px 20px; font-size: 14px; }
            QPushButton#primaryAction:hover { background: #176b65; }
            QLineEdit, QComboBox, QListWidget, QTextEdit { background: #ffffff; border: 1px solid #cbd5d1; border-radius: 7px; padding: 8px; selection-background-color: #cfe5df; selection-color: #103f3c; }
            QLineEdit:focus, QComboBox:focus, QListWidget:focus, QTextEdit:focus { border: 2px solid #4c9b93; }
            QScrollArea { border: 0; background: transparent; }
            QScrollArea#viewScroll { border: 1px solid #d6c59b; border-radius: 14px; background: #fffdf8; padding: 2px; }
            QFrame[route] { background: #fffdf8; border: 1px solid #e4d8bb; border-radius: 14px; }
            QFrame#mainViewArea { background: transparent; }
            QWidget#persistentNavigation { background: #f1eadb; border: 1px solid #c8a75e; border-radius: 12px; }
            QPushButton[route] { background: transparent; color: #174c49; border: 1px solid transparent; border-radius: 7px; padding: 10px 12px; min-height: 22px; text-align: right; }
            QPushButton[route]:hover { background: #dff0eb; border-color: #b9d9ce; }
            QPushButton[route]:checked { background: #ffffff; color: #103f3c; border: 2px solid #4c9b93; font-weight: 700; }
            QLabel#contextBar { background: #fffdf8; color: #52615f; border: 1px solid #d6c59b; border-radius: 7px; padding: 8px 12px; }
            QStackedWidget#viewStack { background: #ffffff; border: 1px solid #dfe5e3; border-radius: 10px; }
            QListWidget { padding: 4px; }
            QListWidget::item { padding: 7px 8px; border-radius: 5px; }
            QListWidget::item:selected { background: #dff0eb; color: #103f3c; }
            QListWidget::item:focus { border: 2px solid #4c9b93; }
            QGroupBox#studentProfile { background: #fffdf8; border: 1px solid #c8a75e; border-radius: 14px; padding: 14px; }
            QLabel#studentProfileContent { color: #173f3b; font-size: 14px; line-height: 1.5; padding: 8px; }
            QLabel#pageTitle { color: #174c49; font-size: 21px; font-weight: 700; padding-bottom: 3px; }
            QLabel#sectionHint { color: #64716f; font-size: 13px; line-height: 1.35; }
            QLabel#emptyState { color: #687572; padding: 18px; border: 1px dashed #bdc9c5; border-radius: 8px; background: #fbfcfc; }
            QTextEdit#activityLog { background: #172422; color: #d8eee8; font-family: Consolas, monospace; border: 1px solid #28443f; }
        """)

    def _build_ui(self):
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        header = QFrame()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(4, 0, 4, 0)
        brand = QLabel(PRODUCT_NAME)
        brand.setObjectName("brandTitle")
        subtitle = QLabel("منظومة محلية لمساندة المربي وإدارة الحلقة وبناء الأثر التربوي")
        subtitle.setObjectName("brandSubtitle")
        header_layout.addWidget(brand)
        header_layout.addWidget(subtitle)
        layout.addWidget(header)

        hero = QFrame()
        hero.setObjectName("hero")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(24, 20, 24, 20)
        hero_title = QLabel("بسم الله الرحمن الرحيم")
        hero_title.setObjectName("heroTitle")
        hero_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_subtitle = QLabel("دليل المربي القرآني | صُنّاع المربي والمفكر")
        hero_subtitle.setObjectName("heroSubtitle")
        hero_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_message = QLabel("نبني جيلًا يصنع أثره بالقرآن، ويقوده العلم، ويزنه الخُلُق، ويقوى بالوعي، وينفع الناس.")
        hero_message.setObjectName("heroMessage")
        hero_message.setWordWrap(True)
        hero_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome = QLabel("مرحبًا بك في دليل المربي القرآني — اجعل القرآن أصل التربية، واجعل كل لقاء خطوة في بناء إنسان صالح، قارئ، متدبر، متعلم، ومعلم.")
        welcome.setObjectName("heroMessage")
        welcome.setWordWrap(True)
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_layout.addWidget(hero_title)
        hero_layout.addWidget(hero_subtitle)
        hero_layout.addWidget(hero_message)
        hero_layout.addWidget(welcome)
        layout.addWidget(hero)

        self.status.setObjectName("gateBanner")
        self.status.setAccessibleName("حالة البيئة والبوابات")
        self.status.setWordWrap(True)
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)

        account_box = QGroupBox("الحساب والصلاحيات")
        account_layout = QFormLayout(account_box)
        account_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        account_layout.addRow("الحساب الحالي", self.account)
        role_text = self.authorization_context.role if self.authorization_context else "سياق اختبار اصطناعي"
        account_hint = QLabel(f"الدور المصادق عليه: {role_text}. تُطبق الصلاحيات تدريجيًا على العمليات المدعومة، وتبقى هذه البيانات اصطناعية في وضع التحقق.")
        account_hint.setObjectName("sectionHint")
        account_layout.addRow("", account_hint)
        layout.addWidget(account_box)

        self._view_specs = [
            ViewSpec("dashboard", "لوحة البداية", "ملخص العمل والإجراءات المسموح بها", "DashboardView"),
            ViewSpec("organization", "المؤسسة والحلقة", "تنظيم المؤسسة والحلقات والمجموعات", "OrganizationView"),
            ViewSpec("students", "الطلاب", "البحث في السجلات الاصطناعية", "StudentsView"),
            ViewSpec("curriculum", "المنهج", "الوحدات والمجالات التعليمية", "CurriculumView"),
            ViewSpec("attendance", "الحضور (اليوم)", "إدارة الحضور اليومي ومتابعة الطلاب", "AttendanceView"),
            ViewSpec("progress_observation", "التقدم والملاحظة", "متابعة التقدم والشواهد", "ProgressObservationView"),
            ViewSpec("reports", "التقارير", "تقارير اصطناعية محلية", "ReportsView"),
            ViewSpec("audit", "التدقيق", "سجل العمليات القابلة للتتبع", "AuditView"),
            ViewSpec("backup_restore", "النسخ والاستعادة", "حماية البيانات المحلية والتحقق منها", "BackupRestoreView"),
        ]
        view_types = {
            "DashboardView": DashboardView,
            "OrganizationView": OrganizationView,
            "StudentsView": StudentsView,
            "CurriculumView": CurriculumView,
            "AttendanceView": AttendanceView,
            "ProgressObservationView": ProgressObservationView,
            "ReportsView": ReportsView,
            "AuditView": AuditView,
            "BackupRestoreView": BackupRestoreView,
        }
        self.view_stack = QStackedWidget()
        self.view_stack.setObjectName("viewStack")
        self.view_stack.setAccessibleName("منطقة محتوى الواجهات الوظيفية")
        self.view_instances = {}
        for spec in self._view_specs:
            view = view_types[spec.view_name](self, spec, self._build_page)
            self.view_instances[spec.route] = view

        navigation_items = [NavigationItem(spec.route, spec.title, spec.tooltip) for spec in self._view_specs]
        self.navigation = PersistentNavigation(navigation_items, self)
        self.router = ViewRouter(self.view_stack, self.navigation, self._focus_view)
        for spec in self._view_specs:
            self.router.register(spec.route, self.view_instances[spec.route])

        self.context_bar = QLabel()
        self.context_bar.setObjectName("contextBar")
        self.context_bar.setAccessibleName("سياق الواجهة الحالية")
        self.context_bar.setWordWrap(True)
        self.context_bar.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.context_bar)

        main_area = QFrame()
        main_area.setObjectName("mainViewArea")
        main_layout = QHBoxLayout(main_area)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)
        main_area.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        main_layout.setDirection(QBoxLayout.Direction.LeftToRight)
        main_layout.addWidget(self.view_stack, 1)
        main_layout.addWidget(self.navigation)
        layout.addWidget(main_area, 1)
        self.router.go("dashboard")

        log_box = QGroupBox("آخر العمليات")
        log_layout = QVBoxLayout(log_box)
        self.log.setObjectName("activityLog")
        self.log.setMinimumHeight(92)
        log_layout.addWidget(self.log)
        layout.addWidget(log_box)
        page_scroll = QScrollArea()
        page_scroll.setObjectName("mainPageScroll")
        page_scroll.setAccessibleName("الصفحة الرئيسية القابلة للتمرير")
        page_scroll.setWidgetResizable(True)
        page_scroll.setFrameShape(QFrame.Shape.NoFrame)
        page_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page_scroll.setWidget(root)
        self.setCentralWidget(page_scroll)

    def _go_to_route(self, route: str):
        if hasattr(self, "router"):
            self.router.go(route)

    def _focus_view(self, route: str):
        spec = next((item for item in self._view_specs if item.route == route), None)
        view = self.view_instances.get(route) if hasattr(self, "view_instances") else None
        if spec is not None and hasattr(self, "context_bar"):
            self.context_bar.setText(f"المسار الحالي: {spec.title} | {spec.tooltip}")
        if view is not None:
            view.focus_initial()

    def _build_page(self, title: str):
        page = QWidget()
        page.setObjectName("pageContent")
        page.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(18, 16, 18, 16)
        heading = QLabel(title)
        heading.setObjectName("pageTitle")
        heading.setAccessibleName(f"عنوان واجهة {title}")
        page_layout.addWidget(heading)
        hint = QLabel(self._page_hint(title))
        hint.setObjectName("sectionHint")
        hint.setWordWrap(True)
        page_layout.addWidget(hint)

        if title == "لوحة البداية":
            start_button = QPushButton("ابدأ رحلة البناء")
            start_button.setObjectName("primaryAction")
            start_button.setToolTip("الانتقال إلى ملخص الحلقة والبدء من لوحة المتابعة")
            start_button.clicked.connect(lambda: self._go_to_route("dashboard"))
            page_layout.addWidget(start_button)
            section_title = QLabel("اليوم في الحلقة")
            section_title.setObjectName("sectionTitle")
            page_layout.addWidget(section_title)
            virtues = QGridLayout()
            virtue_data = [
                ("◈", "قرآني التكوين", "يجعل القرآن أصل هدايته وتربيته وبناء شخصيته."),
                ("◇", "واعٍ ومفكر", "يفهم قبل أن يحكم، ويتثبت قبل أن ينقل."),
                ("●", "ثابت في القيم", "يحفظ المبدأ عند الاختبار ويزن المواقف."),
                ("◆", "فصيح مؤدب", "يجمع وضوح البيان وحسن الخلق."),
                ("✦", "متعلم ومعلّم", "يتعلم بإتقان ثم يحول علمه إلى نفع وتعليم."),
                ("○", "نافع للناس", "يرى العلم والتربية والعمل خدمة للناس وإصلاحًا للحياة."),
                ("△", "قوي الشخصية بلا ظلم", "يثبت ويحسن استخدام القوة بالعدل."),
                ("□", "متقن للعمل", "يؤدي واجبه بإحسان ويجعل الجودة عادة."),
                ("✧", "صاحب رسالة وأثر", "يبني أثرًا يتجاوز اللحظة ويحفظ الأمانة."),
            ]
            for index, (icon_text, title_text, body_text) in enumerate(virtue_data):
                card = QFrame()
                card.setObjectName("virtueCard")
                card_layout = QVBoxLayout(card)
                icon = QLabel(icon_text)
                icon.setObjectName("virtueTitle")
                card_layout.addWidget(icon)
                card_title = QLabel(title_text)
                card_title.setObjectName("virtueTitle")
                card_body = QLabel(body_text)
                card_body.setObjectName("virtueText")
                card_body.setWordWrap(True)
                card_layout.addWidget(card_title)
                card_layout.addWidget(card_body)
                virtues.addWidget(card, index // 3, index % 3)
            empowerment_heading = QLabel("جيل التمكين")
            empowerment_heading.setObjectName("sectionTitle")
            page_layout.addWidget(empowerment_heading)
            page_layout.addLayout(virtues)
            victory_heading = QLabel("الجيل الموعود بالنصر")
            victory_heading.setObjectName("sectionTitle")
            page_layout.addWidget(victory_heading)
            empowerment = QLabel("الجيل الموعود بالنصر لا يبدأ من لحظة النصر؛ بل يبدأ من لحظة البناء.\nيبني إيمانه قبل قوته، وعلمه قبل مكانته، وأخلاقه قبل تأثيره، ويؤدي واجبه قبل أن يطالب بحقه.")
            empowerment.setObjectName("emptyState")
            empowerment.setWordWrap(True)
            page_layout.addWidget(empowerment)
            quote = QLabel("النصر لا يبدأ من لحظة التمكين، بل من سنوات الإعداد.")
            quote.setObjectName("heroMessage")
            quote.setWordWrap(True)
            page_layout.addWidget(quote)
            pillars = QGroupBox("مرتكزات البناء")
            pillars_layout = QGridLayout(pillars)
            pillar_data = [
                ("الإيمان", "يبني القلب ويمنح الطريق بوصلة."),
                ("العلم", "يبني العقل ويقود إلى الفهم الراشد."),
                ("الخُلُق", "يضبط القوة ويجعل الأثر رحمة وعدلًا."),
                ("العمل", "يحوّل المعرفة إلى إتقان ونفع."),
            ]
            for index, (pillar_title, pillar_text) in enumerate(pillar_data):
                pillar = QFrame()
                pillar.setObjectName("virtueCard")
                pillar_layout = QVBoxLayout(pillar)
                pillar_title_label = QLabel(pillar_title)
                pillar_title_label.setObjectName("virtueTitle")
                pillar_text_label = QLabel(pillar_text)
                pillar_text_label.setObjectName("virtueText")
                pillar_text_label.setWordWrap(True)
                pillar_layout.addWidget(pillar_title_label)
                pillar_layout.addWidget(pillar_text_label)
                pillars_layout.addWidget(pillar, 0, index)
            page_layout.addWidget(pillars)
            closing_identity = QLabel("نبني الإنسان الذي يستحق أن يحمل الأمانة، قبل أن نتحدث عن أثره في الحياة.")
            closing_identity.setObjectName("heroMessage")
            closing_identity.setWordWrap(True)
            page_layout.addWidget(closing_identity)
            actions = QGroupBox("إجراءات سريعة")
            actions_layout = QVBoxLayout(actions)
            seed = QPushButton("تهيئة بيانات الرحلة التجريبية")
            seed.setToolTip("إنشاء سجل تجريبي محلي لا يحتوي على محتوى حقيقي")
            seed.clicked.connect(self._seed)
            run = QPushButton("تشغيل رحلة الحلقة التجريبية")
            run.setObjectName("primaryAction")
            run.setToolTip("تنفيذ دورة الحلقة الاصطناعية من المؤسسة إلى التقرير")
            run.clicked.connect(self._run_slice)
            actions_layout.addWidget(seed)
            actions_layout.addWidget(run)
            page_layout.addWidget(actions)
            summary_box = QGroupBox("مؤشرات الحلقة")
            summary_layout = QVBoxLayout(summary_box)
            metric_grid = QGridLayout()
            self.dashboard_metric_labels = {}
            metric_definitions = [
                ("organizations", "المؤسسات"),
                ("circles", "الحلقات"),
                ("groups", "المجموعات"),
                ("students", "الطلاب النشطون"),
                ("curricula", "المناهج"),
                ("units", "الوحدات"),
                ("sessions", "الأيام"),
            ]
            for index, (key, label_text) in enumerate(metric_definitions):
                metric_card = QFrame()
                metric_card.setObjectName("metricCard")
                metric_layout = QVBoxLayout(metric_card)
                metric_layout.setContentsMargins(10, 9, 10, 9)
                value_label = QLabel("—")
                value_label.setObjectName("metricValue")
                value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                name_label = QLabel(label_text)
                name_label.setObjectName("metricLabel")
                name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                metric_layout.addWidget(value_label)
                metric_layout.addWidget(name_label)
                self.dashboard_metric_labels[key] = value_label
                metric_grid.addWidget(metric_card, index // 4, index % 4)
            summary_layout.addLayout(metric_grid)
            self.dashboard_summary_label = QLabel("البيانات محلية ومضبوطة لأغراض التحقق الاصطناعي فقط.")
            self.dashboard_summary_label.setObjectName("sectionHint")
            self.dashboard_summary_label.setWordWrap(True)
            summary_layout.addWidget(self.dashboard_summary_label)
            refresh_summary = QPushButton("تحديث ملخص المتابعة")
            refresh_summary.clicked.connect(self._refresh_dashboard)
            summary_layout.addWidget(refresh_summary)
            page_layout.addWidget(summary_box)
            self._refresh_dashboard()
            quick_box = QGroupBox("إجراءات سريعة")
            quick_layout = QGridLayout(quick_box)
            quick_actions = [
                ("الطلاب", "students"),
                ("المؤسسة والحلقة", "organization"),
                ("المنهج", "curriculum"),
                ("الحضور", "attendance"),
                ("التقارير", "reports"),
            ]
            for index, (label, route) in enumerate(quick_actions):
                quick_button = QPushButton(label)
                quick_button.clicked.connect(lambda checked=False, r=route: self._go_to_route(r))
                quick_layout.addWidget(quick_button, index // 3, index % 3)
            page_layout.addWidget(quick_box)
            closing_message = QLabel("جيلٌ يصنعه القرآن، ويهذبه الخُلُق، ويقوده العلم، ويوقظه الوعي، ويحمله العمل.")
            closing_message.setObjectName("heroMessage")
            closing_message.setWordWrap(True)
            page_layout.addWidget(closing_message)
            empty = QLabel("ابدأ رحلة التربية من لوحة المتابعة، ثم راجع الطلاب والحلقة والمناهج والتقارير. وتبقى بيانات هذه النسخة اصطناعية لأغراض التحقق المحلي.")
            empty.setObjectName("emptyState")
            empty.setWordWrap(True)
            page_layout.addWidget(empty)

        elif title == "الطلاب":
            student_actions = QGroupBox("إدارة الطالب")
            student_actions_layout = QHBoxLayout(student_actions)
            add_student = QPushButton("إضافة طالب اصطناعي")
            add_student.setToolTip("إضافة طالب للاختبار المحلي بمعرّف اصطناعي")
            add_student.clicked.connect(self._add_student_from_ui)
            update_student = QPushButton("تعديل اسم طالب")
            update_student.clicked.connect(self._update_student_from_ui)
            move_student = QPushButton("نقل إلى مجموعة")
            move_student.clicked.connect(self._move_student_from_ui)
            archive_student = QPushButton("أرشفة طالب")
            archive_student.clicked.connect(self._archive_student_from_ui)
            for button in (add_student, update_student, move_student, archive_student):
                student_actions_layout.addWidget(button)
            page_layout.addWidget(student_actions)
            learning_actions = QGroupBox("رحلة التقدم وملاحظات المربي")
            learning_layout = QHBoxLayout(learning_actions)
            add_progress = QPushButton("إضافة تقدم")
            add_progress.setToolTip("توثيق خطوة تقدم اصطناعية للطالب المختار")
            add_progress.clicked.connect(self._add_progress_from_ui)
            add_observation = QPushButton("إضافة ملاحظة")
            add_observation.setToolTip("إضافة ملاحظة تربوية اصطناعية من حصة مفتوحة")
            add_observation.clicked.connect(self._add_observation_from_ui)
            learning_layout.addWidget(add_progress)
            learning_layout.addWidget(add_observation)
            page_layout.addWidget(learning_actions)
            page_layout.addWidget(self._build_search_panel())
        elif title == "الحضور (اليوم)":
            page_layout.addWidget(self._build_session_workflow())
        elif title in {"المؤسسة والحلقة", "المنهج", "التقدم والملاحظة"}:
            if title == "المؤسسة والحلقة":
                supported_actions = QGroupBox("إجراءات مدعومة")
                supported_layout = QHBoxLayout(supported_actions)
                create_circle_button = QPushButton("إضافة حلقة اصطناعية")
                create_circle_button.setToolTip("إنشاء حلقة مرتبطة بمؤسسة موجودة باستخدام معرّف اصطناعي")
                create_circle_button.clicked.connect(self._create_circle_from_ui)
                create_group_button = QPushButton("إضافة مجموعة اصطناعية")
                create_group_button.setToolTip("إنشاء مجموعة مرتبطة بحلقة موجودة باستخدام معرّف اصطناعي")
                create_group_button.clicked.connect(self._create_group_from_ui)
                supported_layout.addWidget(create_circle_button)
                supported_layout.addWidget(create_group_button)
                page_layout.addWidget(supported_actions)
            section_map = {
                "المؤسسة والحلقة": [("المؤسسة", "organization"), ("الحلقات", "circle"), ("المجموعات", "group")],
                "المنهج": [("المناهج", "curriculum"), ("الوحدات", "unit")],
                "الحضور": [("الحصص", "session"), ("الحضور", "attendance")],
                "التقدم والملاحظة": [("التقدم", "progress"), ("الملاحظات", "observation")],
            }
            for label, section in section_map[title]:
                box = QGroupBox(label)
                box_layout = QVBoxLayout(box)
                listing = QListWidget()
                listing.setAccessibleName(f"قائمة {label}")
                box_layout.addWidget(listing)
                refresh = QPushButton(f"تحديث {label}")
                refresh.clicked.connect(lambda checked=False, s=section, w=listing: self._refresh_listing(s, w))
                box_layout.addWidget(refresh)
                page_layout.addWidget(box)
                self._refresh_listing(section, listing)
        elif title == "التقارير":
            actions = QGroupBox("التقارير الاصطناعية المحلية")
            actions_layout = QFormLayout(actions)
            self.report_kind = QComboBox()
            self.report_kind.addItem("تقرير الحالة العامة", "status")
            self.report_kind.addItem("تقرير الطلاب", "student")
            self.report_kind.addItem("تقرير الحلقة", "circle")
            self.report_kind.addItem("تقرير اليوم", "session")
            actions_layout.addRow("نوع التقرير", self.report_kind)
            self.report_filters = {}
            for key, label in (("organization", "المؤسسة"), ("circle", "الحلقة"), ("group", "المجموعة"), ("student", "الطالب"), ("session", "اليوم")):
                combo = QComboBox()
                combo.addItem("كل الخيارات", None)
                combo.setAccessibleName(label)
                combo.currentIndexChanged.connect(self._report_filter_changed)
                self.report_filters[key] = combo
                actions_layout.addRow(label, combo)
            report_button = QPushButton("إنشاء التقرير بالسياق المحدد")
            report_button.clicked.connect(self._report)
            actions_layout.addRow(report_button)
            page_layout.addWidget(actions)
            note = QLabel("اختر السياق المتاح ثم أنشئ تقريرًا اصطناعيًا محليًا. لا يتضمن التقرير محتوى قرآنيًا أو بيانات أشخاص حقيقية.")
            note.setObjectName("emptyState")
            note.setWordWrap(True)
            page_layout.addWidget(note)
            self._refresh_report_filters()
        elif title == "التدقيق":
            audit_box = QGroupBox("سجل العمليات القابلة للتتبع")
            audit_layout = QVBoxLayout(audit_box)
            self.audit_list = QListWidget()
            audit_layout.addWidget(self.audit_list)
            audit_refresh = QPushButton("تحديث سجل التدقيق")
            audit_refresh.clicked.connect(self._refresh_audit)
            audit_layout.addWidget(audit_refresh)
            page_layout.addWidget(audit_box)
            self._refresh_audit()
        elif title == "النسخ والاستعادة":
            actions = QGroupBox("حماية البيانات المحلية")
            actions_layout = QVBoxLayout(actions)
            report = QPushButton("إنشاء تقرير محلي اصطناعي")
            report.clicked.connect(self._report)
            backup = QPushButton("إنشاء نسخة والتحقق من الاستعادة")
            backup.clicked.connect(self._backup)
            actions_layout.addWidget(report)
            actions_layout.addWidget(backup)
            page_layout.addWidget(actions)
        else:
            empty = QLabel("هذه الشاشة مهيأة للاتصال بخدمات النواة. ستُفعّل وظائفها تدريجيًا وفق نطاق الإصدار المعتمد.")
            empty.setObjectName("emptyState")
            empty.setWordWrap(True)
            page_layout.addWidget(empty)
        page_layout.addStretch(1)
        return page

    @staticmethod
    def _page_hint(title: str) -> str:
        hints = {
            "لوحة البداية": "ابدأ من هنا: كل لقاء خطوة في بناء إنسان، وكل متابعة تفتح بابًا لأثر أبعد.",
            "المؤسسة والحلقة": "نرتب البيئة التربوية حتى يجد المربي طريقه بوضوح وطمأنينة.",
            "الطلاب": "نتابع الطالب بوصفه إنسانًا في طريق نمو، لا رقمًا في قائمة.",
            "المنهج": "من الفهم إلى الإتقان: مسار تعليمي متدرج يحفظ المعنى ويقود إلى العمل.",
            "الحضور (اليوم)": "سجل حضور اليوم بسرعة ووضوح، ثم راجع ما يحتاجه كل طالب.",
            "التقدم والملاحظة": "العلم إذا اقترن بالخلق صار أثرًا؛ وثّق التقدم بعناية واتزان.",
            "التقارير": "نحوّل الملاحظة إلى صورة تساعد المربي على الخطوة التالية.",
            "التدقيق": "تعرض هذه المساحة الأحداث القابلة للقراءة عندما تكون خدمة التدقيق متاحة.",
            "النسخ والاستعادة": "تحفظ الملفات محليًا فقط، لأن حفظ الأثر جزء من الأمانة.",
        }
        return hints.get(title, "مساحة عمل محلية ضمن منظومة دليل المربي القرآني.")

    def _build_search_panel(self):
        panel = QWidget()
        outer = QVBoxLayout(panel)
        form = QFormLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("اكتب اسم الطالب أو المعرّف الاصطناعي")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.returnPressed.connect(self._search)
        self.group_filter = QLineEdit()
        self.group_filter.setPlaceholderText("معرّف المجموعة — اختياري")
        self.group_filter.setClearButtonEnabled(True)
        form.addRow("عبارة البحث", self.search_input)
        form.addRow("تصفية المجموعة", self.group_filter)
        outer.addLayout(form)
        actions = QHBoxLayout()
        for label, callback in (("بحث", self._search), ("مسح الحقول", self._clear_search), ("تحديث النتائج", self._search)):
            button = QPushButton(label)
            button.clicked.connect(callback)
            actions.addWidget(button)
        outer.addLayout(actions)
        self.search_state = QLabel("ابحث عن الطالب أو حدّث النتائج لمتابعة طريق النمو.")
        self.search_results = QListWidget()
        self.search_results.setAccessibleName("نتائج البحث في الطلاب الاصطناعيين")
        self.search_results.itemDoubleClicked.connect(self._open_detail)
        self.detail = QLabel("")
        self.detail.setWordWrap(True)
        self.detail.setObjectName("studentProfileContent")
        student_profile = QGroupBox("ملف الطالب")
        student_profile.setObjectName("studentProfile")
        profile_layout = QVBoxLayout(student_profile)
        profile_layout.addWidget(self.detail)
        back = QPushButton("العودة إلى نتائج البحث")
        back.clicked.connect(self._back_detail)
        outer.addWidget(self.search_state)
        outer.addWidget(self.search_results, 1)
        outer.addWidget(student_profile)
        outer.addWidget(back)
        return panel

    def _build_session_workflow(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        context_box = QGroupBox("سياق اليوم")
        context_layout = QFormLayout(context_box)
        self.session_combo = QComboBox()
        self.session_combo.setAccessibleName("اختيار اليوم")
        self.session_combo.currentIndexChanged.connect(self._refresh_session_context)
        context_layout.addRow("اليوم", self.session_combo)
        self.session_context_label = QLabel("جارٍ تجهيز بيانات اليوم...")
        self.session_context_label.setWordWrap(True)
        context_layout.addRow("السياق", self.session_context_label)
        layout.addWidget(context_box)

        actions = QHBoxLayout()
        create_button = QPushButton("إضافة يوم اصطناعي")
        create_button.clicked.connect(self._create_session_from_ui)
        open_button = QPushButton("فتح اليوم")
        open_button.clicked.connect(lambda: self._set_session_status("open"))
        close_button = QPushButton("إغلاق اليوم")
        close_button.clicked.connect(lambda: self._set_session_status("close"))
        refresh_button = QPushButton("تحديث بيانات اليوم")
        refresh_button.clicked.connect(self._refresh_session_options)
        for button in (create_button, open_button, close_button, refresh_button):
            actions.addWidget(button)
        layout.addLayout(actions)

        self.session_students = QListWidget()
        self.session_students.setAccessibleName("طلاب اليوم")
        self.session_students.itemDoubleClicked.connect(self._open_student_from_session)
        layout.addWidget(self.session_students)
        attendance_row = QHBoxLayout()
        self.attendance_status = QComboBox()
        self.attendance_status.addItems(["حاضر", "غائب", "متأخر", "بعذر"])
        self.attendance_status.setAccessibleName("حالة الحضور")
        save_attendance = QPushButton("حفظ الحضور")
        save_attendance.clicked.connect(self._save_attendance_from_ui)
        attendance_row.addWidget(self.attendance_status)
        attendance_row.addWidget(save_attendance)
        layout.addLayout(attendance_row)
        self._refresh_session_options()
        return panel

    def _refresh_session_options(self):
        if not hasattr(self, "session_combo"):
            return
        self.session_combo.blockSignals(True)
        self.session_combo.clear()
        options = self.controller.session_options()
        for session_id, external_id, session_date, status, group_id in options:
            self.session_combo.addItem(f"{external_id} — {session_date} — {status}", session_id)
        self.session_combo.blockSignals(False)
        self._refresh_session_context()

    def _refresh_session_context(self):
        if not hasattr(self, "session_students"):
            return
        self.session_students.clear()
        session_id = self.session_combo.currentData()
        if session_id is None:
            self.session_context_label.setText("لا توجد بيانات للحصة بعد.")
            return
        context = self.controller.session_context(session_id)
        if context is None:
            self.session_context_label.setText("تعذر عرض بيانات الحصة. راجع المدخلات وحاول مرة أخرى.")
            return
        session = context["session"]
        group = context["group"]
        circle = context["circle"]
        organization = context["organization"]
        self.session_context_label.setText(
            f"المؤسسة: {organization.name if organization else 'غير متاحة'} | "
            f"الحلقة: {circle.name if circle else 'غير متاحة'} | "
            f"المجموعة: {group.name if group else 'غير متاحة'} | "
            f"التاريخ: {session.session_date} | الحالة: {session.status}"
        )
        if not context["students"]:
            self.session_students.addItem("لا توجد بيانات للحصة بعد.")
            return
        for student in context["students"]:
            status = context["attendance"].get(student.id, "لم يسجل")
            status_label = {"PRESENT": "حاضر", "ABSENT": "غائب", "LATE": "متأخر", "EXCUSED": "بعذر"}.get(status, status)
            item = QListWidgetItem(f"{student.display_name} — الحضور: {status_label}")
            item.setData(Qt.ItemDataRole.UserRole, student.id)
            self.session_students.addItem(item)

    def _create_session_from_ui(self):
        groups = self.controller.group_options()
        if not groups:
            self._announce("لا توجد مجموعة متاحة لإنشاء الحصة.")
            return
        labels = [f"{name} — {external_id}" for _, name, external_id, _ in groups]
        selected, ok = QInputDialog.getItem(self, "اختيار المجموعة", "المجموعة:", labels, 0, False)
        if not ok:
            return
        group_id = groups[labels.index(selected)][0]
        external_id, ok = QInputDialog.getText(self, "معرّف الحصة", "معرّف اصطناعي يبدأ بـ TEST-:")
        if not ok:
            return
        session_date, ok = QInputDialog.getText(self, "تاريخ الحصة", "التاريخ والوقت:", text="2026-08-24 08:00")
        if not ok:
            return
        try:
            self.controller.create_session_from_ui(group_id, external_id, session_date)
            self._announce("تم حفظ الحصة بنجاح. خطوة أخرى في طريق البناء.")
            self._refresh_session_options()
        except Exception as exc:
            self._announce(f"تعذر حفظ الحصة. راجع المدخلات وحاول مرة أخرى. ({exc})")

    def _set_session_status(self, action):
        session_id = self.session_combo.currentData() if hasattr(self, "session_combo") else None
        if session_id is None:
            self._announce("لا توجد حصة محددة بعد.")
            return
        try:
            if action == "open":
                self.controller.open_session_from_ui(session_id)
                message = "تم فتح الحصة بنجاح."
            else:
                self.controller.close_session_from_ui(session_id)
                message = "تم إغلاق الحصة بنجاح."
            self._announce(message)
            self._refresh_session_options()
        except Exception as exc:
            self._announce(f"تعذر تحديث حالة الحصة. راجع المدخلات وحاول مرة أخرى. ({exc})")

    def _save_attendance_from_ui(self):
        session_id = self.session_combo.currentData() if hasattr(self, "session_combo") else None
        item = self.session_students.currentItem() if hasattr(self, "session_students") else None
        if session_id is None or item is None or item.data(Qt.ItemDataRole.UserRole) is None:
            self._announce("اختر حصة وطالبًا قبل حفظ الحضور.")
            return
        try:
            self.controller.record_attendance_from_ui(session_id, item.data(Qt.ItemDataRole.UserRole), self.attendance_status.currentText())
            self._announce("تم حفظ الحضور بنجاح.")
            self._refresh_session_context()
        except Exception as exc:
            self._announce(f"تعذر حفظ الحضور. راجع المدخلات وحاول مرة أخرى. ({exc})")

    def _open_student_from_session(self, item):
        student_id = item.data(Qt.ItemDataRole.UserRole)
        if student_id is None:
            return
        self._go_to_route("students")
        context = self.controller.student_context(student_id)
        if context:
            student = context["student"]
            self.detail.setText(
                f"الطالب: {student.display_name} | {student.external_id}\n"
                f"الحضور المسجل: {len(context['attendance'])}\n"
                f"التقدم المسجل: {len(context['progress'])}\n"
                f"الملاحظات التربوية: {len(context['observations'])}"
            )
            self.search_state.setText("تم فتح الطالب من سياق الحصة. استخدم العودة للرجوع إلى النتائج.")

    def _create_circle_from_ui(self):
        options = self.controller.organization_options()
        if not options:
            self._announce("لا توجد مؤسسة نشطة؛ ابدأ بتهيئة بيانات الرحلة التجريبية.")
            return
        labels = [f"{name} — {external_id}" for _, name, external_id in options]
        selected, ok = QInputDialog.getItem(self, "اختيار المؤسسة", "المؤسسة:", labels, 0, False)
        if not ok:
            return
        index = labels.index(selected)
        external_id, ok = QInputDialog.getText(self, "معرّف الحلقة", "معرّف اصطناعي يبدأ بـ TEST-:")
        if not ok:
            return
        name, ok = QInputDialog.getText(self, "اسم الحلقة", "اسم الحلقة:")
        if not ok:
            return
        try:
            self.controller.create_circle_from_ui(options[labels.index(selected)][0], external_id, name)
            self._announce("تم حفظ الحلقة بنجاح. خطوة أخرى في طريق البناء.")
            self._refresh_all_listings()
        except Exception as exc:
            self._announce(f"تعذر إتمام العملية. راجع البيانات وحاول مرة أخرى. ({exc})")

    def _create_group_from_ui(self):
        options = self.controller.circle_options()
        if not options:
            self._announce("لا توجد حلقة نشطة؛ ابدأ بإضافة حلقة أولًا.")
            return
        labels = [f"{name} — {external_id}" for _, name, external_id in options]
        selected, ok = QInputDialog.getItem(self, "اختيار الحلقة", "الحلقة:", labels, 0, False)
        if not ok:
            return
        index = labels.index(selected)
        external_id, ok = QInputDialog.getText(self, "معرّف المجموعة", "معرّف اصطناعي يبدأ بـ TEST-:")
        if not ok:
            return
        name, ok = QInputDialog.getText(self, "اسم المجموعة", "اسم المجموعة:")
        if not ok:
            return
        try:
            self.controller.create_group_from_ui(options[index][0], external_id, name)
            self._announce("تم حفظ المجموعة بنجاح. خطوة أخرى في طريق البناء.")
            self._refresh_all_listings()
        except Exception as exc:
            self._announce(f"تعذر إتمام العملية. راجع البيانات وحاول مرة أخرى. ({exc})")

    def _add_student_from_ui(self):
        groups = self.controller.list_records("group")
        if not groups:
            self._announce("لا توجد مجموعة متاحة؛ ابدأ بتهيئة الرحلة أو أضف مجموعة أولًا.")
            return
        group_index, ok = QInputDialog.getInt(self, "اختيار المجموعة", "رقم ترتيب المجموعة في القائمة:", 1, 1, len(groups))
        if not ok:
            return
        with self.controller.factory() as session:
            from quran_educator.infrastructure.db import Group
            group_rows = session.query(Group).order_by(Group.id.desc()).all()
            group_id = group_rows[group_index - 1].id
        external_id, ok = QInputDialog.getText(self, "معرّف الطالب", "معرّف اصطناعي يبدأ بـ TEST-:")
        if not ok:
            return
        display_name, ok = QInputDialog.getText(self, "اسم الطالب", "اسم الطالب:")
        if not ok:
            return
        try:
            self.controller.add_student_from_ui(group_id, external_id, display_name)
            self._announce("تم حفظ السجل بنجاح. خطوة أخرى في طريق البناء.")
            self._search()
        except Exception as exc:
            self._announce(f"تعذر إتمام العملية. راجع البيانات وحاول مرة أخرى. ({exc})")

    def _choose_student(self):
        students = self.controller.student_options()
        if not students:
            self._announce("لا توجد سجلات بعد. ابدأ بإضافة أول طالب لبناء الحلقة.")
            return None
        labels = [f"{name} — {external_id}" for _, name, external_id, _ in students]
        selected, ok = QInputDialog.getItem(self, "اختيار الطالب", "الطالب:", labels, 0, False)
        if not ok:
            return None
        return students[labels.index(selected)]

    def _update_student_from_ui(self):
        selected = self._choose_student()
        if selected is None:
            return
        new_name, ok = QInputDialog.getText(self, "تعديل اسم الطالب", "الاسم الجديد:", text=selected[1])
        if not ok:
            return
        try:
            self.controller.update_student_from_ui(selected[0], new_name)
            self._announce("تم حفظ السجل بنجاح. خطوة أخرى في طريق البناء.")
            self._search()
        except Exception as exc:
            self._announce(f"تعذر إتمام العملية. راجع البيانات وحاول مرة أخرى. ({exc})")

    def _move_student_from_ui(self):
        selected = self._choose_student()
        if selected is None:
            return
        groups = self.controller.circle_options()
        if not groups:
            self._announce("لا توجد حلقات متاحة لاختيار مجموعة جديدة.")
            return
        with self.controller.factory() as session:
            from quran_educator.infrastructure.db import Group
            group_rows = session.query(Group).order_by(Group.id.desc()).all()
            labels = [f"مجموعة #{row.id} — حلقة #{row.circle_id} — {row.name}" for row in group_rows]
        target, ok = QInputDialog.getItem(self, "نقل الطالب", "المجموعة الجديدة:", labels, 0, False)
        if not ok:
            return
        target_id = group_rows[labels.index(target)].id
        try:
            self.controller.move_student_from_ui(selected[0], target_id)
            self._announce("تم حفظ السجل بنجاح. خطوة أخرى في طريق البناء.")
            self._search()
        except Exception as exc:
            self._announce(f"تعذر إتمام العملية. راجع البيانات وحاول مرة أخرى. ({exc})")

    def _archive_student_from_ui(self):
        selected = self._choose_student()
        if selected is None:
            return
        answer = QMessageBox.question(self, "أرشفة الطالب", "هل تريد أرشفة هذا السجل؟ لن يُحذف نهائيًا.")
        if answer != QMessageBox.StandardButton.Yes:
            return
        try:
            self.controller.archive_student_from_ui(selected[0])
            self._announce("تم حفظ السجل بنجاح. خطوة أخرى في طريق البناء.")
            self._search()
        except Exception as exc:
            self._announce(f"تعذر إتمام العملية. راجع البيانات وحاول مرة أخرى. ({exc})")

    def _add_progress_from_ui(self):
        selected = self._choose_student()
        if selected is None:
            return
        sources = self.controller.synthetic_source_options()
        if not sources:
            self._announce("لا يوجد مصدر اصطناعي متاح لتوثيق التقدم.")
            return
        source_labels = [f"{external_id} — {version}" for _, external_id, version in sources]
        source_label, ok = QInputDialog.getItem(self, "مصدر التقدم", "المصدر الاصطناعي:", source_labels, 0, False)
        if not ok:
            return
        source_id, _, source_version = sources[source_labels.index(source_label)]
        surah_id, ok = QInputDialog.getInt(self, "المعرّف التعليمي", "رقم الوحدة التعليمية الاصطناعية:", 1, 1, 999)
        if not ok:
            return
        ayah_start, ok = QInputDialog.getInt(self, "بداية النطاق", "بداية النطاق:", 1, 1, 9999)
        if not ok:
            return
        ayah_end, ok = QInputDialog.getInt(self, "نهاية النطاق", "نهاية النطاق:", ayah_start, ayah_start, 9999)
        if not ok:
            return
        status, ok = QInputDialog.getItem(self, "حالة التقدم", "الحالة:", ["مخطط", "قيد التقدم", "مراجع", "متقن"], 1, False)
        if not ok:
            return
        completion, ok = QInputDialog.getInt(self, "نسبة الإنجاز", "النسبة من 0 إلى 100:", 0, 0, 100)
        if not ok:
            return
        try:
            self.controller.create_progress_from_ui(selected[0], source_id, source_version, surah_id, ayah_start, ayah_end, status, completion)
            self._announce("تم حفظ التقدم بنجاح. خطوة أخرى في طريق البناء.")
            self._open_student_context_by_id(selected[0])
        except Exception:
            self._announce("تعذر حفظ السجل. راجع البيانات وحاول مرة أخرى.")

    def _add_observation_from_ui(self):
        selected = self._choose_student()
        if selected is None:
            return
        sessions = self.controller.open_session_options()
        if not sessions:
            self._announce("لا توجد حصة مفتوحة لإضافة ملاحظة المربي.")
            return
        labels = [f"{external_id} — مجموعة #{group_id}" for _, external_id, group_id in sessions]
        session_label, ok = QInputDialog.getItem(self, "سياق الملاحظة", "الحصة المفتوحة:", labels, 0, False)
        if not ok:
            return
        session_id = sessions[labels.index(session_label)][0]
        observation_type, ok = QInputDialog.getText(self, "نوع الملاحظة", "نوع الملاحظة:", text="متابعة تربوية")
        if not ok:
            return
        observation_text, ok = QInputDialog.getText(self, "ملاحظة المربي", "النص:")
        if not ok:
            return
        try:
            self.controller.create_observation_from_ui(selected[0], session_id, observation_type, observation_text)
            self._announce("تم حفظ الملاحظة بنجاح.")
            self._open_student_context_by_id(selected[0])
        except Exception:
            self._announce("تعذر حفظ السجل. راجع البيانات وحاول مرة أخرى.")

    def _open_student_context_by_id(self, student_id):
        context = self.controller.student_context(student_id)
        if context:
            student = context["student"]
            lines = [
                f"الطالب: {student.display_name} | {student.external_id}",
                f"الحضور المسجل: {len(context['attendance'])}",
                f"التقدم المسجل: {len(context['progress'])}",
                f"الملاحظات التربوية: {len(context['observations'])}",
                f"الوحدات المرتبطة: {len(context['assignments'])}",
            ]
            if context["progress"]:
                latest = context["progress"][0]
                lines.append(f"آخر تقدم: {latest.completion}% — {latest.status}")
            if context["observations"]:
                lines.append(f"آخر ملاحظة: {context['observations'][0].observation_text}")
            self.detail.setText("\n".join(lines))
            self.search_state.setText("تم تحديث سياق الطالب.")

    def _refresh_all_listings(self):
        for widget in self.findChildren(QListWidget):
            if widget is not getattr(self, "search_results", None) and widget is not getattr(self, "audit_list", None):
                for section in ("organization", "circle", "group", "curriculum", "unit", "session", "attendance", "progress", "observation"):
                    try:
                        if widget.accessibleName() == {"organization": "قائمة المؤسسة", "circle": "قائمة الحلقات", "group": "قائمة المجموعات", "curriculum": "قائمة المناهج", "unit": "قائمة الوحدات", "session": "قائمة الحصص", "attendance": "قائمة الحضور", "progress": "قائمة التقدم", "observation": "قائمة الملاحظات"}.get(section):
                            self._refresh_listing(section, widget)
                    except Exception:
                        continue

    def _announce(self, text: str):
        self.status.setText(f"بيئة التطوير المضبوطة — بيانات اصطناعية فقط | {text}")

    def _refresh_listing(self, section: str, widget: QListWidget):
        widget.clear()
        try:
            rows = self.controller.list_records(section)
            if not rows:
                widget.addItem("لا توجد سجلات بعد. ابدأ بإضافة أول عنصر لبناء الحلقة.")
                return
            widget.addItems(rows)
        except Exception:
            widget.addItem("تعذر عرض السجلات الآن. راجع البيانات وحاول مرة أخرى.")

    def _refresh_dashboard(self):
        try:
            summary = self.controller.dashboard_summary()
            for key, value_label in self.dashboard_metric_labels.items():
                value_label.setText(str(summary.get(key, 0)))
            self.dashboard_summary_label.setText("آخر قراءة محلية للبيانات الاصطناعية — لا تمثل بيانات مستخدمين حقيقيين.")
        except Exception:
            for value_label in getattr(self, "dashboard_metric_labels", {}).values():
                value_label.setText("—")
            self.dashboard_summary_label.setText("تعذر قراءة ملخص المتابعة حاليًا. راجع آخر العمليات.")

    def _refresh_report_filters(self):
        if not hasattr(self, "report_filters"):
            return
        options = self.controller.report_filter_options()
        self._set_report_combo(self.report_filters["organization"], [(item[0], f"{item[1]} — {item[2]}") for item in options["organizations"]])
        self._set_report_combo(self.report_filters["circle"], [(item[0], f"{item[1]} — {item[2]}") for item in options["circles"]])
        self._set_report_combo(self.report_filters["group"], [(item[0], f"{item[1]} — {item[2]}") for item in options["groups"]])
        self._set_report_combo(self.report_filters["student"], [(item[0], f"{item[1]} — {item[2]}") for item in options["students"]])
        self._set_report_combo(self.report_filters["session"], [(item[0], f"{item[1]} — {item[2]}") for item in options["sessions"]])

    def _set_report_combo(self, combo, rows):
        combo.blockSignals(True)
        selected = combo.currentData()
        combo.clear()
        combo.addItem("كل الخيارات", None)
        for item_id, label in rows:
            combo.addItem(label, item_id)
        if selected is not None:
            index = combo.findData(selected)
            if index >= 0:
                combo.setCurrentIndex(index)
        combo.blockSignals(False)

    def _report_filter_changed(self):
        if not hasattr(self, "report_filters"):
            return
        selected_org = self.report_filters["organization"].currentData()
        selected_circle = self.report_filters["circle"].currentData()
        selected_group = self.report_filters["group"].currentData()
        options = self.controller.report_filter_options()
        circles = [(item[0], f"{item[1]} — {item[2]}") for item in options["circles"] if selected_org is None or item[3] == selected_org]
        groups = [(item[0], f"{item[1]} — {item[2]}") for item in options["groups"] if selected_circle is None or item[3] == selected_circle]
        students = [(item[0], f"{item[1]} — {item[2]}") for item in options["students"] if selected_group is None or item[3] == selected_group]
        sessions = [(item[0], f"{item[1]} — {item[2]}") for item in options["sessions"] if selected_group is None or item[3] == selected_group]
        self._set_report_combo(self.report_filters["circle"], circles)
        self._set_report_combo(self.report_filters["group"], groups)
        self._set_report_combo(self.report_filters["student"], students)
        self._set_report_combo(self.report_filters["session"], sessions)

    def _refresh_audit(self):
        if not hasattr(self, "audit_list"):
            return
        self.audit_list.clear()
        try:
            entries = self.controller.audit_entries()
            if not entries:
                self.audit_list.addItem("لا توجد أحداث تدقيق قابلة للعرض حاليًا.")
                return
            for entry in entries:
                reason = f" | {entry.reason}" if entry.reason else ""
                self.audit_list.addItem(f"{entry.timestamp} | العملية: {entry.action} | السياق: {entry.entity_type}#{entry.entity_id} | النتيجة: {entry.outcome}{reason}")
        except Exception:
            self.audit_list.addItem("تعذر قراءة سجل التدقيق. لم تُنشأ أحداث بديلة.")

    def _seed(self):
        try:
            self.controller.seed_demo()
            self._refresh_dashboard()
            self._refresh_audit()
            self._append_log("تم حفظ الرحلة التجريبية بنجاح. خطوة أخرى في طريق البناء.")
            self._announce("تمت تهيئة البيانات الاصطناعية بنجاح.")
            self._search()
        except Exception as exc:
            self._report_error("تعذر تهيئة البيانات الاصطناعية", exc)

    def _run_slice(self):
        try:
            session_id = self.controller.run_vertical_slice()
            self._refresh_dashboard()
            self._refresh_audit()
            self._append_log(f"اكتملت رحلة الحلقة التجريبية. رقم الجلسة: {session_id}. خطوة أخرى في طريق البناء.")
            self._announce("اكتمل المسار التجريبي بنجاح.")
        except Exception as exc:
            self._report_error("تعذر تشغيل المسار التجريبي", exc)

    def _search(self):
        self.search_results.clear()
        self.detail.clear()
        try:
            raw_group = self.group_filter.text().strip()
            group_id = int(raw_group) if raw_group else None
            rows = self.controller.search_students(self.search_input.text(), group_id=group_id)
            for row in rows:
                item = QListWidgetItem(f"{row.display_name}  |  {row.external_id}")
                item.setData(Qt.ItemDataRole.UserRole, row.id)
                self.search_results.addItem(item)
            self.search_state.setText(f"تم العثور على {len(rows)} نتيجة اصطناعية." if rows else "لم تُعثر على نتائج. جرّب عبارة بحث أخرى.")
        except Exception as exc:
            self.search_state.setText("تعذر تنفيذ البحث. راجع آخر العمليات للتفاصيل.")
            self._report_error("تعذر تنفيذ البحث", exc)

    def _clear_search(self):
        self.search_input.clear()
        self.group_filter.clear()
        self.search_results.clear()
        self.detail.clear()
        self.search_state.setText("تم مسح حقول البحث والتصفية.")

    def _open_detail(self, item):
        student_id = item.data(Qt.ItemDataRole.UserRole)
        try:
            context = self.controller.student_context(student_id)
            if context is None:
                self.detail.setText("تعذر العثور على سجل الطالب ضمن البيانات الحالية.")
                return
            student = context["student"]
            group = context["group"]
            circle = context["circle"]
            organization = context["organization"]
            attendance = context["attendance"]
            progress = context["progress"]
            observations = context["observations"]
            assignments = context["assignments"]
            sessions = context["sessions"]
            lines = [
                f"الطالب: {student.display_name} | {student.external_id}",
                f"المؤسسة: {organization.name if organization else 'غير متاحة'}",
                f"الحلقة: {circle.name if circle else 'غير متاحة'}",
                f"المجموعة: {group.name if group else 'غير متاحة'}",
                f"الحضور المسجل: {len(attendance)}",
                f"التقدم المسجل: {len(progress)}",
                f"الملاحظات التربوية: {len(observations)}",
                f"الوحدات المرتبطة: {len(assignments)}",
                f"الأيام المرتبطة بالحضور: {len(sessions)}",
            ]
            if progress:
                latest = progress[0]
                lines.append(f"آخر تقدم: {latest.completion}% — {latest.status}")
            if observations:
                lines.append(f"آخر ملاحظة: {observations[0].observation_text}")
            self.detail.setText("\n".join(lines))
            self.search_state.setText("تم فتح سياق الطالب. استخدم زر العودة عند الانتهاء.")
        except Exception:
            self.detail.setText("تعذر عرض سياق الطالب الآن. راجع البيانات وحاول مرة أخرى.")
            self.search_state.setText("تعذر فتح السياق التعليمي.")

    def _back_detail(self):
        self.detail.clear()
        self.search_state.setText("تمت العودة إلى نتائج البحث.")

    def _report(self):
        path, _ = QFileDialog.getSaveFileName(self, "حفظ التقرير المحلي", "controlled_report.pdf", "ملفات PDF (*.pdf)")
        if path:
            try:
                report_kind = self.report_kind.currentData() if hasattr(self, "report_kind") else "status"
                context = {}
                if hasattr(self, "report_filters"):
                    values = {key: combo.currentData() for key, combo in self.report_filters.items()}
                    context = self.controller.contextual_report_context(
                        organization_id=values["organization"], circle_id=values["circle"], group_id=values["group"],
                        student_id=values["student"], session_id=values["session"]
                    )
                self.controller.create_report(Path(path), report_kind=report_kind, context=context)
                self._append_log(f"تم إنشاء التقرير المحلي الاصطناعي بنجاح: {path}")
            except Exception as exc:
                self._report_error("تعذر إنشاء التقرير المحلي", exc)

    def _backup(self):
        base = self.controller.database_path.parent / "backups"
        base.mkdir(parents=True, exist_ok=True)
        try:
            result = self.controller.backup_restore_verify(base / "ui.backup.sqlite", base / "ui.restored.sqlite")
            if result:
                self._append_log("تم إنشاء النسخة المحلية والتحقق من الاستعادة بنجاح.")
            else:
                self._report_error("لم ينجح التحقق من النسخة والاستعادة", "نتيجة التحقق غير صحيحة")
        except Exception as exc:
            self._report_error("تعذر تنفيذ النسخ والاستعادة", exc)

    def _append_log(self, text: str):
        self.log.append(f"نجاح — {text}")

    def _report_error(self, title: str, error):
        message = str(error)
        self.log.append(f"خطأ — {title}: {message}")
        self._announce(f"{title}. راجع آخر العمليات.")
        QMessageBox.warning(self, title, f"{title}.\n\nيمكنك مراجعة آخر العمليات أسفل الشاشة.\nالتفاصيل: {message}")

    def closeEvent(self, event):
        self.controller.close()
        event.accept()


def create_app(argv=None):
    app = QApplication(argv or [])
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    icon = QIcon(str(_asset_path("quran_educator_royal_icon.png")))
    if not icon.isNull():
        app.setWindowIcon(icon)
    return app


def main():
    project_root = Path(__file__).resolve().parents[3]
    layout, metadata = startup_contract(project_root)
    logger = configure_local_logging(layout)
    logger.info("controlled startup application_version=%s schema_version=%s", metadata["application_version"], metadata["schema_version"])
    if "--controlled-smoke" in sys.argv[1:]:
        result_path = run_packaged_smoke(layout.database_path, layout.runtime_data_root)
        logger.info("controlled package smoke completed result=%s", result_path)
        return 0
    app = create_app()
    show_welcome_splash(app)
    production_root = layout.runtime_data_root.parent / "production-runtime"
    production_root.mkdir(parents=True, exist_ok=True)
    entry = ProductionEntryDialog(production_root / "production_auth.sqlite")
    if entry.exec() != QDialog.DialogCode.Accepted:
        return 0
    authorization_context = AuthorizationPolicy().context_for(entry.authenticated_session)
    window = MainWindow(production_root / "database.sqlite", authorization_context=authorization_context)
    window.account.clear()
    window.account.addItem(f"{entry.authenticated_session.display_name} — {entry.authenticated_session.role}")
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
