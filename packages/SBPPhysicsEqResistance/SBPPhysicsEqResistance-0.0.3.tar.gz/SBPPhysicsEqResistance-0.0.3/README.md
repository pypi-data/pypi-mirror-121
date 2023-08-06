# SBPPhysicsEqResistance Package

Hi, I'm Mohammad Ghiasvand Mohammadkhani, the author of this python scientific package .

To use this scientific package,at first you need to install it by pip command, then you have to code the text in the quotation, "from SBPPhysicsEqResistance import SBPPhysicsEqResistance" ;Then if you want to see an output from that, you can code one of the texts in the quotations, "print(SBPPhysicsEqResistance.series())" or "print(SBPPhysicsEqResistance.parallel())" ;You can pass the parallel or series function as many arguments as you want and you can also use the functions inside the other ones ;If you pay attention to the examples below, you will understand everything completely .

print(SBPPhysicsEqResistance.parallel(12, 6, 4, 2, 1)) => output = 0.5

print(SBPPhysicsEqResistance.series(4, 3, 2, 1)) => output = 10

print(SBPPhysicsEqResistance.parallel(6, 3, SBPPhysicsEqResistance.series(1, 1))) => output = 1

print(SBPPhysicsEqResistance.series(4, 5, SBPPhysicsEqResistance.parallel(2, 2))) => output = 10


But please note that you will encounter to an error if you enter non-positive values for your resistors because a resistor with a non-positive value does not exist . 

Thanks,
Hope to be helpful for you .
