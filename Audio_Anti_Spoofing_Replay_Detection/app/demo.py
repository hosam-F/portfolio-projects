from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.predict import predict

MODEL = str(ROOT / 'models' / 'svm_mfcc.joblib')

BG = '#F4F7FB'
CARD = '#FFFFFF'
NAVY = '#16324F'
BLUE = '#1F6FEB'
GREEN = '#168A5B'
RED = '#C93C4D'
MUTED = '#64748B'


def choose_audio():
    path = filedialog.askopenfilename(
        title='اختر ملفًا صوتيًا',
        filetypes=[('ملفات WAV', '*.wav'), ('جميع الملفات', '*.*')],
    )
    if not path:
        return

    file_name_var.set(Path(path).name)
    status_var.set('جارٍ تحليل الملف الصوتي...')
    result_var.set('')
    confidence_var.set('')
    result_card.configure(bg=CARD)
    root.update_idletasks()

    try:
        result = predict(path, MODEL)
        label = result['label']
        confidence = float(result['confidence'])
        confidence_pct = confidence * 100

        if label == 'GENUINE':
            arabic_label = 'تسجيل أصلي'
            explanation = 'يبدو أن الملف تسجيل أصلي وليس إعادة تشغيل.'
            color = GREEN
        else:
            arabic_label = 'تسجيل مُعاد التشغيل'
            explanation = 'يبدو أن الملف يحتوي على خصائص تسجيل مُعاد تشغيله.'
            color = RED

        result_var.set(arabic_label)
        result_label.configure(fg=color)
        confidence_var.set(f'مستوى الثقة: {confidence_pct:.2f}%')
        explanation_var.set(explanation)
        status_var.set('اكتمل التحليل بنجاح')
        result_card.configure(bg='#F8FAFC')
    except Exception as exc:
        status_var.set('تعذر تحليل الملف')
        messagebox.showerror('خطأ في التنبؤ', str(exc))


def reset_result():
    file_name_var.set('لم يتم اختيار ملف بعد')
    status_var.set('جاهز لتحليل ملف صوتي')
    result_var.set('بانتظار الاختيار')
    confidence_var.set('')
    explanation_var.set('اختر ملف WAV لعرض التصنيف ومستوى الثقة.')
    result_label.configure(fg=MUTED)


root = tk.Tk()
root.title('كاشف التسجيلات المعاد تشغيلها')
root.geometry('620x500')
root.minsize(560, 460)
root.configure(bg=BG)
root.option_add('*Font', 'Arial 11')

header = tk.Frame(root, bg=NAVY, height=105)
header.pack(fill='x')
header.pack_propagate(False)
tk.Label(header, text='كاشف التسجيلات المعاد تشغيلها', bg=NAVY, fg='white',
         font=('Arial', 22, 'bold')).pack(pady=(18, 2))
tk.Label(header, text='تحليل صوتي أكاديمي باستخدام خصائص MFCC ونموذج SVM',
         bg=NAVY, fg='#D7E6F5', font=('Arial', 11)).pack()

body = tk.Frame(root, bg=BG)
body.pack(fill='both', expand=True, padx=36, pady=24)

tk.Label(body, text='اختر ملفًا صوتيًا بصيغة WAV', bg=BG, fg=NAVY,
         font=('Arial', 15, 'bold')).pack(anchor='e')

action_row = tk.Frame(body, bg=BG)
action_row.pack(fill='x', pady=(12, 4))
tk.Button(action_row, text='اختيار ملف صوتي', command=choose_audio,
          bg=BLUE, fg='white', activebackground='#1559B5', activeforeground='white',
          relief='flat', cursor='hand2', padx=18, pady=9,
          font=('Arial', 12, 'bold')).pack(side='right')
tk.Button(action_row, text='مسح النتيجة', command=reset_result,
          bg='#E2E8F0', fg=NAVY, activebackground='#CBD5E1', relief='flat',
          cursor='hand2', padx=14, pady=9, font=('Arial', 11)).pack(side='right', padx=(0, 10))

file_name_var = tk.StringVar(value='لم يتم اختيار ملف بعد')
tk.Label(body, textvariable=file_name_var, bg=BG, fg=MUTED,
         font=('Arial', 10)).pack(anchor='e', pady=(0, 16))

result_card = tk.Frame(body, bg=CARD, highlightbackground='#D9E2EC', highlightthickness=1)
result_card.pack(fill='both', expand=True)
status_var = tk.StringVar(value='جاهز لتحليل ملف صوتي')
result_var = tk.StringVar(value='بانتظار الاختيار')
confidence_var = tk.StringVar(value='')
explanation_var = tk.StringVar(value='اختر ملف WAV لعرض التصنيف ومستوى الثقة.')

tk.Label(result_card, textvariable=status_var, bg=CARD, fg=MUTED,
         font=('Arial', 10)).pack(pady=(22, 8))
result_label = tk.Label(result_card, textvariable=result_var, bg=CARD, fg=MUTED,
                        font=('Arial', 25, 'bold'))
result_label.pack(pady=(8, 8))
tk.Label(result_card, textvariable=confidence_var, bg=CARD, fg=NAVY,
         font=('Arial', 16, 'bold')).pack(pady=4)
tk.Label(result_card, textvariable=explanation_var, bg=CARD, fg=MUTED,
         font=('Arial', 11), wraplength=460).pack(pady=(12, 25))

footer = tk.Label(root, text='ملاحظة: النتيجة تقديرية وتعتمد على النموذج المدرب والملف المدخل.',
                  bg=BG, fg=MUTED, font=('Arial', 9))
footer.pack(pady=(0, 14))

root.mainloop()
