#pragma once
#include<iostream>

using namespace std;

//-------------------------------------------
// User-defined parameters
//-------------------------------------------

double V_initial = 0;//volume L
double con_initial = 0; // mol/L  2e-5/(dia_initial/2 * dia_initial/2 * hei_initial * 3.1415926536 *beta)  18science:Synthesis of Colloidal COF Seeds (HHTP, 0.02 mmol, BA, 0.03 mmol))
double hei_initial = 0; // nm
double dia_initial = 0; // nm
int addition_number = 30;//number of addition
int addition_interval = 1200; //time interval s
double C_hhtp_add = 0.002; //monomer concentration mol/L
double V_add[] = {0.002,0.002,0.002,0.002,0.002076,0.003774,0.006216,0.009534,0.013866,0.019344,0.026106,0.034284,0.044016,0.055434,0.068676,0.083874,0.101166,0.120684,0.142566,0.160384,0.002,0.002,0.002,0.0037,0.0061,0.0091,0.0127,0.0169,0.0217,0.023799999999999974}; //volume of addition L
double min_c = 1e-11;//min monomer concentration mol/L


//--------------------------------------------------------
// crystal 
// -------------------------------------------------------

//struct
struct crystal_struct {
	double dia; //nuclei_diameter nm
	double hei; // nuclei_height nm
	double concentration; //concentration mol/L
} crystal[1000000];


//---------------------------------------------------------------------
// The following parameters are code internal calculation parameters
// According to different units
//---------------------------------------------------------------------

//step
//const int max_step = 86400000; //max_step
float i_step = 0; //step
int i_ = -1; //lengh of crystal - 1
int max_crystal_length; //Optimize process parameters

//s
double time_unit = 0.001; //unit_time s
double t;    //time s
double t_in; //induction time  s
int last_add_monomer_time = 0;//The last time of monomer addition s

//L
double V;    //volume L

//mol/L
double c_monomer_hhtp=0; //monomer concentration mol/L
double c_consum_nucleation = 0; //monomer concentration consumption from nucleation mol/L
double c_consum_growth = 0; //monomer concentration consumption from growth mol/L
double c_consum = 0;//monomer concentration consumption mol/L
double c_nucleus = 0;  //total nuclei concentration mol/L

//mol
double monomer_consumption_mol = 0;//total monomer consumption mol
double mol_consum_growth_all = 0; //monomer consumption from nucleation mol
double mol_consum_nucleation_all = 0; //monomer consumption from nucleation mol
double mol_addition = 0; //monomer addition mol

//nm
double intver = 0.001; //Optimize process parameters
double ave_d = 0;//average diameter
double max_dia = 0;//largest diameter

//number
int max_step_rale = 0; //final max_step
int i_addition = 0;//number of addition
int point_number = 0; //number of addition = addition_number
int struct_length = 10000; //nuclri struct length

//counter(Judgment boundary condition)
int point_optimize = 0; // last optimize
int point_end = 0; //=1 end simulation
int point_addition = 1;//=0 monomer addition
int point_it = 1; // =0 induction time
int point_out = 1; //Output data : monomer concentration = 0






