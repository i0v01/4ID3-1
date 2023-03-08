using MultiViewTemplate.Views;


namespace MultiViewTemplate
{
    public partial class MainPage : Form
    {
        public Login _loginForm;
        public Form1 _form1;
        public Form2 _form2;
        public Form3 _form3;    
        public Form4 _form4;

        public MainPage()
        {
            InitializeComponent();
            _loginForm = new Login(this);
            _form1 = new Form1(this);
            _form2 = new Form2(this);
            _form3 = new Form3(this);
            _form4 = new Form4(this);

            btn_Form1.Visible= false;
            btn_Form2.Visible = false;
            btn_Form3.Visible = false;
            btn_Form4.Visible = false;

            
            _loginForm.TopLevel = false;
            panel1.Controls.Add(_loginForm);
            _loginForm.BringToFront();
            _loginForm.Show();
        }

        private void btn_login_Click(object sender, EventArgs e)
        {
            Login login = new Login(this);
            login.TopLevel = false;
            panel1.Controls.Add(login);
            login.BringToFront();
            login.Show();
            _loginForm = login;

        }

        private void btn_Form1_Click(object sender, EventArgs e)
        {
            //Form1 f1 = new Form1(this);
            _form1.TopLevel = false;
            panel1.Controls.Add(_form1);
            _form1.BringToFront();
            _form1.Show();
            //_form1 = f1;

        }
        
        private void btn_Form2_Click(object sender, EventArgs e)
        {
            //Form2 f2 = new Form2(this);
            _form2.TopLevel = false;
            panel1.Controls.Add(_form2);
            _form2.BringToFront();
            _form2.Show();
            //_form2 = f2;
        }
        
        private void btn_Form3_Click(object sender, EventArgs e)
        {
            //Form3 f3 = new Form3(this);
            _form3.TopLevel = false;
            panel1.Controls.Add(_form3);
            _form3.BringToFront();
            _form3.Show();
            //_form3 = f3;
        }

        private void btn_Form4_Click(object sender, EventArgs e)
        {
            //Form4 f4 = new Form4(this);
            _form4.TopLevel = false;
            panel1.Controls.Add(_form4);
            _form4.BringToFront();
            _form4.Show();
            //_form4 = f4;
        }
    }
}