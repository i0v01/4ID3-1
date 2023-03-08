using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MultiViewTemplate.Views
{
    public partial class Login : Form
    {
        MainPage _parent;
        public Login(MainPage parent)
        {
            InitializeComponent();
            _parent = parent;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (txt_email.Text == "winforms@example.com" && txt_password.Text == "9055259140")
            {
                _parent.btn_Form1.Visible = true;
                _parent.btn_Form2.Visible = true;
                _parent.btn_Form3.Visible = true;
                _parent.btn_Form4.Visible = true;
            }
        }
    }
}
