### the following should works somehow as they are given in the presentation (Symmetry, topology, and
### visualization of crystal structures) of VESTA author Koichi Momma.

##1- For Windows & Linux
#VESTA -open test.cif
#VESTA -list bond
#VESTA -export_img test.png
#VESTA close

#2-To change or the format or write .vesta file, we can use the following command:

VESTA -nogui -i test.vasp -o option=cartesain test.vesta



#VESTA -nogui -i test.cif -o format=rietan test.ins
#VESTA -nogui -i test.cif -o option=cartesian test.vasp
#VESTA -nogui -i test.cif -list bond angle poly
#
#Note:
#
#-i : input
#-o : output
#
#format : Examples: cif, xyz, rietan, pdb etc (see the  for input and output formate https://jp-minerals.org/vesta/en/)
#
#option :  cartesian,pcell,reduced,as_displayed
#
#here cartesian will write cartesian vasp file. while reduced will write in diret co-ordinate form.
#
#ChatGPT explanation of
#
#pcell: 	Use primitive cell instead of the full conventional cell. (Not understood)
#
#as_displayed:  Save only what's visible on screen (e.g., cleaved surface, zoomed portion, etc.). Very useful for making figures or surface cuts. (Not understood),
