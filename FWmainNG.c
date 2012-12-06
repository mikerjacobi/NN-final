/* Flatworld II V1.0 main test program.  Doe not use GLUT/OpenGL for sim loop & visualization. 
*  Created 17 March 2009 by T. Caudell
*  Updated 20 Sept 2009, tpc
*  Updated 14 Nov 2009, tpc
*
*  Copyright University of New Mexico 2009
*/

#include <stdio.h>
#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <GL/glut.h>
#include <GL/glu.h>
#include "Distributions_Funcs.h"
#include "FlatworldIICore.h"
#include "GraphicsCore.h"

#define TRUE 1
#define FALSE 0
#define PI2 6.283185307179586
#define PI 3.141592653589793

/* Global pointer to current Flatworld */
WORLD_TYPE *Flatworld ;
int simtime = 0 ;
int runflag = 1 ;

#include "Distributions_Funcs.c"
#include "FlatworldIICore.c"
#include "Controller.c"

AGENT_TYPE *current_agent ;

/* Main Loop ---------------------------------------------------------------------------------------*/
int main(int argc, char** argv)
{
	init(0,0);
    int t;
  	for( t=0 ; t<3000000 ; t++ )
  	{
    	agents_controller( Flatworld ) ;
    	simtime++ ;
		//if (simtime%2000==0)
		//	printf("simtime:%d ",simtime);
  	}

  	printf("main- terminating normally.\n") ;
  	return 0;
}

