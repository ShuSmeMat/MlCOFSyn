#pragma once
#include <iostream>
#include <cmath>

using std::cout;
using std::endl;

// Microscopic parameters
const double kbf1 = 0.40667;  // mol/L/s
const double kbf2 = 1210.7;   // mol/L/s
const double kbf3 = 20361.1;   // mol/L/s
const double BETA = 0.741640598; // number of HHTP units per volume (nm^3)
const double N_nuc_hhtp = 20;  // number of monomers for nucleation
const double d = 0.346;         // distance between layers nm
const double S = 1.0;             // disk-shaped crystals
const double kappa = 3.897;     // lateral area per number of vertices in 2D lattice nm^2
const double d_nuc_init = 7.002431562087647; // nm
const double h_nuc_init = 0.7002431562087647; // nm
const double PI = 3.1415926536; // pi

double induction_time(double kbf1, double c_monomer);
double nucleation_rate(double kbf1, double kbf2, double kbf3, double c_monomer);
double nucleation_rate_c_monomer(double kbf1, double kbf2, double kbf3, double c_monomer, double N_nuc_hhtp);
double growth_rate_ver(double kbf1, double kbf2, double kbf3, double c_monomer, double d);
double growth_rate_lat(double kbf1, double kbf2, double kbf3, double c_monomer, double S, double kappa);
double growth_rate_lat_ver_c_monomer(double kbf1, double kbf2, double kbf3, double c_monomer, double c_monomer_nucleus, double dia, double hei, double BETA);

double induction_time(double kbf1, double c_monomer) {
    return 0.068916294722367 / (kbf1 * c_monomer); // s
}

double nucleation_rate(double kbf1, double kbf2, double kbf3, double c_monomer) {
    double gamma1 = kbf2 / kbf1;
    double gamma2 = kbf3 / kbf1;
    return 0.030363169641638444 * c_monomer * c_monomer * kbf1 * pow(gamma1, 0.05) * pow(gamma2, 0.025); // mol/L/s
}

double nucleation_rate_c_monomer(double kbf1, double kbf2, double kbf3, double c_monomer, double N_nuc_hhtp) {
    return nucleation_rate(kbf1, kbf2, kbf3, c_monomer) * N_nuc_hhtp; // mol/L/s
}

double growth_rate_ver(double kbf1, double kbf2, double kbf3, double c_monomer, double d) { // nm/s
    double gamma1 = kbf2 / kbf1;
    double gamma2 = kbf3 / kbf1;
    double kbf23 = 2008.0000177867732 - 199.49404467629432 * pow(gamma2, 1.0 / 7) +
                   sqrt(pow(gamma1, 3) * pow(gamma2, 1.0 / 3) /
                   (53248.465539123325 * gamma1 + 13199.729668575232 * gamma2));
    return d * kbf1 * c_monomer * kbf23;
}

double growth_rate_lat(double kbf1, double kbf2, double kbf3, double c_monomer, double S, double kappa) { // nm/s
    double gamma1 = kbf2 / kbf1;
    double gamma2 = kbf3 / kbf1;
    return S * kbf1 * c_monomer * sqrt(pow(gamma1, 2) * gamma2 * kappa /
             (0.8339246759138563 * gamma1 + 1.259398254488272 * gamma2));
}

double growth_rate_lat_ver_c_monomer(double kbf1, double kbf2, double kbf3, double c_monomer,
                                      double c_monomer_nucleus, double dia, double hei,
                                      double BETA, double S, double kappa, double d) {
    return PI / 4 * BETA * (growth_rate_ver(kbf1, kbf2, kbf3, c_monomer, d) * dia * dia +
                             2 * dia * hei * growth_rate_lat(kbf1, kbf2, kbf3, c_monomer, S, kappa)) * c_monomer_nucleus;
}