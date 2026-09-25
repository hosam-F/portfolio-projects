using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Security.Cryptography;

namespace THE_HW1_ALL_ENCRAPTION
{
    public partial class Form1 : Form
    {
         
        //the parimaters for RSE
        RSAParameters publci_key;
        RSAParameters  privte_key;
        //END PARIMATERS FOR RSE
        private int[,] encryptionkey = { { 6, 24, 1 }, { 13, 16, 10 }, { 20, 17, 15 } };
        int x;
        char[] alpha = new[] { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
'k', 'l', 'm', 'n',
'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' };
        //for the arabic
        char[] a_alpha = new[] { 'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي' };


        //for avigner
        static string avinalfa = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        static string output = null;
        static char[] letter = avinalfa.ToCharArray();
        static char[] input = null;
        static int res = 0;
        string m = null;
        string k = null;
        //for arabic avigner
        static string avinalfa_arabic = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        static string output_arabic = null;
        static char[] letter_arabic = new[] { 'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي' };
        static char[] input_arabic = null;
        static int res_arabic = 0;
        string m_arabic = null;
        string k_arabic = null;

        public static int Getkeyarabic(string key)
        {
            int r = 0;
            input = key.ToUpper().ToCharArray();
            for (int j = 0; j < input.Length; j++)
            {

                for (int i = 0; i < letter_arabic.Length; i++)
                {
                    if (input[j] == letter_arabic[i])
                    {

                        r = i;

                    }
                }
            }


            return r;
        }

        //for hill















            //deon
        public static string Encryptoin_arabic(string plainText, int key)
        {
            input = plainText.ToUpper().ToCharArray();
            for (int j = 0; j < input.Length; j++)
            {
                for (int i = 0; i < letter_arabic.Length; i++)
                {
                    if (input[j] == letter_arabic[i])
                    {
                        input[j] = letter_arabic[(i + key) % letter_arabic.Length];
                        break;
                    }
                }

            }
            output = new string(input);
            return output;

        }
        private string Encrypt_r(string plaintext)
        {
            StringBuilder ciphertext = new StringBuilder();
             for(int i=0;i <plaintext.Length; i+=3)
            {
                int[] paintextGroup = new int[3];
                int[] ciphertextGroup = new int[3];


                for (int j = 0; j < 3; j++)
                {
                    if (i + j < plaintext.Length)

                    {
                        paintextGroup[j] = plaintext[i + j] - 'A';


                    }
                    else
                    {
                        paintextGroup[j] = 25;
                    }

                }
                for (int j=0; j<3; j++)
                {
                    for (int k = 0; k < 3; k++)

                        ciphertextGroup[j] += encryptionkey[j, k] * paintextGroup[k] ;
                    ciphertextGroup[j] %= 26;
                }
                for(int j=0; j<3;j++)
                {
                    char encryptedchar = (char)(ciphertextGroup[j] + 'A');
                    ciphertext.Append(encryptedchar);
                }


            }
            return ciphertext.ToString();
        }
        private string dncrypt_r(string ciphertext)
        {
            StringBuilder plaintext = new StringBuilder();

            for (int i = 0; i < ciphertext.Length; i += 3)
            {
                int[] paintextGroup = new int[3];
                int[] ciphertextGroup = new int[3];


                for (int j = 0; j < 3; j++)
                {
                    ciphertextGroup[j] = ciphertext[i + j] - 'A';

                }
                int[,] inversekey = { { 8, 5, 10 }, { 21, 8, 21 }, { 21, 12, 8 } };

                for(int j=0;j<3; j++)
                {
                      for(int k=0;k<3; k++)
                    {
                        paintextGroup[j] += inversekey[j, k] * ciphertextGroup[k];
                    }
                    paintextGroup[j] %= 26;
                }
                for(int j=0;j<3;j++)
                {
                    char decryptedchar = (char)(paintextGroup[j] + 'A');
                    plaintext.Append(decryptedchar);
                }
            }
            return plaintext.ToString();
             
        }
        private string Encrypt_a(string plaintext)
        {
            StringBuilder ciphertext = new StringBuilder();
            for (int i = 0; i < plaintext.Length; i += 3)
            {
                int[] paintextGroup = new int[3];
                int[] ciphertextGroup = new int[3];


                for (int j = 0; j < 3; j++)
                {
                    if (i + j < plaintext.Length)

                    {
                        paintextGroup[j] = plaintext[i + j] - 'ي';


                    }
                    else
                    {
                        paintextGroup[j] = 25;
                    }

                }
                for (int j = 0; j < 3; j++)
                {
                    for (int k = 0; k < 3; k++)

                        ciphertextGroup[j] += encryptionkey[j, k] * paintextGroup[k];
                    ciphertextGroup[j] %= 26;
                }
                for (int j = 0; j < 3; j++)
                {
                    char encryptedchar = (char)(ciphertextGroup[j] + 'ي');
                    ciphertext.Append(encryptedchar);
                }


            }
            return ciphertext.ToString();
        }
        private string dncrypt_a(string ciphertext)
        {
            StringBuilder plaintext = new StringBuilder();

            for (int i = 0; i < ciphertext.Length; i += 3)
            {
                int[] paintextGroup = new int[3];
                int[] ciphertextGroup = new int[3];


                for (int j = 0; j < 3; j++)
                {
                    ciphertextGroup[j] = ciphertext[i + j] - 'ي';

                }
                int[,] inversekey = { { 8, 5, 10 }, { 21, 8, 21 }, { 21, 12, 8 } };

                for (int j = 0; j < 3; j++)
                {
                    for (int k = 0; k < 3; k++)
                    {
                        paintextGroup[j] += inversekey[j, k] * ciphertextGroup[k];
                    }
                    paintextGroup[j] %= 26;
                }
                for (int j = 0; j < 3; j++)
                {
                    char decryptedchar = (char)(paintextGroup[j] + 'ي');
                    plaintext.Append(decryptedchar);
                }
            }
            return plaintext.ToString();

        }
        public static string Dencryptoin_arabic(string cipherText, int key)
        {
            input = cipherText.ToUpper().ToCharArray();
            for (int j = 0; j < input.Length; j++)
            {
                for (int i = 0; i < letter_arabic.Length; i++)
                {
                    if (input[j] == letter_arabic[i])
                    {
                        res = (i - key + letter_arabic.Length);
                        input[j] = letter[res % letter_arabic.Length];
                        break;
                    }
                }

            }
            output = new string(input);
            return output;

        }

        //the vignier for arabic encraption  

        public static int Getkey(string key)
        {
            int r = 0;
            input = key.ToUpper().ToCharArray();
            for (int j = 0; j < input.Length; j++)
            {

                for (int i = 0; i < letter.Length; i++)
                {
                    if (input[j] == letter[i])
                    {
                        r = i;
                    }
                }
            }


            return r;
        }
       public  static string Encryptoin(string plainText,int key)
        {
            input = plainText.ToUpper().ToCharArray();
            for(int j=0;j<input.Length;j++)
            {
                for (int i = 0; i < letter.Length; i++)
                {
                    if (input[j] == letter[i])
                    {
                        input[j] = letter[(i + key) % letter.Length];
                        break;
                    }
                }

            }
            output = new string(input);
            return output;
             
        }

        public static string Dencryptoin(string cipherText, int key)
        {
            input = cipherText.ToUpper().ToCharArray();
            for (int j = 0; j < input.Length; j++)
            {
                for (int i = 0; i < letter.Length; i++)
                {
                    if (input[j] == letter[i])
                    {
                        res = (i - key + letter.Length);
                        input[j] = letter[res % letter.Length ];
                        break;
                    }
                }

            }
            output = new string(input);
            return output;

        }


        public Form1()
        {
            InitializeComponent();

            RSACryptoServiceProvider n = new RSACryptoServiceProvider(2048);

            publci_key= n.ExportParameters(false);
            privte_key = n.ExportParameters(true);
        }  

        private void Label1_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {
            


        }
        //جميع خوارزميات التشفير عند الظغط على زر التشفير      مع تحيات حسام محمد الجرافي 
        private void Button1_Click(object sender, EventArgs e)
        {
            try
            {
                if (comboBox1.Text == "English")
                {
                    //خوارزمية تحقق من الادخال والتشفير بشفرة القيصر مع تحيات حسام محمد الجرافي 
                    if (radioButton1.Checked == true)
                    {
                        if (textBox1.Text == "")
                        {
                            MessageBox.Show("Enter text in the textBOX  for incraption or enter the key ");
                        }
                        else if (textBox3.Text == "")
                        {
                            MessageBox.Show("Enter text in the textBOX  for incraption or enter the key ");
                        }
                        else
                        {
                            int key = int.Parse(textBox3.Text);
                            char[] y = textBox1.Text.ToCharArray();
                            textBox1.Text = "";
                            textBox2.Text = "";
                            for (int i = 0; i < y.Length; i++)
                            {
                                for (int j = 0; j < 26; j++)
                                {
                                    if (y[i] == alpha[j])
                                    {
                                        textBox2.Text += alpha[(key + j) % 26].ToString();
                                    }
                                }
                            }
                        }

                    }
                    //خوارزمية تحقق من الادخال والتشفير بشفرة الافاين مع تحيات حسام محمد الجرافي
                    else if (radioButton2.Checked == true)
                    {
                        if (textBox1.Text == "")
                        {
                            MessageBox.Show("Enter text in the textBOX  for  encraption   ");
                        }
                        else if (textBox3.Text == "")
                        {
                            MessageBox.Show(" Enter the key for incraption   ");
                        }
                        else if (textBox4.Text == "")
                        {
                            MessageBox.Show("Enter valu of A for encraption  ");
                        }
                        else
                        {
                            int c = 0;

                            int a = int.Parse(textBox4.Text);
                            for (int i = 2; i < a; i++)
                            {
                                if (a % i == 0)
                                {
                                    c++;
                                }
                            }
                            if (c == 0)
                            {

                                int key = int.Parse(textBox3.Text);
                                char[] y = textBox1.Text.ToCharArray();

                                //لمسح فراغات النص

                                textBox1.Text = "";
                                textBox2.Text = "";
                                /*  for(int i = 0; i < 26; i++)
                                  {
                                      if ((a * i) % 26 == 1)
                                      {
                                          x = i;
                                      }
                                  }*/
                                for (int i = 0; i < y.Length; i++)
                                {
                                    for (int j = 0; j < 26; j++)
                                    {
                                        if (y[i] == alpha[j])
                                        {
                                            textBox2.Text += alpha[(a * j + key) % 26].ToString();

                                        }
                                    }
                                }
                            }


                        }
                    }

                         //خوارزمية تحقق من الادخال والتشفير بشفرة العب بالنار مع تحيات حسام محمد الجرافي
                    else if (radioButton3.Checked == true)
                    {
                        if (textBox1.Text == "")
                        {
                            MessageBox.Show("Enter text in the textBOX  for  encraption   ");
                        }
                        else if (textBox3.Text == "")
                        {
                            MessageBox.Show(" Enter the key for incraption   ");
                        }
                        else
                        {

                            textBox2.Text += "";
                            char[] matrix = (textBox3.Text + new string(alpha)).ToCharArray();
                            for (int i = 0; i < matrix.Length; i++)
                            {
                                if (matrix[i] == 'j')
                                {
                                    matrix[i] = 'i';
                                }
                            }
                            for (int i = 0; i < matrix.Length; i++)
                                for (int j = i + 1; j < matrix.Length; j++)
                                {
                                    if (matrix[i] == matrix[j])
                                    {
                                        matrix = (new string(matrix)).Remove(j, 1).ToCharArray();
                                    }
                                }
                            char[,] matrix2D = new char[5, 5];
                            for (int i = 0; i < 5; i++)
                            {
                                for (int j = 0; j < 5; j++)
                                {
                                    matrix2D[i, j] = matrix[i * 5 + j];
                                }
                            }
                            char[] words = textBox1.Text.ToCharArray();
                            for (int j = 0; j < words.Length; j += 2)
                            {
                                char firstletter;
                                char secondletter;

                                if (words[j] == 'j')
                                {
                                    words[j] = 'i';
                                }
                                if (j + 1 < words.Length && words[j + 1] == 'j')
                                {
                                    words[j + 1] = 'i';
                                }
                                if (j + 1 == words.Length)
                                {
                                    firstletter = words[j];
                                    secondletter = 'x';
                                }
                                else if ((j + 1 < words.Length && words[j] == words[j + 1]))
                                {
                                    firstletter = words[j];
                                    secondletter = 'x';
                                    j--;
                                }
                                else
                                {
                                    firstletter = words[j];
                                    secondletter = words[j + 1];
                                }
                                int firstx = 0, fristy = 0, secondx = 0, secondy = 0;
                                for (int row = 0; row < 5; row++)
                                {
                                    for (int col = 0; col < 5; col++)
                                    {

                                        if (firstletter == matrix2D[row, col])
                                        {
                                            firstx = row;
                                            fristy = col;
                                        }
                                        if (secondletter == matrix2D[row, col])
                                        {
                                            secondx = row;
                                            secondy = col;
                                        }
                                    }
                                }
                                if (firstx == secondx)
                                { // same row 
                                    textBox2.Text += matrix2D[firstx, (fristy + 1) % 5];
                                    textBox2.Text += matrix2D[secondx, (secondy + 1) % 5];
                                }
                                else if (fristy == secondy)
                                {
                                    //same col 
                                    textBox2.Text += matrix2D[(firstx + 1) % 5, fristy];
                                    textBox2.Text += matrix2D[(secondx + 1) % 5, secondy];
                                }
                                else
                                {//Different will take intersection 
                                    textBox2.Text += matrix2D[firstx, secondy];
                                    textBox2.Text += matrix2D[secondx, fristy];
                                }
                                textBox1.Text = "";

                            }

                        }
                    }

                         //خوارزمية تحقق من الادخال والتشفير بشفرة الفيجنر مع تحيات حسام محمد الجرافي
                    else if (radioButton4.Checked == true)
                    {
                        if (textBox3.Text.Trim() != "")
                        {

                            textBox2.Clear();
                            m = textBox1.Text;
                            k = textBox3.Text;
                            int r = 0;
                            string s = null;
                            for (int i = 0; i < m.Length; i++)
                            {
                                if (r == k.Length - 1)
                                {
                                    r = 0;
                                }
                                else if (r < k.Length && i > 0)
                                {
                                    r++;



                                }
                                else if (r < k.Length && i == 0)
                                {
                                    r = 0;
                                }
                                if (r < k.Length)
                                {
                                    s += Encryptoin(m.Substring(i, 1).ToUpper(), Getkey(k.Substring(r, 1).ToUpper()));


                                }

                            }
                            textBox2.Text = s;


                        }
                        else
                        {
                            MessageBox.Show("Enter the key world for ENCRPTON  VIGENER ");
                        }


                    }
                    else if (radioButton5.Checked == true)
                    {


                    }
                    //خوارزمية تحقق من الادخال والتشفير بشفرة ار اس اي مع تحيات حسام محمد الجرافي
                    else if(radioButton6.Checked==true)
                    {
                        if (textBox1.Text == "")
                        {
                            MessageBox.Show("Enter text in the textBOX  for  encraption   ");
                        }
                        
                        else
                        {
                            RSACryptoServiceProvider n2 = new RSACryptoServiceProvider();
                            n2.ImportParameters(publci_key);
                            byte[] m = Encoding.Unicode.GetBytes(textBox1.Text);
                            byte[] m2 = n2.Encrypt(m, false);
                            textBox5.Text = Convert.ToBase64String(m2);


                        }

                        }

                         //خوارزمية تحقق من الادخال والتشفير بشفرة الهيل مع تحيات حسام محمد الجرافي
                    else if(radioButton7.Checked==true)
                    {
                        string plaintext = textBox1.Text.ToUpper();
                        string ciphertext = Encrypt_r(plaintext);
                        textBox2.Text = ciphertext;
                    }
                }
                //خوارزميات  التشفير  مع تحيات حسام محمد الجرافي

                else if (comboBox1.Text == "Arabic")
                        {
                            if (radioButton1.Checked == true)
                            {
                                if (textBox1.Text == "")
                                {
                                    MessageBox.Show("ادخل النص في مربع النص وادحل المفتاح في مرع المفتاح");
                                }
                                else if (textBox3.Text == "")
                                {
                                    MessageBox.Show("يجب عليك ادخال المفتاح في حقل المفتاح ");
                                }
                                else
                                {
                                    int key = int.Parse(textBox3.Text);
                                    char[] y = textBox1.Text.ToCharArray();
                                    textBox1.Text = "";
                                    textBox2.Text = "";
                                    for (int i = 0; i < y.Length; i++)
                                    {
                                        for (int j = 0; j < 28; j++)
                                        {
                                            if (y[i] == a_alpha[j])
                                            {
                                                textBox2.Text += a_alpha[(key + j) % 28].ToString();
                                            }
                                        }
                                    }
                                }


                            }

                                 //خوارزميات التشفير  مع تحيات حسام محمد الجرافي
                            else if (radioButton2.Checked == true)
                            {
                                if (textBox1.Text == "")
                                {
                                    MessageBox.Show("ادخل النص في مربع النص وادحل المفتاح في مرع المفتاح ");
                                }
                                else if (textBox3.Text == "")
                                {
                                    MessageBox.Show(" يجب عليك ادخال المفتاح في حقل المفتاح  ");
                                }
                                else if (textBox4.Text == "")
                                {
                                    MessageBox.Show("  يجب عليك ادخال مضروب العدد ");
                                }
                                else
                                {
                                    int c = 0;

                                    int a = int.Parse(textBox4.Text);
                                    for (int i = 2; i < a; i++)
                                    {
                                        if (a % i == 0)
                                        {
                                            c++;
                                        }
                                    }
                                    if (c == 0)
                                    {

                                        int key = int.Parse(textBox3.Text);
                                        char[] y = textBox1.Text.ToCharArray();


                                        textBox1.Text = "";
                                        textBox2.Text = "";
                                        /*  for(int i = 0; i < 26; i++)
                                          {
                                              if ((a * i) % 26 == 1)
                                              {
                                                  x = i;
                                              }
                                          }*/
                                        for (int i = 0; i < y.Length; i++)
                                        {
                                            for (int j = 0; j < 28; j++)
                                            {
                                                if (y[i] == a_alpha[j])
                                                {
                                                    textBox2.Text += a_alpha[(a * j + key) % 28].ToString();

                                                }
                                            }
                                        }
                                    }


                                }

                            }
                            //خوارزميات التشفير  مع تحيات حسام محمد الجرافي
                            else if (radioButton3.Checked == true)
                            {
                                if (textBox1.Text == "")
                                {
                                    MessageBox.Show(" يجب ادخال النص المراد تشفيره وادخال المفتاح  ");
                                }
                                else if (textBox3.Text == "")
                                {
                                    MessageBox.Show(" يجب ادخال المفتاح من اجل التشفير  ");
                                }
                                else
                                {

                                    textBox2.Text += "";
                                    char[] matrix = (textBox3.Text + new string(a_alpha)).ToCharArray();
                                    for (int i = 0; i < matrix.Length; i++)
                                    {
                                        if (matrix[i] == 'ص' || matrix[i] == 'س')
                                        {
                                            matrix[i] = 'ش';
                                        }
                                    }
                                    for (int i = 0; i < matrix.Length; i++)
                                        for (int j = i + 1; j < matrix.Length; j++)
                                        {
                                            if (matrix[i] == matrix[j])
                                            {
                                                matrix = (new string(matrix)).Remove(j, 1).ToCharArray();
                                            }
                                        }
                                    char[,] matrix2D = new char[5, 5];
                                    for (int i = 0; i < 5; i++)
                                    {
                                        for (int j = 0; j < 5; j++)
                                        {
                                            matrix2D[i, j] = matrix[i * 5 + j];
                                        }
                                    }
                                    char[] words = textBox1.Text.ToCharArray();
                                    for (int j = 0; j < words.Length; j += 2)
                                    {
                                        char firstletter;
                                        char secondletter;

                                        if (words[j] == 'س' || words[j] == 'ص')
                                        {
                                            words[j] = 'ش';
                                        }
                                        if (j + 1 < words.Length && words[j + 1] == 'س' )
                                        {
                                            words[j + 1] = 'ش';
                                        }
                                        if (j + 1 < words.Length && words[j + 1] == 'ص')
                                        {
                                            words[j + 1] = 'ش';
                                        }
                                        if (j + 1 == words.Length)
                                        {
                                            firstletter = words[j];
                                            secondletter = 'x';
                                        }
                                        else if ((j + 1 < words.Length && words[j] == words[j + 1]))
                                        {
                                            firstletter = words[j];
                                            secondletter = 'x';
                                            j--;
                                        }
                                        else
                                        {
                                            firstletter = words[j];
                                            secondletter = words[j + 1];
                                        }
                                        int firstx = 0, fristy = 0, secondx = 0, secondy = 0;
                                        for (int row = 0; row < 5; row++)
                                        {
                                            for (int col = 0; col < 5; col++)
                                            {

                                                if (firstletter == matrix2D[row, col])
                                                {
                                                    firstx = row;
                                                    fristy = col;
                                                }
                                                if (secondletter == matrix2D[row, col])
                                                {
                                                    secondx = row;
                                                    secondy = col;
                                                }
                                            }
                                        }
                                        if (firstx == secondx)
                                        { // same row 
                                            textBox2.Text += matrix2D[firstx, (fristy + 1) % 5];
                                            textBox2.Text += matrix2D[secondx, (secondy + 1) % 5];
                                        }
                                        else if (fristy == secondy)
                                        {
                                            //same col 
                                            textBox2.Text += matrix2D[(firstx + 1) % 5, fristy];
                                            textBox2.Text += matrix2D[(secondx + 1) % 5, secondy];
                                        }
                                        else
                                        {//Different will take intersection 
                                            textBox2.Text += matrix2D[firstx, secondy];
                                            textBox2.Text += matrix2D[secondx, fristy];
                                        }
                                        textBox1.Text = "";




                                    }



                                }
                            }
                            //خوارزميات التشفير  مع تحيات حسام محمد الجرافي
                            else if (radioButton4.Checked == true)
                            {
                                if (textBox3.Text.Trim() != "")
                                {

                                    textBox2.Clear();
                                    m = textBox1.Text;
                                    k = textBox3.Text;
                                    int r = 0;
                                    string s = null;
                                    for (int i = 0; i < m.Length; i++)
                                    {
                                        if (r == k.Length - 1)
                                        {
                                            r = 0;
                                        }
                                        else if (r < k.Length && i > 0)
                                        {

                                            r++;



                                        }
                                        else if (r < k.Length && i == 0)
                                        {
                                            r = 0;
                                        }
                                        if (r < k.Length)
                                        {
                                            s += Encryptoin_arabic(m.Substring(i, 1).ToUpper(), Getkeyarabic(k.Substring(r, 1).ToUpper()));


                                        }

                                    }
                                    textBox2.Text = s;


                                }
                                else
                                {
                                    MessageBox.Show("Enter the key world for ENCRPTON  VIGENER ");
                                }


                            }
                            else if (radioButton6.Checked == true)
                    {
                        if (textBox1.Text == "")
                        {
                            MessageBox.Show("Enter text in the textBOX  for  encraption   ");
                        }

                        else
                        {
                            RSACryptoServiceProvider n2 = new RSACryptoServiceProvider();
                            n2.ImportParameters(publci_key);
                            byte[] m = Encoding.Unicode.GetBytes(textBox1.Text);
                            byte[] m2 = n2.Encrypt(m, false);
                            textBox5.Text = Convert.ToBase64String(m2);


                        }

                    }
                            //خوارزميات التشفير  مع تحيات حسام محمد الجرافي
                            else if(radioButton7.Checked==true)
                    {
                        string plaintext = textBox1.Text.ToUpper();
                        string ciphertext = Encrypt_a(plaintext);
                        textBox2.Text = ciphertext;
                    }


                }


        }

            catch (Exception)
            {
                MessageBox.Show(" Error in the try ");
            }

}


        // جميع خوارزميات فك التشفير عند حدث ظغط على زر فك التشفير مع تحيات حسام محمد الجرافي 
       
        
        private void Button2_Click(object sender, EventArgs e)
        {
            try
            {
                if (comboBox1.Text == "English")
                {


                    //خوارزمية فك تشفر القيصر مع تحيات حسام محمد الجرافي 
                    if (radioButton1.Checked == true)
                    {
                        if (textBox2.Text == "")
                        {
                            MessageBox.Show("Enter text in the textBOX  for decraption  ");
                        }
                        else if (textBox3.Text == "")
                        {
                            MessageBox.Show("Enter key for decraption   ");
                        }
                        else
                        {
                            int key = int.Parse(textBox3.Text);
                            char[] y = textBox2.Text.ToCharArray();
                            textBox1.Text = "";
                            textBox2.Text = "";

                            for (int i = 0; i < y.Length; i++)
                            {
                                for (int j = 0; j < 26; j++)
                                {
                                    if (y[i] == alpha[j])
                                    {
                                        if (j - key < 0)
                                        {
                                            textBox1.Text += alpha[(j - key) + 26].ToString();
                                        }
                                        else
                                        {
                                            textBox1.Text += alpha[(j - key)].ToString();

                                        }
                                    }
                                }
                            }
                        }


                    }
                    //خوارزمية فك تشفر الافاين مع تحيات حسام محمد الجرافي 
                    else if (radioButton2.Checked == true)
                    {
                        if (textBox2.Text == "")
                        {
                            MessageBox.Show("enter text in the textBOX  for  decraption  ");
                        }
                        else if (textBox3.Text == "")
                        {
                            MessageBox.Show(" enter the key for decraption  ");
                        }
                        else if (textBox4.Text == "")
                        {
                            MessageBox.Show("enter valu of A for ancraption ");
                        }
                        else
                        {
                            int c = 0;

                            int a = int.Parse(textBox4.Text);
                            for (int i = 2; i < a; i++)
                            {
                                if (a % i == 0)
                                {
                                    c++;
                                }
                            }
                            if (c == 0)
                            {

                                int key = int.Parse(textBox3.Text);
                                char[] y = textBox2.Text.ToCharArray();


                                textBox1.Text = "";
                                textBox2.Text = "";

                                for (int i = 1; i < 26; i++)
                                {
                                    if ((a * i) % 26 == 1)
                                    {
                                        x = i;
                                    }
                                }
                                for (int i = 0; i < y.Length; i++)
                                {
                                    for (int j = 0; j < 26; j++)
                                    {
                                        if (y[i] == alpha[j])
                                        {
                                            textBox1.Text += alpha[(x * ((j - key) + 26)) % 26].ToString().ToUpper();

                                        }
                                    }
                                }
                            }


                        }

                    }
                    //خوارزمية فك تشفر العب بالنار مع تحيات حسام محمد الجرافي 
                    else if (radioButton3.Checked == true)
                    {


                        if (textBox2.Text == "")
                        {
                            MessageBox.Show("enter text in the textBOX  for  decraption  ");
                        }
                        else if (textBox3.Text == "")
                        {
                            MessageBox.Show(" enter the key for decraption  ");
                        }
                        else
                        {
                            textBox1.Text = "";

                            char[] matrix = (textBox3.Text + new string(alpha)).ToCharArray();
                            //change every j to i 
                            for (int i = 0; i < matrix.Length; i++)
                            {
                                if (matrix[i] == 'j')
                                {
                                    matrix[i] = 'i';
                                }
                            }
                            //Remove duplcate letter 
                            for (int i = 0; i < matrix.Length; i++)
                                for (int j = i + 1; j < matrix.Length; j++)
                                {
                                    if (matrix[i] == matrix[j])
                                    {
                                        matrix = (new string(matrix)).Remove(j, 1).ToCharArray();
                                    }
                                }
                            // create array 5*5 
                            char[,] matrix2D = new char[5, 5];
                            for (int i = 0; i < 5; i++)
                            {
                                for (int j = 0; j < 5; j++)
                                {
                                    matrix2D[i, j] = matrix[i * 5 + j];
                                }
                            }

                            char[] words = (Convert.ToString(textBox2.Text)).ToArray();
                            // block block of two letter 
                            for (int j = 0; j < words.Length; j += 2)
                            {
                                char firstletter;
                                char secondletter;
                                //change every j to i 
                                if (words[j] == 'j')
                                {
                                    words[j] = 'i';
                                }
                                if (j + 1 < words.Length && words[j + 1] == 'j')
                                {
                                    words[j + 1] = 'i';
                                }
                                if (j + 1 == words.Length)
                                {
                                    firstletter = words[j];
                                    secondletter = 'x';
                                }
                                else if ((j + 1 < words.Length && words[j] == words[j + 1]))
                                {
                                    firstletter = words[j];
                                    secondletter = 'x';
                                    j--;
                                }
                                else
                                {
                                    firstletter = words[j];
                                    secondletter = words[j + 1];
                                }
                                int firstx = 0, fristy = 0, secondx = 0, secondy = 0;
                                for (int row = 0; row < 5; row++)
                                {
                                    for (int col = 0; col < 5; col++)
                                    {
                                        if (firstletter == matrix2D[row, col])
                                        {
                                            firstx = row;
                                            fristy = col;
                                        }
                                        if (secondletter == matrix2D[row, col])
                                        {
                                            secondx = row;
                                            secondy = col;
                                        }
                                    }
                                }
                                if (firstx == secondx)
                                { // same row 

                                    textBox1.Text += matrix2D[firstx, ((fristy - 1) % 5)].ToString();
                                    textBox1.Text += matrix2D[secondx, ((secondy - 1) % 5)].ToString();
                                }

                                else if (fristy == secondy)
                                {
                                    //same col 
                                    textBox1.Text += matrix2D[(firstx - 1) % 5, fristy].ToString();
                                    textBox1.Text += matrix2D[(secondx - 1) % 5, secondy].ToString();
                                }
                                else
                                {//Different will take intersection 
                                    textBox1.Text += matrix2D[firstx, secondy].ToString();
                                    textBox1.Text += matrix2D[secondx, fristy].ToString();
                                }
                                textBox2.Text = "";
                            }






                        }


                    }
                    //خوارزمية فك تشفر الفيجنر مع تحيات حسام محمد الجرافي 
                    else if (radioButton4.Checked == true)
                    {
                        if (textBox3.Text.Trim() != "")
                        {
                            textBox1.Clear();
                            m = textBox2.Text;
                            k = textBox3.Text;
                            int r = 0;
                            string s = null;
                            for (int i = 0; i < m.Length; i++)
                            {
                                if (r == k.Length - 1)
                                {
                                    r = 0;
                                }
                                else if (r < k.Length && i > 0)
                                {
                                    r++;



                                }
                                else if (r < k.Length && i == 0)
                                {
                                    r = 0;
                                }
                                if (r < k.Length)
                                {
                                    s += Dencryptoin(m.Substring(i, 1).ToUpper(), Getkey(k.Substring(r, 1).ToUpper()));


                                }

                            }
                            textBox1.Text = s;


                        }
                        else
                        {
                            MessageBox.Show("Enter the key world for ENCRPTON  VIGENER ");
                        }


                    }

                        //خوارزمية فك تشفر ار اس اي مع تحيات حسام محمد الجرافي 
                    else if(radioButton6.Checked==true)
                    {
                        if (textBox5.Text == "")
                        {
                            MessageBox.Show("enter text in the textBOX  for  decraption  ");
                        }
                        else
                        {
                            RSACryptoServiceProvider decrpt = new RSACryptoServiceProvider();
                            decrpt.ImportParameters(privte_key);
                            byte[] c = Convert.FromBase64String(textBox5.Text);
                            byte[] c1 = decrpt.Decrypt(c, false);
                            textBox1.Text = Encoding.Unicode.GetString(c1);
                        }

                    }
                    //خوارزمية فك تشفر الهيل مع تحيات حسام محمد الجرافي 
                    else if(radioButton7.Checked==true)
                    {
                        string ciphertext = textBox2.Text.ToUpper();
                        string plaintext = dncrypt_r(ciphertext);
                        textBox1.Text = plaintext;
                    }

                }
                //خوارزمية فك تشفر باللغة العربية مع تحيات حسام محمد الجرافي 
                else if(comboBox1.Text== "Arabic")
                {
                    if (radioButton1.Checked == true)
                    {
                        if (textBox2.Text == "")
                        {
                            MessageBox.Show(" تاكد من وجود نص لا فك التشفير   ");
                        }
                        else if (textBox3.Text == "")
                        {
                            MessageBox.Show("لا يوجد مفتاح يجب عليك ادخال المفتاح   ");
                        }
                        else
                        {
                            int key = int.Parse(textBox3.Text);
                            char[] y = textBox2.Text.ToCharArray();
                            textBox1.Text = "";
                            textBox2.Text = "";

                            for (int i = 0; i < y.Length; i++)
                            {
                                for (int j = 0; j < 28; j++)
                                {
                                    if (y[i] == a_alpha[j])
                                    {
                                        if (j - key < 0)
                                        {
                                            textBox1.Text += a_alpha[ (j - key) + 28].ToString();
                                        }
                                        else
                                        {
                                            textBox1.Text += a_alpha[(j - key)].ToString();

                                        }
                                    }
                                }
                            }
                        }


                    }
                    //خوارزمية فك تشفر عربي مع تحيات حسام محمد الجرافي 
                    else if (radioButton2.Checked == true)
                    {
                        if (textBox2.Text == "")
                        {
                            MessageBox.Show("تاكد من وجود نص لا فك التشفير");
                        }
                        else if (textBox3.Text == "")
                        {
                            MessageBox.Show("لا يوجد مفتاح يجب عليك ادخال المفتاح ");
                        }
                        else if (textBox4.Text == "")
                        {
                            MessageBox.Show("معكوس المعامل الضربي ليس موجود يجب عليك اضافة المعامل الضربي  ");
                        }
                        else
                        {
                            int c = 0;

                            int a = int.Parse(textBox4.Text);
                            for (int i = 2; i < a; i++)
                            {
                                if (a % i == 0)
                                {
                                    c++;
                                }
                            }
                            if (c == 0)
                            {

                                int key = int.Parse(textBox3.Text);
                                char[] y = textBox2.Text.ToCharArray();


                                textBox1.Text = "";
                                textBox2.Text = "";

                                for (int i = 1; i < 26; i++)
                                {
                                    if ((a * i) % 26 == 1)
                                    {
                                        x = i;
                                    }
                                }
                                for (int i = 0; i < y.Length; i++)
                                {
                                    for (int j = 0; j < 28; j++)
                                    {
                                        if (y[i] == a_alpha[j])
                                        {
                                            textBox1.Text += a_alpha[(x * ((j - key) + 28)) % 26].ToString().ToUpper();

                                        }
                                    }
                                }
                            }


                        }

                    }
                    //خوارزمية فك تشفر عربي مع تحيات حسام محمد الجرافي 
                    else if (radioButton3.Checked == true)
                    {


                        if (textBox2.Text == "")
                        {
                            MessageBox.Show(" تاكد من وجود نص لا فك التشفير");
                        }
                        else if (textBox3.Text == "")
                        {
                            MessageBox.Show(" لا يوجد مفتاح يجب عليك ادخال المفتاح  ");
                        }
                        else
                        {
                            textBox1.Text = "";

                            char[] matrix = (textBox3.Text + new string(a_alpha)).ToCharArray();
                            //change every j to i 
                            for (int i = 0; i < matrix.Length; i++)
                            {
                                if (matrix[i] == 'س' || matrix[i]=='ص')
                                {
                                    matrix[i] = 'ش';
                                }
                            }
                            //Remove duplcate letter 
                            for (int i = 0; i < matrix.Length; i++)
                                for (int j = i + 1; j < matrix.Length; j++)
                                {
                                    if (matrix[i] == matrix[j])
                                    {
                                        matrix = (new string(matrix)).Remove(j, 1).ToCharArray();
                                    }
                                }
                            // create array 5*5 
                            char[,] matrix2D = new char[5, 5];
                            for (int i = 0; i < 5; i++)
                            {
                                for (int j = 0; j < 5; j++)
                                {
                                    matrix2D[i, j] = matrix[i * 5 + j];
                                }
                            }

                            char[] words = (Convert.ToString(textBox2.Text)).ToArray();
                            // block block of two letter 
                            for (int j = 0; j < words.Length; j += 2)
                            {

                                char firstletter;
                                char secondletter;
                                //change every j to i 
                                if (words[j] == 'س'||words[j]=='ص')
                                {
                                    words[j] = 'ش';
                                }
                                if (j + 1 < words.Length && words[j + 1] == 'س')
                                {
                                    words[j + 1] = 'ش';
                                }
                                if (j + 1 < words.Length && words[j + 1] == 'ص')
                                {
                                    words[j + 1] = 'ش';
                                }
                                if (j + 1 == words.Length)
                                {
                                    firstletter = words[j];
                                    secondletter = 'ش';
                                }
                                else if ((j + 1 < words.Length && words[j] == words[j + 1]))
                                {
                                    firstletter = words[j];
                                    secondletter = 'ش';
                                    j--;
                                }
                                else
                                {
                                    firstletter = words[j];
                                    secondletter = words[j + 1];
                                }
                                int firstx = 0, fristy = 0, secondx = 0, secondy = 0;
                                for (int row = 0; row < 5; row++)
                                {
                                    for (int col = 0; col < 5; col++)
                                    {
                                        if (firstletter == matrix2D[row, col])
                                        {
                                            firstx = row;
                                            fristy = col;
                                        }
                                        if (secondletter == matrix2D[row, col])
                                        {
                                            secondx = row;
                                            secondy = col;
                                        }
                                    }
                                }
                                if (firstx == secondx)
                                { // same row 

                                    textBox1.Text += matrix2D[firstx, ((fristy - 1) % 5)].ToString();
                                    textBox1.Text += matrix2D[secondx, ((secondy - 1) % 5)].ToString();
                                }

                                else if (fristy == secondy)
                                {
                                    //same col 
                                    textBox1.Text += matrix2D[(firstx - 1) % 5, fristy].ToString();
                                    textBox1.Text += matrix2D[(secondx - 1) % 5, secondy].ToString();
                                }
                                else
                                {//Different will take intersection 
                                    textBox1.Text += matrix2D[firstx, secondy].ToString();
                                    textBox1.Text += matrix2D[secondx, fristy].ToString();
                                }
                                textBox2.Text = "";
                            }






                        }


                    }
                    //خوارزمية فك تشفر عربي مع تحيات حسام محمد الجرافي 
                    else if (radioButton6.Checked == true)
                    {
                        if (textBox5.Text == "")
                        {
                            MessageBox.Show("enter text in the textBOX  for  decraption  ");
                        }
                        else
                        {
                            RSACryptoServiceProvider decrpt = new RSACryptoServiceProvider();
                            decrpt.ImportParameters(privte_key);
                            byte[] c = Convert.FromBase64String(textBox5.Text);
                            byte[] c1 = decrpt.Decrypt(c, false);
                            textBox1.Text = Encoding.Unicode.GetString(c1);
                        }

                    }
                    //خوارزمية فك تشفر عربي مع تحيات حسام محمد الجرافي 
                    else if( radioButton7.Checked==true)
                    {
                        string ciphertext = textBox2.Text.ToUpper();
                        string plaintext = dncrypt_a(ciphertext);
                        textBox1.Text = plaintext;
                    }

                }

            }
                                                //انتهت خوارزميات التشفير وفك التشفير







            catch (Exception)
            {
                MessageBox.Show(" errrrror in the try ");
            }
        }
        
        private void RadioButton5_CheckedChanged(object sender, EventArgs e)
        { 
           
            if(radioButton5.Checked==true)
            {
                Form2 form = new Form2();
                form.Show();
            }
            

           
        }

        private void RadioButton4_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton4.Checked == true)
            {
                textBox4.Hide();
                label4.Hide();
                textBox5.Hide();
            }
            else
            {
                textBox4.Show();
                label4.Show();
                textBox5.Show();
            }
        }

        private void RadioButton3_CheckedChanged(object sender, EventArgs e)
        {/*
            if (radioButton3.Checked == true)
            {
                textBox4.Hide();
                label4.Hide();
            }
            else
            {
                textBox4.Show();
                label4.Show();
            }*/
            if (radioButton3.Checked == true)
            {
                textBox4.Hide();
                label4.Hide();
                textBox5.Hide();
                /* label4.Hide();*/

            }
            else
            {
                textBox4.Show();
                label4.Show();
                textBox5.Show();
            }



        }

        private void ComboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

            if (comboBox1.Text == "Arabic")
            {
                this.RightToLeftLayout = true;
                this.RightToLeft = RightToLeft.Yes;


                this.Text = "جميع التشفير ";
                label1.Text = " النص الاصلي ";
                label2.Text = "النص المشفر";
                label3.Text = "المفتاح ";
                label4.Text = "معامل الضرب ";
                button1.Text = "تشفير ";
                button2.Text = "فك التشفير ";
                label5.Text = "اختر اللغه ";
                radioButton1.Text = "خوارزمية القيصر ";
                radioButton2.Text = "خوارزمية الافاين";
                radioButton3.Text = "خوارزمية العب ب النار";
                radioButton4.Text = "حوارزمية فيجنير ";
                radioButton5.Text = "خوارزمية ارسال المفتاح ";
                
                  
            }
             else 
            {
                this.RightToLeftLayout = false;
                this.RightToLeft = RightToLeft.No;

                this.Text = "All Encraptographec";
                label1.Text = "PLANT TEXT";
                label2.Text = "CIPHER TEXT";
                label3.Text = "KEY";
                label4.Text = "VALUE OF A";
                button1.Text = "Encraption";
                button2.Text = "Decraption";
                label5.Text = "Choose your language";
                radioButton1.Text = "Caser encrption";
                radioButton2.Text = "Affin encraption";
                radioButton3.Text = "play fire";
                radioButton4.Text = "Vigenere encrapion";
                radioButton5.Text = "Send The key";


            }


            }

        private void RadioButton1_CheckedChanged(object sender, EventArgs e)
        {
            if(radioButton1.Checked==true)
            {
                textBox4.Hide();
                label4.Hide();
                textBox5.Hide();
               /* label4.Hide();*/

            }
            else
            {
                textBox4.Show();
                label4.Show();
                textBox5.Show();
            }
        }

        private void RadioButton2_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton2.Checked == true)
            {
                
                textBox5.Hide();
                /* label4.Hide();*/

            }
            else
            {
                textBox4.Show();
                label4.Show();
                textBox5.Show();
            }
        }

        private void RadioButton6_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton6.Checked == true)
            {
                textBox4.Hide();
                label4.Hide();
                /* label4.Hide();*/

            }
            else
            {
                textBox4.Show();
                label4.Show();
             
            }
        }

        private void RadioButton7_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton7.Checked == true)
            {
                textBox4.Hide();
                label4.Hide();
                textBox5.Hide();
                label3.Hide();
                textBox3.Hide();
                /* label4.Hide();*/

            }
            else
            {
                textBox4.Show();
                label4.Show();
                textBox5.Show();
                label3.Show();
                textBox3.Show();
            }
        }

        private void label6_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void textBox5_TextChanged(object sender, EventArgs e)
        {

        }

        private void groupBox1_Enter(object sender, EventArgs e)
        {

        }

        private void textBox4_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
