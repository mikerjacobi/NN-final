/*
 *  Controller.c
 *  For the UNM Neural Networks class, this is the only fle you will need to modify.
 *  It contains the agent initialization code and the agent controller code.  An
 *  example of a non-neural controller is included here, which can be modified.
 *  Note that most all of the functions called here can be found in the 
 *  file FlatworldIICore.c
 *  
 *
 *  Created by Thomas Caudell on 9/15/09.
 *  Modified by Thomas Caudell on 9/30/2010
 *  Copyright 2009 UNM. All rights reserved.
 *
 */
#include <python2.6/Python.h>

const char *pyfile = "Controller.py";
PyObject *controller, *run_brain, *learn;
PyObject *reset, *update_stats, *process_stats;
int last_object = 0;

#define PY(cmd) cmd; PyCheckError(#cmd);
void PyCheckError(const char * err){
  if(PyErr_Occurred()){
    fprintf(stderr, "ERROR IN: %s\n", err);
    PyErr_Print();
    exit(0);
  }
}

PyObject * PyMatrix(float ** mat, size_t dim1, size_t dim2){
  int i,j;
  PyObject *list, *row;

  PY(list = PyList_New(dim1));

  for(i=0;i<dim1;i++){
    PY(row = PyList_New(dim2));
    for(j=0;j<dim2;j++){
      PY(PyList_SET_ITEM(row, j, PyFloat_FromDouble(mat[i][j])));
    }
    PY(PyList_SET_ITEM(list, i, row));
  }
  return list;
}


// This function initializes the graphics, and creates and initializes the world an the agent.
void init(int graphics, int verbose_flag)
{
	int brain = 0;

  AGENT_TYPE *current_agent;
  AGENT_TYPE *agent ;
  GEOMETRIC_SHAPE_TYPE *agentshape  ;
  ACOUSTIC_SHAPE_TYPE *sound ;
  int nsoundreceptors, nsoundbands ;
  float angle_locations0[31] = {
    -15.*2,-14.*2,-13.*2,-12.*2,-11.*2,
    -10.*2,-9.*2,-8.*2,-7.*2,-6.*2,
    -5.*2,-4.*2,-3.*2,-2.*2,-1.*2,0.*2,
    1.*2,2.*2,3.*2,4.*2,5.*2,
    6.*2,7.*2,8.*2,9.*2,10.*2,
    11.*2,12.*2,13.*2,14.*2,15
  } ;
  float directions0[31] = {
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
  } ;
  time_t now ;
  struct tm *date ;
  char timestamp[30] ;

  FILE * pyhandle;
  PyObject * main_module, *global_dict, *func_name, *arg, *result;

  if (graphics){
    /* Graphics window global variables */
    int wh = 600, ww = 800 ;
    float frustrum_theta=60.0, frustrum_znear=0.1, frustrum_zfar=1000.0 ;
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
  
  // create and initialize the world 
  //Flatworld = make_world( 0, 10, 610, 100.0, -100.0, 100.0, -100.0 ) ;
  Flatworld = make_world( 0, 1, 600, 100.0, -100.0, 100.0, -100.0, 0 ) ;
  read_object_spec_file( Flatworld, "WorldObjects.dat" ) ;

  agentshape = read_geometric_shape_file( "geoshapeAgent.dat",0 ) ;
  sound = read_acoustic_shape_file( "soundshapeAgent.dat" ) ;
  
  nsoundreceptors = sound->nfrequencies ; 
  nsoundbands = sound->nbands ;
    
  // Creat and initialize the Agent
  agent = make_agent( 1, 0.0, 0.0, 0.0, 0.5, 1.0 ) ; 
  add_physical_shape_to_agent( agent, agentshape ) ;
  add_sound_shape_to_agent( agent, sound ) ;
  add_visual_sensor_to_agent( agent, 31, 3, 0.0, angle_locations0, directions0 ) ;
  add_acoustic_sensor_to_agent( agent, nsoundreceptors, nsoundbands, 0.0, 90.0 ) ;
  add_acoustic_sensor_to_agent( agent, nsoundreceptors, nsoundbands, 0.0, -90.0 ) ;
  add_cargo_manifest_type_to_agent( agent, 0 ) ;
  add_soma_sensor_to_agent( agent, 1, 0.0, agentshape ) ;
  add_actuators_to_agent( agent, 0.0, 0.0, 0.0, 0.0 ) ;
  set_agent_head_angle( agent, 0.0 ) ;
  set_metabolic_burn_rate_agent(agent, 5.0e-4 ) ;
  add_agent_to_world( Flatworld, agent ) ; 
  current_agent = agent ;

  // Initialize the python singleton controller
  pyhandle = fopen(pyfile, "r");
  Py_Initialize();
  PyRun_SimpleFile(pyhandle, pyfile);
  PY(main_module = PyImport_AddModule("__main__"));
  PY(global_dict = PyModule_GetDict(main_module));
  PY(controller = PyDict_GetItemString(global_dict,"controller"));
  PY(run_brain = PyString_FromString("run_brain"));
  PY(learn = PyString_FromString("learn"));
  //PY(reset = PyString_FromString("reset"));
  //PY(process_stats = PyString_FromString("process_stats"));
  //PY(update_stats = PyString_FromString("update_stats"));

  PY(func_name = PyString_FromString("set_brain"));
  PY(arg = PyInt_FromLong(brain));
	
  PY(result = PyObject_CallMethodObjArgs(controller, func_name, arg, NULL));
  Py_DECREF(result);
  Py_DECREF(func_name);

  if(verbose_flag){
    PY(func_name = PyString_FromString("verbose"));
    PY(result = PyObject_CallMethodObjArgs(controller, func_name, NULL));
    Py_DECREF(result);
    Py_DECREF(func_name);
  }

  // Initialize the world and wall clock times.
  init_world_time( Flatworld ) ;
  now = time(NULL) ;
  date = localtime( &now ) ;
  strftime(timestamp, 30, "%y/%m/%d H: %H M: %M S: %S",date) ;
  printf("Start time: %s\n",timestamp) ;
}

void cleanup(){
  PyObject * result;
  PY(result = PyObject_CallMethodObjArgs(controller, process_stats, NULL));
  Py_XDECREF(result);
  Py_DECREF(run_brain);
  Py_DECREF(learn);
  Py_DECREF(reset);
  Py_DECREF(process_stats);
  Py_DECREF(update_stats);
  Py_Finalize();
}


int agents_controller( WORLD_TYPE *w )
{
  AGENT_TYPE *a ;
  int x, y, h, arg = 0;
  time_t now;
  struct tm *date;
  char timestamp[30];

  // To instrument eating, we need these variables
  int i, j, touched = 0, eaten = 0, collision_flag = 0;
  OBJECT_TYPE *o = NULL;

  float headth; //, bodyx, bodyy, bodyth;

  // Sensors and other input
  float charge, dcharge = 0;
  PyObject *eyevalues, *ear0values, *ear1values, *touchvalues;
  PyObject *input, *result;
  float dfb, drl, dth, dh;

  // Python dictionary output from neural controller
  PyObject *control;

  // Output from the brain to control robot actions
  int eat = 0; // Eat flag
  float ndfb, ndrl, ndth, ndh; // New actuator values

  a = w->agents[0] ; // get agent pointer
    
  // test if agent is alive. if so, process sensors and actuators.
  // if not, report death and exit
  if( a->instate->metabolic_charge>0.0 ) {

    // STEP 1: Move
    ////////////////////////////////////

    // move the agents body
    move_body_agent( a );
    move_head_agent( a );

    // STEP 2: Read sensors
    /////////////////////////////////////////////////
    charge = read_agent_metabolic_charge( a );
    collision_flag = read_soma_sensor(w, a);
    touchvalues = PyMatrix(extract_soma_receptor_values_pointer( a ),
      a->instate->skin->nreceptors, a->instate->skin->nbands);
    read_actuators_agent( a, &dfb, &drl, &dth, &dh );
    //read_agent_body_position( a, &bodyx, &bodyy, &bodyth );
    read_agent_head_angle( a, &headth );
    read_visual_sensor( w, a) ;
    eyevalues = PyMatrix(extract_visual_receptor_values_pointer( a, 0 ),
      a->instate->eyes[0]->nreceptors, a->instate->eyes[0]->nbands);
    read_acoustic_sensor( w, a) ;
    ear0values = PyMatrix(extract_sound_receptor_values_pointer( a, 0 ),
      a->instate->ears[0]->nreceptors, a->instate->ears[0]->nbands);
    ear1values = PyMatrix(extract_sound_receptor_values_pointer( a, 1 ),
      a->instate->ears[1]->nreceptors, a->instate->ears[1]->nbands);

    // Call the controller with [charge, touchvalues]
    PY(input = PyList_New(7));
    PY(PyList_SET_ITEM(input, arg++, PyFloat_FromDouble(charge)));
    PY(PyList_SET_ITEM(input, arg++, touchvalues));
    PY(PyList_SET_ITEM(input, arg++, eyevalues));
    PY(PyList_SET_ITEM(input, arg++, ear0values));
    PY(PyList_SET_ITEM(input, arg++, ear1values));
    PY(PyList_SET_ITEM(input, arg++, Py_BuildValue("(ffff)", dfb, drl, dth, dh)));
    PY(PyList_SET_ITEM(input, arg++, PyFloat_FromDouble(headth)));
    PY(control = PyObject_CallMethodObjArgs(controller, run_brain, input, NULL));
    Py_DECREF(input);
    PY(PyArg_ParseTuple(control, "iffff", &eat, &ndfb, &ndrl, &ndth, &ndh));
    Py_DECREF(control);

    // STEP 3: Take actions, possibly learn
    // Eat if we can and the controller said its okay.
    if( collision_flag>0 ) {
      for( j=0 ; j<a->instate->skin->nreceptors ; j++ ) {
        i = a->instate->skin->touched_objects[j] ;
        if(i > 0 )  {
          o = w->objects[i-1] ;
          touched = o->type;
          if( o->inworld_flag!=0) {
            dcharge = agent_eat_object_with_flag( w, a, o, eat );
            if(eat){
              //Debugging code
              /*
              if(eat && dcharge < 0)
                fprintf(stderr, "Ate poision!\n");
              */
              eaten = touched;
            }
            //a->instate->itemp[0]++; 
            //printf("Object of type: %d eaten. New charge: %f total eaten: %d\n",
            //  obj_type, a->instate->metabolic_charge, a->instate->itemp[0]);
          }
        }
      }
    }
    // Don't count an object twice if we are sitting on it.
    if(o){
      if(last_object == o->index)
        touched = 0;
      last_object = o->index;
    }

    // Let the brain learn if it can.
    PY(input = PyFloat_FromDouble(dcharge));
    PY(control = PyObject_CallMethodObjArgs(controller, learn, input, NULL));
    Py_DECREF(input);
    Py_DECREF(control);

    // Setup the next movement step
    set_actuators_agent( a, ndfb, ndrl, ndth, ndh ) ;
    //set_agent_body_angle( a, bodyth+dbodyth ) ;
    //set_agent_head_angle( a, headth ) ;
    //scan_head_agent( a, headthmax, headthmin, headperiod ) ;

    // STEP 4: Record statistics about this iteration.
    PY(input = PyList_New(5));
    arg = 0;
    PY(PyList_SET_ITEM(input, arg++, PyFloat_FromDouble(charge)));
    PY(PyList_SET_ITEM(input, arg++, PyFloat_FromDouble(dcharge)));
    PY(PyList_SET_ITEM(input, arg++, Py_BuildValue("(ffff)", dfb, drl, dth, dh)));
    PY(PyList_SET_ITEM(input, arg++, PyInt_FromLong(touched)));
    PY(PyList_SET_ITEM(input, arg++, PyInt_FromLong(eaten)));
    //PY(control = PyObject_CallMethodObjArgs(controller, update_stats, input, NULL));
    Py_DECREF(input);
    //Py_DECREF(control);

    // decrement metabolic charge by basil metabolism rate.  DO NOT REMOVE THIS CALL 
    basal_metabolism_agent( a ) ;
    
    // increment world time clock 
    increment_world_clock( w ) ;

    return 1;

  } // end agent alive condition 
  else
  {
    // Example of agent is dead condition 
    printf("agent_controller- Agent has died, eating %d objects.\n",a->instate->itemp[0]) ;
    //print_world_time( Flatworld) ;
    now = time(NULL) ;
    date = localtime( &now ) ;
    strftime(timestamp, 30, "%y/%m/%d H: %H M: %M S: %S",date) ;
    printf("Death time: %s\n",timestamp) ;
    last_object = 0;
    
    // Example as to how to restore the world and agent after it dies. 
    // restore all of the objects h=back into the world 
    restore_objects_to_world( Flatworld );
    // recharge the agent's battery to full 
    reset_agent_charge( a );
    // zero the number of object's eaten accumulator 
    a->instate->itemp[0] = 0;
    // zero the Flatworld clock
    init_world_time( Flatworld );
    // pick random starting position and heading
    x = distributions_uniform( Flatworld->xmin, Flatworld->xmax ); 
    y = distributions_uniform( Flatworld->ymin, Flatworld->ymax );
    h = distributions_uniform( -179.0, 179.0);
    // set new position and heading of agent
    set_agent_body_position( a, x, y, h );

    //PY(result = PyObject_CallMethodObjArgs(controller, reset, NULL));
    Py_XDECREF(result);

    return 0;
    
  } // end agent dead condition 

}


