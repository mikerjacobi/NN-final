/* Flatworld II V1.0 main test program.  Uses GLUT/OpenGL for sim loop & visualization. 
*  Created 17 March 2009 by T. Caudell
*  Updated 20 Sept 2009, tpc
*  Modified by Thomas Caudell 9/13/12
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

/* Graphics window global variables */
int wh = 600, ww = 800 ;
float frustrum_theta=60.0, frustrum_znear=0.1, frustrum_zfar=1000.0 ;

/* Locomotion global variables */
float locox=0.0, locoy=0.0, locoz=-30.0, locothx=0.0, locothy=0.0, locothz=0.0 ;

/* Global pointer to current Flatworld */
WORLD_TYPE *Flatworld ;
int simtime = 0 ;
int runflag = 1 ;  
int agent_track_flag = 0 ;
AGENT_TYPE *current_agent ;

#include "Distributions_Funcs.c"
#include "FlatworldIICore.c"
#include "GraphicsCore.c"
#include "Controller.c"


/* GLUT Functions ---------------------------------------------------------------------------------------*/

void ginit(void)
{ /* This function initializes the graphics, and creates and initializes the world an the agent. tpc */
	glViewport(0,0,ww,wh) ;
	glMatrixMode( GL_PROJECTION) ;
	glLoadIdentity() ;	
	gluPerspective( frustrum_theta,(GLfloat)ww/(GLfloat)wh,frustrum_znear,frustrum_zfar);
	glMatrixMode(GL_MODELVIEW);
	glClearColor(0.0, 0.0, 0.0, 1.0);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT ) ;
	glEnable (GL_DEPTH_TEST);
	glShadeModel(GL_SMOOTH) ;
	glEnable(GL_LIGHTING) ;
	
	
}

void reshape(int w, int h)
{
	glViewport(0,0,w,h) ;
	glMatrixMode( GL_PROJECTION) ;
	glLoadIdentity() ;
	gluPerspective( frustrum_theta,(GLfloat)w/(GLfloat)h,frustrum_znear,frustrum_zfar);
	/* update ww0,wh0 */
	ww = w ;
	wh = h ;
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
}

void keyboard(unsigned char key, int x, int y)
{
  switch (key) {
		case 'q':
			 exit(0);
			 break;
    case 'j' :
			locothx = 0.0 ;
			locothy = 0.0 ;
			locothz = 0.0 ;
			locox = 0.0 ;
			locoy = 0.0 ;
			locoz = -20.0 ;
			break ;
    case 'o':
      runflag = 1 ;
      break ;
    case 'p':
      runflag = 0 ;
      break; 
		case 'f':
			locoz += 1.0 ;
			break;
		case 'r':
			locoz -= 1.0 ;
			break;
		case 'd':
			locox -= 2.0 ;
			break;
		case 'a':
			locox += 2.0 ;
			break;
		case 'w':
			locoy -= 2.0 ;
			break;
		case 's':
			locoy += 2.0 ;
			break;
		case 'u':
			locothx += 1.0 ;
			break;
		case 'm':
			locothx -= 1.0 ;
			break;
		case 'h':
			locothy += 1.0 ;
			break;
		case 'k':
			locothy -= 1.0 ;
			break;
		case 'g':
			locothz += 1.0 ;
			break;
		case 'y':
			locothz -= 1.0 ;
			break;
    case 't':
      if( agent_track_flag==1)
        agent_track_flag = 0 ;
      else 
        agent_track_flag = 1 ;
     break ;
  }
}

void gz_SetWorldLighting(void)
{
	float ldir0[4],lamb0[4],ldif0[4],lspec0[4] ;
	
  /* Light0 */
	ldir0[0] = 1.0 ;
	ldir0[1] = 1.0 ;
	ldir0[2] = 1.0 ;
	ldir0[3] = 0.0 ;
	glLightfv(GL_LIGHT0, GL_POSITION, ldir0 ) ;
	lamb0[0] = 0.1;
	lamb0[1] = 0.1 ;
	lamb0[2] = 0.1 ;
	lamb0[3] = 1.0 ;
	glLightfv(GL_LIGHT0, GL_AMBIENT, lamb0 ) ;
	ldif0[0] = 0.8 ;
	ldif0[1] = 0.8 ;
	ldif0[2] = 0.8 ;
	ldif0[3] = 1.0 ;
	glLightfv(GL_LIGHT0, GL_DIFFUSE, ldif0 ) ;
	lspec0[0] = 0.0 ;
	lspec0[1] = 0.0 ;
	lspec0[2] = 0.0 ;
	lspec0[3] = 1.0 ;
	glLightfv(GL_LIGHT0, GL_SPECULAR, lspec0) ;
	
	/* Light1 */
	ldir0[0] = -1.0 ;
	ldir0[1] = -1.0 ;
	ldir0[2] = -1.0 ;
	ldir0[3] = 0.0 ;
	glLightfv(GL_LIGHT1, GL_POSITION, ldir0 ) ;
	lamb0[0] = 0.1;
	lamb0[1] = 0.1 ;
	lamb0[2] = 0.1 ;
	lamb0[3] = 1.0 ;
	glLightfv(GL_LIGHT1, GL_AMBIENT, lamb0 ) ;
	ldif0[0] = 0.8 ;
	ldif0[1] = 0.8 ;
	ldif0[2] = 0.8 ;
	ldif0[3] = 1.0 ;
	glLightfv(GL_LIGHT1, GL_DIFFUSE, ldif0 ) ;
	lspec0[0] = 0.0 ;
	lspec0[1] = 0.0 ;
	lspec0[2] = 0.0 ;
	lspec0[3] = 1.0 ;
	glLightfv(GL_LIGHT1, GL_SPECULAR, lspec0) ;
}

void display(void)
{    
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
  glDepthFunc(GL_LEQUAL) ;

	glEnable(GL_LIGHT0 ) ;
	glEnable(GL_LIGHT1 ) ;
	gz_SetWorldLighting() ;
  
  /* Do observer locomotion */
	glLoadIdentity();
	glTranslatef(0.0,0.0,6.0) ;
	glTranslatef(locox, locoy, locoz) ;
	glRotatef(locothx,1.0,0.0,0.0);
	glRotatef(locothy,0.0,1.0,0.0);
	glRotatef(locothz,0.0,0.0,1.0);

  /* do the graphics for the world, agents, and objects */
	draw_Flatworld() ;

  /* Ad hoc controller for agents.  To be replaced by neural network controller */
  if( runflag==1 )
    agents_controller( Flatworld ) ;  /* See file Controller.c for this function */
    
  if( agent_track_flag==1 )
  {
    locox = -current_agent->outstate->x ;
    locoy = -current_agent->outstate->y ;
  }  
  /* tick = 0.1 second sim word time */
  simtime++ ;
  
	glFlush();
	glutSwapBuffers() ;
}

void idle(void)
{	
	glutPostRedisplay() ;
}

/* Main Loop ---------------------------------------------------------------------------------------*/
int main(int argc, char** argv)
{
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA | GLUT_DOUBLE | GLUT_DEPTH );
	glutInitWindowSize (ww, wh);
	glutInitWindowPosition (100, 100);
	glutCreateWindow ("Flatworld II Program");
	init(1,0);
	glutIdleFunc (idle);
	glutReshapeFunc (reshape);
	glutDisplayFunc(display); 
	glutKeyboardFunc (keyboard);
		
	glutMainLoop();
	return 0; 
}

