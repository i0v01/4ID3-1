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
    public partial class Form4 : Form
    {
        MainPage _parent;
        public Form4(MainPage parent)
        {
            InitializeComponent();
            _parent = parent;
        }
    }
}
