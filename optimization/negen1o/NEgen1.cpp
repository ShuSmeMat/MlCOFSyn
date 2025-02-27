#include<iostream>
#include<fstream>
#include<numeric>
#include<algorithm>
#include<iomanip>
#include "cof_parameter.h"
#include "cof_function.h"
#include<queue>
using namespace std;
using std::accumulate;

int main() {

	c_monomer_hhtp = (c_monomer_hhtp * V_initial + C_hhtp_add * V_add[i_addition]) / (V_add[i_addition] + V_initial); //monomer concentration mol/L
	V = V_add[i_addition];//volume L
	mol_addition = mol_addition + C_hhtp_add * V_add[i_addition];//monomer mol
	t = induction_time(kbf1, c_monomer_hhtp);//time s
	i_addition++;//number of additions


	//output
	cout << i_step << "   ";
	cout << t << "   ";
	cout << V << "   ";
	cout << "0   0  "; //average_dia, max_dia
	cout << setprecision(8) << c_nucleus << "   ";
	cout << setprecision(8) << c_monomer_hhtp << "   ";
	cout << setprecision(8) << c_consum_growth << "   ";
	cout << setprecision(8) << c_consum_nucleation << "    ";
	cout << setprecision(8) << mol_consum_growth_all << "   ";
	cout << setprecision(8) << mol_consum_nucleation_all << "    ";
	cout << setprecision(8) << V * c_monomer_hhtp << "     ";
	cout << setprecision(8) << (V - V_initial) * C_hhtp_add << "      ";
	cout << setprecision(8) << (V - V_initial) * C_hhtp_add / (2e-5) << endl; //equiv

	int i = 0;
	while(true)
	{
		i_ = i_ + 1; //nuclei struct length
		i_step = i; //step
		t = t + time_unit; //time

		c_consum_growth = 0;//monomer consumption from growth mol/l

		//induction time
		if (point_it == 0) {
			point_it = 1;
			t_in = induction_time(kbf1, c_monomer_hhtp);
			double dia;
			double hei;
			double con;
			//growth
			double it_c_consum_growth = 0; // mol/L
			for (int it_i = 0; it_i < t_in / time_unit + 1; it_i++) {
				for (int j = 0; j < i_; j++) {

					dia = crystal[j].dia; //diameter nm

					hei = crystal[j].hei; //height nm

					con = crystal[j].concentration; //nucei cocentration mol/L

					//it_c_consum_growth = it_c_consum_growth + time_unit * growth_rate_lat_ver_c_monomer(kbf1, kbf2, kbf3, c_monomer_hhtp, con, dia, hei,beta, S ,kappa, d); //nuclei concentration

					crystal[j].dia = crystal[j].dia + time_unit * growth_rate_lat(kbf1, kbf2, kbf3, c_monomer_hhtp, S, kappa);//diameter nm

					crystal[j].hei = crystal[j].hei + time_unit * growth_rate_ver(kbf1, kbf2, kbf3, c_monomer_hhtp, d); //height nm

					it_c_consum_growth = it_c_consum_growth + 3.1415926536 / 4 * (crystal[j].dia * crystal[j].dia * crystal[j].hei - dia * dia * hei) * BETA * con;//monomer cocentration in induction time mol/L
				}

				c_monomer_hhtp = c_monomer_hhtp - it_c_consum_growth;//monomer concentration mol/L
				c_consum_growth = it_c_consum_growth;//monomer consumption from growth mol/l
				mol_consum_growth_all = mol_consum_growth_all + it_c_consum_growth * V;//monomer concentration mol


				//output
				if (it_i % 10000 == 0 || c_monomer_hhtp <  min_c) {

					//diameter
					ave_d = 0.00000;
					max_dia = 0.00000;
					for (int k = 0; k < i_ + 1; k++)
					{
						//v_check = v_check+ 3.1415926536 / 4 * crystal_nucleus[k].crystal_nucleus_dia * crystal_nucleus[k].crystal_nucleus_dia * crystal_nucleus[k].crystal_nucleus_hei * crystal_nucleus[k].crystal_nucleus_concentration * V * 6.02214076e23;
						//output <<"  !!!!!!!!!!!!!"<< mol * 6.02214076e23 << "    " << v_check * beta <<(mol * 6.02214076e23- v_check * beta)/ 6.02214076e23 << endl;
						ave_d = ave_d + crystal[k].concentration * crystal[k].dia;
						if (crystal[k].dia > max_dia)
							max_dia = crystal[k].dia;
					}


				    //output
					cout << i << "   ";
					cout << t << "   ";
					cout << V << "   ";
					cout << setprecision(8) << ave_d / c_nucleus << "   ";
					cout << setprecision(8) << max_dia << "    ";
					cout << setprecision(8) << c_nucleus << "   ";
					cout << setprecision(8) << c_monomer_hhtp << "   ";
					cout << setprecision(8) << c_consum_growth << "                    0                "; //c_consum_nucleation = 0
					cout << setprecision(8) << mol_consum_growth_all << "   ";
					cout << setprecision(8) << mol_consum_nucleation_all << "    ";
					cout << setprecision(8) << V * c_monomer_hhtp << "     ";
					cout << i_addition << endl; //number of additions


					//output << i << "   " << setprecision(8) << t << "   " << setprecision(6) << V << "   " << setprecision(6) << ave_d / c_nucleus << "   " << setprecision(6) << max_dia << "    " << c_nucleus << "   " << setprecision(10) <<c_monomer_hhtp << "   " <<setprecision(10)<< c_consum_nuc << "   " << c_consum_growth << "   " << cunn << endl;
				}

				it_c_consum_growth = 0; //nucei cocentration in induction time mol/L


				//c_monomer_hhtp =0
				if (c_monomer_hhtp < min_c) {
					break;
				}
				else {
					i = i + 1;
					t = t + time_unit;

				}
			}

		}


		//growth
		double dia;
		double hei;
		double con;
		for (int j = 0; j < i_; j++) {
			
			dia = crystal[j].dia; //diameter nm

			hei = crystal[j].hei; //height nm

			con = crystal[j].concentration; //nuclei concentration mol/L

			//c_consum_growth = c_consum_growth + time_unit * growth_rate_lat_ver_c_monomer(kbf1, kbf2, kbf3, c_monomer_hhtp, con, dia, hei, beta, S, kappa, d); 

			crystal[j].dia = crystal[j].dia + time_unit * growth_rate_lat(kbf1, kbf2, kbf3, c_monomer_hhtp, S, kappa);//diameter nm

			crystal[j].hei = crystal[j].hei + time_unit * growth_rate_ver(kbf1, kbf2, kbf3, c_monomer_hhtp, d);//height nm

			c_consum_growth = c_consum_growth + 3.1415926536 / 4 * (crystal[j].dia * crystal[j].dia * crystal[j].hei - dia * dia * hei) * BETA * con;//monomer cocentration from growth in induction time mol/L

		}
		mol_consum_growth_all = mol_consum_growth_all + c_consum_growth * V;//monomer cocentration from growth mol


		c_consum_nucleation = nucleation_rate_c_monomer(kbf1, kbf2, kbf3, c_monomer_hhtp, N_nuc_hhtp) * time_unit;//monomer cocentration from nucleation mol/L
		mol_consum_nucleation_all = mol_consum_nucleation_all + c_consum_nucleation * V;//monomer cocentration from growth and nucleation mol

		c_consum = c_consum_growth + c_consum_nucleation;//monomer cocentration from nucleation and growth mol/L


		//Determine whether the monomer concentration is 0
		if (c_monomer_hhtp < min_c) { //monomer concentration = 0

			//interval_time - reaction_time
			t = t + addition_interval - (t - last_add_monomer_time);//s

			//new time_
			double time_ = time_unit * c_monomer_hhtp / (c_consum / time_unit); //s
			c_consum_growth = c_consum_growth * (time_ / time_unit); //monomer cocentration from growth  mol/L
			c_consum_nucleation = c_consum_nucleation * (time_ / time_unit); //monomer cocentration from nucleation mol/L
			monomer_consumption_mol = mol_consum_growth_all + mol_consum_nucleation_all;//monomer cocentration from growth and nucleation mol

			//new nuclei

			crystal[i_].dia = d_nuc_init;//diameter nm
			crystal[i_].hei = h_nuc_init;//height nm
			crystal[i_].concentration = nucleation_rate(kbf1, kbf2, kbf3, c_monomer_hhtp) * time_;//nuclei concentration mol/L
			c_nucleus = c_nucleus + crystal[i_].concentration;//nuclei concentration mol/L

			point_addition = 0;
			point_out = 0;

			//c_monomer_hhtp = 0;

			//counter(number of addition -> max)
			if (point_number == 1) {
				point_optimize = 1;
			}

		}
		else {//monomer concentration != 0
			monomer_consumption_mol = mol_consum_growth_all + mol_consum_nucleation_all;

			//new nuclei
			crystal[i_].dia = d_nuc_init;//diameter nm
			crystal[i_].hei = h_nuc_init;//height nm
			crystal[i_].concentration = nucleation_rate(kbf1, kbf2, kbf3, c_monomer_hhtp) * time_unit;//nuclei concentration mol/L
			c_nucleus = c_nucleus + crystal[i_].concentration;//nuclei concentration mol/L

			c_monomer_hhtp = c_monomer_hhtp - c_consum;//monomer concentration mol/L

		}


        //output
		if (i>-1 || point_out == 0) {
			point_out = 1;

			//diameter
			ave_d = 0.00000;
			max_dia = 0.00000;
			for (int k = 0; k < i_ + 1; k++)
			{
				//v_check = v_check+ 3.1415926536 / 4 * crystal_nucleus[k].crystal_nucleus_dia * crystal_nucleus[k].crystal_nucleus_dia * crystal_nucleus[k].crystal_nucleus_hei * crystal_nucleus[k].crystal_nucleus_concentration * V * 6.02214076e23;
				//output <<"  !!!!!!!!!!!!!"<< mol * 6.02214076e23 << "    " << v_check * beta <<(mol * 6.02214076e23- v_check * beta)/ 6.02214076e23 << endl;
				ave_d = ave_d + crystal[k].concentration * crystal[k].dia;
				if (crystal[k].dia > max_dia)
					max_dia = crystal[k].dia;
			}
			
			//output
			cout << i << "   ";
			cout << t << "   ";
			cout << V << "   ";
			cout << setprecision(8) << ave_d / c_nucleus << "   ";
			cout << setprecision(8) << max_dia << "    ";
			cout << setprecision(8) << c_nucleus << "   ";
			cout << setprecision(8) << c_monomer_hhtp << "   ";
			cout << setprecision(8) << c_consum_growth << "  "; 
			cout << setprecision(8) << c_consum_nucleation << "  ";
			cout << setprecision(8) << mol_consum_growth_all << "   ";
			cout << setprecision(8) << mol_consum_nucleation_all << "    ";
			cout << setprecision(8) << V * c_monomer_hhtp << "     ";
			cout << i_addition << endl; //number of additions
			//cout << i << "   " << t << "   " <<  V << "   " <<  ave_d / c_nucleus << "   " << max_dia << "    " << c_nucleus << "   " << c_monomer_hhtp << "   " << c_consum_nuc<<"      "<< c_consum_growth <<"     " << mol_consum_growth_all << "          " << mol_consum_nucleation_all << "      " << V * c_monomer_hhtp << "    " << i_addition << endl;
		}

        //add
		if (i_addition < addition_number) {
			if (point_addition == 0) {
				point_addition = 1;
				//new nuclei concentration
				double new_c_nucleus = 0; //nuclei concentration mol/L
				for (int j = 0; j < i_ + 1; j++)
				{
					crystal[j].concentration = crystal[j].concentration * V / (V_add[i_addition] + V);//nuclei concentration mol/L
					new_c_nucleus = crystal[j].concentration + new_c_nucleus;//nuclei concentration mol/L
				}
				c_nucleus = new_c_nucleus;//nuclei concentration mol/L

				//new monomer concentration
				c_monomer_hhtp = (c_monomer_hhtp * V + C_hhtp_add * V_add[i_addition]) / (V_add[i_addition] + V);//monomer concentration mol/L
				mol_addition = mol_addition + C_hhtp_add * V_add[i_addition];//monomer  mol
				V = V + V_add[i_addition];//volume L
				last_add_monomer_time = t;//time s
				i_addition = i_addition + 1;//number of addition
			    point_it = 0;
			}

			// if (i_addition == addition_number) {
			// 	point_number = 1;
			// }
		}
		if (i_addition == addition_number) {
				point_number = 1;
			}

		//optimize
		if ((i % struct_length == 0 && i > 0) || point_optimize == 1) {

			double interval_dia = crystal[0].dia; //Optimize process parameters nm
			int point_j = 0; //Optimize process parameters nm
			double dia_ave_1 = 0; //Optimize process parameters nm
			double hei_ave_1 = 0; //Optimize process parameters nm
			double con_ave_1 = 0; //Optimize process parameters mol/L

			//double check_nuc = 0;
			for (int k = 0; k < i_ + 1; k++) {

				if (interval_dia - intver < crystal[k].dia && crystal[k].dia <= interval_dia) {

					dia_ave_1 = crystal[k].dia * crystal[k].concentration + dia_ave_1; //nm
					hei_ave_1 = crystal[k].hei * crystal[k].concentration + hei_ave_1; //nm
					con_ave_1 = crystal[k].concentration + con_ave_1; //mol/L

					if (k == i_) {

						crystal[point_j].dia = dia_ave_1 / con_ave_1;//nm
						crystal[point_j].hei = hei_ave_1 / con_ave_1;//nm
						crystal[point_j].concentration = con_ave_1;//mol/L
						//check_nuc = check_nuc + con_ave_1;

					}
				}
				else {
					crystal[point_j].dia = dia_ave_1 / con_ave_1;//nm
					crystal[point_j].hei = hei_ave_1 / con_ave_1;//nm
					crystal[point_j].concentration = con_ave_1;//mol/L
					//check_nuc = check_nuc + con_ave_1;

					if (k != i_) {
						point_j = point_j + 1;
					}

					dia_ave_1 = crystal[k].dia * crystal[k].concentration;//nm
					hei_ave_1 = crystal[k].hei * crystal[k].concentration;//nm
					con_ave_1 = crystal[k].concentration;//mol/L
					interval_dia = crystal[k].dia;//nm
			

				}

			}

			//output << c_nucleus<< "            " << check_nuc <<"            " << c_nucleus - check_nuc << endl;
			//c_nucleus = check_nuc;
			dia_ave_1 = 0;
			hei_ave_1 = 0;
			con_ave_1 = 0;
			i_ = point_j;

			if (point_optimize == 1) {
				point_end = 1;
			}

		}
		

		max_step_rale = i;
		max_crystal_length = i_;
		if (point_end == 1)
			break;

		i = i + 1;



	}



	//percentage
	ofstream percentage;
	percentage.open("Percentage(%).txt", ios::out);
	// double dia_hei[1000000];//diameter-height ratio
	double* dia_hei = new double[1000000];
	double ave_dia_hei = 0;//average(diameter-height ratio)
	double dia_hei_sd = 0;//RSD(diameter-height ratio)
	int n_window = 1000; //windows
	double window_size = (crystal[0].dia + 0.00001) / n_window;
	double d_windows_low_bound[1000];
	double d_windows_high_bound[1000];
	double d_windows_Cnuc[1000] = { 0 };
	d_windows_low_bound[0] = 0;
	for (int i = 0; i < n_window - 1; i++) {
		d_windows_high_bound[i] = d_windows_low_bound[i] + window_size;
		d_windows_low_bound[i + 1] = d_windows_high_bound[i];
	}
	d_windows_high_bound[999] = d_windows_low_bound[999] + window_size;

	int i_window = n_window - 1;
	int i_nuc = 0;
	while (true) {
		if (i_nuc > max_crystal_length) {

			break;
		}
		if (i_window == 0) {
			//percentage << "i_window == 0" << endl;
			break;
		}
		if (crystal[i_nuc].dia > d_windows_low_bound[i_window] && crystal[i_nuc].dia <= d_windows_high_bound[i_window]) {
			d_windows_Cnuc[i_window] = d_windows_Cnuc[i_window] + crystal[i_nuc].concentration;
			i_nuc = i_nuc + 1;
			//percentage << max_str  <<"    " << i_nuc << "   " << d_windows_Cnuc[i_window] << endl;

		}
		else {
			//percentage << "i_window=   "<<i_window << endl;
			i_window = i_window - 1;
		}

	}
	double sum_d = 0;
	for (int i = 0; i < n_window; i++) {
		sum_d = sum_d + d_windows_Cnuc[i];
	}
	for (int i = 0; i < n_window; i++) {
		percentage << d_windows_low_bound[i] << "   " << d_windows_high_bound[i] << "   " << d_windows_Cnuc[i] << "   " << d_windows_Cnuc[i] / sum_d << endl;
	}

	//giameter-to-height ratio and data validation
	ofstream dia_hei_;
	dia_hei_.open("dia_hei.txt", ios::out);
	dia_hei_sd = 0;
	double nuc_all = 0;
	double v_all = 0;
	for (int k = 0; k < max_crystal_length; k++)
	{

		dia_hei[k] = crystal[k].dia / crystal[k].hei;
		nuc_all = crystal[k].concentration + nuc_all;
		v_all = v_all + 3.1415926536 / 4 * crystal[k].dia * crystal[k].dia * crystal[k].hei * crystal[k].concentration * V * 6.02214076e23;
		ave_dia_hei = dia_hei[k] * crystal[k].concentration + ave_dia_hei;
		dia_hei_ << k << "   " << dia_hei[k] << "   " << 3.1415926536 * crystal[k].dia / 2 * crystal[k].dia / 2 * crystal[k].hei << "     " << crystal[k].concentration * 6.02214076e23 << endl;
	}
	ave_dia_hei = ave_dia_hei / c_nucleus;
	dia_hei_ << "average_diameter-height_ratio" << "   " << ave_dia_hei << "   " << endl;
	dia_hei_ << "total_nuclei_concentration_opt" << "   " << nuc_all << "   " << "total_nuclei_concentration" << "    " << c_nucleus << endl;
	dia_hei_ << "total_nuclei_volume" << "   " << v_all << "   " << fixed<< setprecision(10)<<v_all * BETA << endl;
	dia_hei_ << "monomer_consumption_mol" << "   " << monomer_consumption_mol << "   " << endl;
	dia_hei_ << "monomer_addition_mol" << "     " << mol_addition << "         " <<  fixed<< setprecision(10)<<6.02214076e23 * mol_addition << "          " << (6.02214076e23 * mol_addition - v_all * BETA) / 6.02214076e23 << "     " << endl;

	for (int k = 0; k < max_crystal_length; k++)
	{
		dia_hei_sd = dia_hei_sd + (dia_hei[k] - ave_dia_hei) * (dia_hei[k] - ave_dia_hei);

	}
	dia_hei_sd = pow(dia_hei_sd / max_crystal_length, 0.5);
	dia_hei_ << "SD" << "   " << dia_hei_sd / ave_dia_hei << "   " << endl;


	// height
	ofstream hei_;
	hei_.open("hei.txt", ios::out);
	double ave_hei = 0;//nm
	double hei_sd = 0;//RSD
	for (int k = 0; k < max_crystal_length; k++)
	{
		dia_hei[k] = crystal[k].hei;
		ave_hei = dia_hei[k] * crystal[k].concentration + ave_hei;
		hei_ << k << "   " << dia_hei[k] << "   " << endl;
	}
	ave_hei = ave_hei / c_nucleus;
	hei_ << "ave" << "   " << ave_hei << "   " << endl;
	for (int k = 0; k < max_crystal_length; k++)
	{
		hei_sd = hei_sd + (dia_hei[k] - ave_hei) * (dia_hei[k] - ave_hei);

	}
	hei_sd = pow(hei_sd / max_crystal_length, 0.5);
	hei_ << "SD" << "   " << hei_sd / ave_hei << "   " << endl;


	//diameter
	ofstream dia_;
	dia_.open("dia.txt", ios::out);
	hei_sd = 0;
	ave_hei = 0;
	for (int k = 0; k < max_crystal_length; k++)
	{
		dia_hei[k] = crystal[k].dia;
		ave_hei = dia_hei[k] * crystal[k].concentration + ave_hei;
		dia_ << k << "   " << dia_hei[k] << "   " << endl;
	}
	ave_hei = ave_hei / c_nucleus;
	dia_ << "ave" << "   " << ave_hei << "   " << endl;
	for (int k = 0; k < max_crystal_length; k++)
	{
		hei_sd = hei_sd + (dia_hei[k] - ave_hei) * (dia_hei[k] - ave_hei);

	}
	hei_sd = pow(hei_sd / max_crystal_length, 0.5);
	dia_ << "SD" << "   " << hei_sd / ave_hei << "   " << endl;
	delete[] dia_hei;
	
}





