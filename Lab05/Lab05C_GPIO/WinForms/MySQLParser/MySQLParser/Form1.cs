using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MySql.Data.MySqlClient;

namespace MySQLParser
{   
    public class Model
    {
        public int iddata { get; set; }
        public string DeviceName { get; set; }
        public string SensorName { get; set; }    

        public string SensorValue { get; set; } 
    }

    public partial class Form1 : Form
    {

        
        public Form1()
        {
            InitializeComponent();
        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {


            try
            {
                MySqlConnection conn = new MySqlConnection("server=" + txt_dbip.Text + ";user id=" + txt_user.Text  + ";password=" + txt_pass.Text + ";database=" + txt_schema.Text);
                conn.Open();
                String query = txt_query.Text;
                MySqlCommand cmd = new MySqlCommand(query, conn);
                MySqlDataReader reader = cmd.ExecuteReader();


                List<Model> dbModel = new List<Model>();

                while (reader.Read())
                {
                    for(int i = 0; i < reader.FieldCount; i+=5)
                    {


                        Console.WriteLine(reader.GetValue(i));

                        dbModel.Add(new Model()
                        {
                            iddata = int.Parse(reader.GetValue(i).ToString()),
                            DeviceName = reader.GetValue(i + 1).ToString(),
                            SensorName = reader.GetValue(i + 2).ToString(),
                            SensorValue = reader.GetValue(i + 3).ToString()
                        }) ;
                        Console.WriteLine(dbModel[i].ToString());

                    }
                    var bindingList = new BindingList<Model>(dbModel);
                    var source = new BindingSource(bindingList, null);
                    dataGrid.DataSource = source;

                    //Console.WriteLine(dbModel);
                        
                    
                }
                reader.Close();

            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }



        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox4_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox5_TextChanged(object sender, EventArgs e)
        {

        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }
}
