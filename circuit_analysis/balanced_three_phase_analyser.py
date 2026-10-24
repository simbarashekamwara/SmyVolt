
import numpy as np
import matplotlib.pyplot as plt

def analyser():
    """
    This is a balanced 3-Phase analyser with up to n loads either in delta or wye connections.
    """

    #requesting the input from user
    #going to start by Voltage with V_l , V_p for line voltage and phase voltage respectively
    #all volts are in rms 
    #i have made an assumption that v_source is with phase = 0 and that the sources are connected in abc(positive) sequence

    v_source =  float(input("Enter the value of the source voltage: "))
    if input("Is the source wye or delta: ").lower() == "delta":
        v_source /= 3**(1/2)


    #z_y  z_d and z_s represents wye connected impedence , delta connected impedence and line or source impedence respectively

    z_s = np.complex128(input("Enter the source/line impedence in the form a + bj: "))

    print("Enter all the wye connected load impedences in the form a + bj")
    print("Use commas to seperate eg. 1 + 2j, 5+4j, 9+12j")


    z_yeq, z_deq = 0, 0

    if input("Enter 1 if there are wye connected load otherwise 0: ") == "1":
        z_y = np.array([x.strip() for x in input("Delta impedences: ").split(',')], dtype=complex)
        
        #calculating total equivalence of z_delta denoted z_yeq
        z_yeq = z_eq(z_y)
        
    if input("Enter 1 if there are delta connected load otherwise 0: ") == "1":
        z_d = np.array([x.strip() for x in input("Delta impedences: ").split(',')], dtype=complex)
        
        #converting each z_d to z_y denoted z_dy
        z_dy = z_d/3

        #calculating total equivalence of z_delta denoted z_deq
        z_deq = z_eq(z_dy)
        
    #impendece for the whole circuit     
    z_total = z_s + z_yeq + z_deq


    #Calculating the phase current denoted I_a
    I_a = v_source/z_total
    Ia = np.abs(I_a)
    phi = np.angle(I_a, deg=True)
    I_max = Ia*(2**(1/2))

    #Results from the analysis
    print("=" * 50)
    print("RESULTS")
    print("="* 50)
    print(f"Phase current {Ia:.2f} phi={phi:.2f}")
    print(f" i_a(wt) = {I_max:.2f}sin(wt + {np.radians(phi):.3f})")
    print(f" i_b(wt) = {I_max:.2f}sin(wt + {np.radians(phi-120):.3f})")
    print(f" i_c(wt) = {I_max:.2f}sin(wt + {np.radians(phi+120):.3f})")


    #Power calculations
    #s , p, q denotes apparent, active/real and reactive power respectively 
    #pf is the power factor

    s = 3 * v_source * np.conj(I_a)
    p = np.real(s)
    q = np.imag(s)
    pf = p/(np.abs(s))

    print(f"Apparent Power(S): {s:.2f} VA")
    print(f"Active/Real Power(P): {p:.2f} W")
    print(f"Reactive Power(Q): {q:.2f} VAR")
    print(f"Power Factor(PF): {pf:.2f} ")


    #a plot of V_source and I_a 
    pi = np.pi
    wt = np.linspace(0, 5*pi, 500)
    plt.plot(wt, v_source*(2**(1/2))*np.sin(wt), "b", wt, Ia*(2**(1/2))*np.sin(wt- np.radians(phi)), "r")
    plt.axhline(0, color='k', linestyle='-') 
    plt.xlabel("wt")
    plt.show()


def z_eq(arr):
    #arr represents an array containing parallel connected impedences
    #calculates the equivqlence of a parallel impedences up to n impedences
    return ((1 / arr).sum())** (-1)


def main():
    analyser()
    
    
    
    

if __name__ == "__main__":
    main()