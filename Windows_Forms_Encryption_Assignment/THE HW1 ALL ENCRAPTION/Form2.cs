using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace THE_HW1_ALL_ENCRAPTION
{
    public partial class Form2 : Form
    {
        public Form2()
        {
            InitializeComponent();
        }

        private void Button1_Click(object sender, EventArgs e)
        {


            if (textBox1.Text.Trim() != "" && textBox2.Text.Trim() != "" && textBox3.Text.Trim() != "" && textBox4.Text.Trim() != "")
            {
                float p = float.Parse(textBox1.Text);
                float g = float.Parse(textBox2.Text);
                float THE_SENDER_privet_KEY = float.Parse(textBox3.Text);
                float THE_RSEVOR_privet_KEY = float.Parse(textBox3.Text);
                int contp = 0;
                int contg = 0;

                for (int i = 2; i < p; i++)
                {
                    if (p % i == 0)
                    {
                        contp++;
                    }
                }
                for (int i = 2; i < g; i++)
                {
                    if (g % i == 0)
                    {
                        contg++;
                    }
                }



                if (contp == 0)
                {
                    if (contg == 0)
                    {
                        double publicsender = Math.Pow(g, THE_SENDER_privet_KEY) % p;
                        double publicrsevor = Math.Pow(g, THE_RSEVOR_privet_KEY) % p;
                        double secks = Math.Pow(publicrsevor, THE_SENDER_privet_KEY) % p;
                        double seckr = Math.Pow(publicsender, THE_RSEVOR_privet_KEY) % p;
                        textBox5.Text = secks.ToString();
                        textBox6.Text = seckr.ToString();





                    }



                    else
                {
                    MessageBox.Show("G     is not primary number inter primary number plass... ");
                }

            }

            else
            {
                MessageBox.Show("P  is not primary number inter primary number plass... ");
            }

        }
            else
            {

                MessageBox.Show("Error inter your key is it");

            }
        }



        

        private void TextBox6_KeyPress(object sender, KeyPressEventArgs e)
        {
            if((e.KeyChar<48||e.KeyChar>58)&&e.KeyChar!=8)
            {
                /*  textBox1.Handle = true;
                  textBox2.Handle = true;
                  textBox3.Handle = true;
                  textBox4.Handle = true;
                  textBox5.Handle = true;*/

                
              

            }
        }

        private void Form2_Load(object sender, EventArgs e)
        {

        }

        private void label7_Click(object sender, EventArgs e)
        {
           Form1 loginform = new Form1();
            //loginform.Show();
            this.Hide();
        }

        private void groupBox1_Enter(object sender, EventArgs e)
        {

        }
    }
}
