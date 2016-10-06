/*--------------------------------------------------------------------------*/
/*---------------------------- File Main.C ---------------------------------*/
/*--------------------------------------------------------------------------*/
/** @file
 * 
 * Sample Main file to illustrate the use of any solver deriving from
 * MCFClass. By changing just *two lines of code* and little more (see comment
 * PECULIARITY, if exists) the file works with any derived solver. 
 *
 * An instance of a Min Cost Flow problem in DIMACS standard format is read
 * from file and solved. In addition, the same problem can be written on a
 * file in MPS format. 
 *
 * \version 4.00
 *
 * \date 30 - 12 - 2009
 *
 * \author Alessandro Bertolini \n
 *         Operations Research Group \n
 *         Dipartimento di Informatica \n
 *         Universita' di Pisa \n
 *
 * \author Antonio Frangioni \n
 *         Operations Research Group \n
 *         Dipartimento di Informatica \n
 *         Universita' di Pisa \n

/*--------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------*/

/*--------------------------------------------------------------------------*/
/*------------------------------ INCLUDES ----------------------------------*/
/*--------------------------------------------------------------------------*/

#include <fstream>
#include <sstream>
//Johannes Sommer - for linux
#include <limits.h>

#include "SPTree.h"
#define MCFSOLVER SPTree

// just change the two lines above and any MCFClass solver can be used (with
// the exception of PECULIARITY)

/*--------------------------------------------------------------------------*/
/*------------------------------- MACROS -----------------------------------*/
/*--------------------------------------------------------------------------*/

#define PRINT_RESULTS 0

/* If PRINT_RESULTS != 0, the optimal flows and potentials are printed
   after that the problem is successfully solved to optimality (so, watch
   out if your instance is very large). */

/*--------------------------------------------------------------------------*/
/*-------------------------------- USING -----------------------------------*/
/*--------------------------------------------------------------------------*/

#if( OPT_USE_NAMESPACES )
 using namespace MCFClass_di_unipi_it;
#endif

/*--------------------------------------------------------------------------*/
/*------------------------------- FUNCTIONS --------------------------------*/
/*--------------------------------------------------------------------------*/

template<class T>
inline T ABS( const T x )
{
 return( x >= T( 0 ) ? x : -x );
 }

/*--------------------------------------------------------------------------*/
// This function reads the first part of a string (before white spaces) and
// copy T value in the variable sthg (of T type)


template<class T>
static inline void str2val( const char* const str , T &sthg )
{
 istringstream( str ) >> sthg;
 }

/*--------------------------------------------------------------------------*/
// This function skips comment line in a input stream, where comment line is 
// marked by an initial '#' character

void SkipComments( ifstream &iParam , string &buf )
{
 do {
  iParam >> ws;
  getline( iParam , buf );
 }
 while( buf[ 0 ] == '#' );
}

/*--------------------------------------------------------------------------*/
// This function tries to read the parameter file; if it finds it, the
// corresponding parameters are set in the MCFClass object

void SetParam( MCFClass *mcf )
{
 ifstream iParam( "config.txt" ); 
 if( ! iParam.is_open() )
  return;

 string buf;
 int num;
 SkipComments( iParam , buf );
 str2val( buf.c_str(), num );        // get number of int parameters

 for( int i = 0 ; i < num ; i++ ) {  // read all int parameters
  int param , val;
  
  SkipComments( iParam , buf );
  str2val( buf.c_str(), param );     // parameter name
  
  SkipComments( iParam , buf );
  str2val( buf.c_str(), val );       // parameter value

  mcf->SetPar( param , val );

  }  // end( for( i ) )

 SkipComments( iParam , buf );
 str2val( buf.c_str() , num );       // get number of double parameters

 for( int i = 0 ; i < num ; i++ ) {  // read all double parameters
  int param;
  double val;
  SkipComments( iParam , buf );
  str2val( buf.c_str(), param );     // parameter name
  
  SkipComments( iParam , buf );
  str2val( buf.c_str() , val );      // parameter value
  
  mcf->SetPar( param , val );

  }  // end( for( i ) )
 }  // end( SetParam )

unsigned int BuildODPath(unsigned int origin, unsigned int dest, 
  SPTree *mcf, bool printOutput )
{
// Build Path from 1 Origin to 1 Dest
   MCFClass::cIndex_Set arcPre = mcf->ArcPredecessors();
   MCFClass::cIndex_Set pre = mcf->Predecessors();
   int counter = 0;
   unsigned int lastStartNode = Inf<unsigned int>();
   unsigned int lastEndNode = Inf<unsigned int>();
   bool setLastNodes = true;
   bool endNodeVisited = false;
   for (int i = mcf->MCFnmax();  i > 0 ; i--)
   {
     if (arcPre[i] < Inf<unsigned int>())
     {
       unsigned int arcIndex = arcPre[i];
       unsigned int startNode = pre[i];//mcf->MCFSNde(arcIndex);  
       unsigned int endNode = i;//mcf->MCFENde(arcIndex);
       //cout << "  EndNode " << endNode << " LastEndNode " << lastEndNode <<  " StartNode " << startNode << " LastStartNode " << lastStartNode << endl;
       // check for the first arc with the dest as endNode
       if (endNode == dest)
	endNodeVisited = true;

       if (endNodeVisited)
       {
        if (lastStartNode < Inf<unsigned int>() && 
		lastEndNode < Inf<unsigned int>() )
	{
	  if (endNode == lastStartNode)
	  {
	    if (printOutput)
		 cout << "  Solution Arc: #" << arcPre[i] << " (" << endNode << "," << startNode << ")" << endl;
       
	    counter = counter +1;
	    setLastNodes = true;
	   }
	 // don't set lastStartNode if endNode != lastStartNode
	  else
	   setLastNodes = false;
           if (startNode == origin)
	    break;
	}
	//first cout
       else if (lastStartNode == Inf<unsigned int>() && 
		lastEndNode == Inf<unsigned int>())
       {
	    if (printOutput)
	     cout << "  Solution Arc: #" << arcPre[i] << " (" << endNode << "," << startNode << ")" << endl;

	    counter = counter +1;
       }
	if (setLastNodes)
	{ 
          lastEndNode = endNode;
          lastStartNode = startNode;
        }
       }
     }
   }
 return counter;
}

unsigned int BuildSPTree(unsigned int origin, SPTree *mcf, bool printOutput )
{
// Build Shortest Path Tree from 1 Origin to all Dests
   MCFClass::cIndex_Set arcPre = mcf->ArcPredecessors();
   MCFClass::cIndex_Set pre = mcf->Predecessors();
   int counter = 0;
   unsigned int lastStartNode = Inf<unsigned int>();
   unsigned int lastEndNode = Inf<unsigned int>();
   bool setLastNodes = true;
   bool startNodeVisited = false;
   for (int i = 1;  i <= mcf->MCFnmax() ; i++)
   {
     if (arcPre[i] < Inf<unsigned int>())
     {
       unsigned int arcIndex = arcPre[i];
       unsigned int startNode = pre[i];//mcf->MCFSNde(arcIndex);  
       unsigned int endNode = i;//mcf->MCFENde(arcIndex);
	   if (printOutput)
	    cout << "  Solution Arc: #" << arcPre[i] << " (" << startNode << "," << endNode << ")" << endl;
       
	   counter = counter +1;
     }
   }
 return counter;
}

/*--------------------------------------------------------------------------*/
/*--------------------------------- MAIN -----------------------------------*/
/*--------------------------------------------------------------------------*/

int main( int argc , char **argv )
{
 // reading command line parameters - - - - - - - - - - - - - - - - - - - - -

 if( argc < 2 ) {
  cerr << "Usage: MCFSolve <input file> [<directed:(true|false)>] [<allDest>] [<output MPS file>]" << endl;
  return( -1 );
  }

 // opening input stream- - - - - - - - - - - - - - - - - - - - - - - - - - -

 ifstream iFile( argv[ 1 ] );
 if( ! iFile ) {
  cerr << "ERROR: opening input file " << argv[ 1 ] << endl;
  return( -1 );
  }

  //JS MCFClass --> SPTree
  // directed or undirected
 bool isDirected = true;
 bool allDest = false;
 if (argc > 2)
 {
  std::string directed = argv[2];
  if ( directed == "true")
   isDirected = true;
  else if (directed == "false")
   isDirected = false;
  else if (directed == "allDest")
   allDest = true;
 }
 else
   isDirected = true;
 if (argc > 3)
 {
  std::string allDestStr = argv[3];
  if (allDestStr == "allDest")
   allDest = true;
 }

 std::string outFileName = "";
 if (argc > 4)
 { 
   outFileName = argv[4];
 }
 
 cout << "Arguments: " << "directed: "<< isDirected << " allDest: " << allDest << " outFile: " << outFileName  << endl;

 try {
  // construct the solver - - - - - - - - - - - - - - - - - - - - - - - - - -

  SPTree *mcf = new MCFSOLVER(0,0,isDirected);

  mcf->SetMCFTime();  // do timing

  // load the network - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  mcf->LoadDMX( iFile );

  // set "reasonable" values for the epsilons, if any - - - - - - - - - - - -

  MCFClass::FNumber eF = 1;
  for( register MCFClass::Index i = mcf->MCFm() ; i-- ; )
   eF = max( eF , ABS( mcf->MCFUCap( i ) ) );

  for( register MCFClass::Index i = mcf->MCFn() ; i-- ; )
   eF = max( eF , ABS( mcf->MCFDfct( i ) ) );   

  MCFClass::CNumber eC = 1;
  for( register MCFClass::Index i = mcf->MCFm() ; i-- ; )
   eC = max( eC , ABS( mcf->MCFCost( i ) ) );

  mcf->SetPar( MCFSOLVER::kEpsFlw, (double) numeric_limits<MCFClass::FNumber>::epsilon() * eF *
		  mcf->MCFm() * 10);  // the epsilon for flows

  mcf->SetPar( MCFSOLVER::kEpsCst, (double) numeric_limits<MCFClass::CNumber>::epsilon() * eC *
		  mcf->MCFm() * 10);  // the epsilon for costs

  // set other parameters from configuration file (if any)- - - - - - - - - -

   SetParam( mcf );
   
  // solver call- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   //MCFClass::cIndex_Set set = mcf->Dests();
  // for (int i = 0;  i < mcf->DestN(); i++)
  // {
		//cout << "Dests: " << set[i] << endl;
  // }
   //cout << "Count dest: " << mcf->DestN() << endl;

   cout << "Algorithm: " << SPT_ALGRTM << endl;
   cout << " Label setting: " << LABEL_SETTING << endl;
   cout << "Directed Graph: " << isDirected << endl;

   MCFClass::Index OrigOrigin;
   MCFClass::Index dest;

   int originCounter = 0;
   for (int i = 0; i < mcf->MCFn(); i++)
   {
   	if (mcf->MCFDfct(i) < 0)
	{
	  cout << "Deficit of Node "<< i+1 << " is:" << mcf->MCFDfct(i) << endl;
	  OrigOrigin = i+1;
	  originCounter = originCounter + 1;
	}
      	if (mcf->MCFDfct(i) > 0)
	  dest = i+1;
   }

   if (allDest)
   {
    dest = Inf<MCFClass::cIndex>();
   }

   //for (int i = 1; i <= 1000; i++)
   //{
       	   MCFClass::Index origin = OrigOrigin; //i;
	   mcf->SetOrigin(origin);
	   // method is sensitive to type: either pass Inf<MCFClass::cIndex>>() or
           // don't call it
	   mcf->SetDest(dest);
	   cout << " Origin: " << origin << endl;
	   if (!allDest)
	    cout << " Destination: " << dest << endl;
	   else
	    cout << " Destination: all nodes" << endl;

	   //cout << "Inf: " << UINT_MAX << endl;
	   //mcf->SolveMCF();
	   mcf->ShortestPathTree();
	   for (int i = 1; i <= mcf->MCFn(); i++)
	   {
		//if (mcf->Reached(i))
		 //cout << "Node " << i << " reached: " << mcf->Reached(i) << endl;
	   }

	   if (dest != Inf<MCFClass::cIndex>() && !mcf->Reached(dest))
	   {
		throw MCFException("Destination not reachable!");
	   }

	   //double tu , ts;
	   //mcf->TimeMCF( tu , ts );
	   cout << "Shortest Path Tree - rooted at: " << origin << endl;
	   MCFClass::cIndex_Set pre = mcf->Predecessors();
	   for (int i = 1;  i <= mcf->MCFnmax(); i++)
	   {
	       //if (pre[i] > 0)
               //if(mcf->Reached(pre[i]))
		//cout << "Pre Vector (" << pre[i] << "," << i  << ")"<< endl;
	   }
	   
           unsigned int counter;
           if (allDest)
            counter = BuildSPTree(origin, mcf, true);
           else
            counter = BuildODPath(origin, dest, mcf, true);

           
	   cout << "  Node count: #" << mcf->MCFn() << endl;
	   cout << "  Arc count: #" << mcf->MCFm() << endl;
	   cout << "  Arc count of SPT: #" << counter << endl;
   //}

   //mcf->SolveMCF();

  // output results - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  switch( mcf->MCFGetStatus() ) {
   case( MCFClass::kOK ):
    cout << "Optimal Objective Function value = " << mcf->MCFGetFO() << endl;

    double tu , ts;
    mcf->TimeMCF( tu , ts );
    cout << "Solution time (s): user " << tu << ", system " << ts << endl;
    #if( PRINT_RESULTS )
    {
     if( ( numeric_limits<MCFClass::CNumber>::is_integer == 0 ) ||
	 ( numeric_limits<MCFClass::FNumber>::is_integer == 0 ) ) {
      cout.setf( ios::scientific, ios::floatfield );
      cout.precision( 12 );
      }

     MCFClass::FRow x = new MCFClass::FNumber[ mcf->MCFm() ];
     mcf->MCFGetX( x );
     for( MCFClass::Index i = 0 ; i < mcf->MCFm() ; i++ )
      cout << "x[" << i << "] = "  << x[ i ] << endl;

     delete[] x;
     MCFClass::CRow pi = new MCFClass::CNumber[ mcf->MCFn() ];
     mcf->MCFGetPi( pi );
     for( MCFClass::Index i = 0 ; i < mcf->MCFn() ; i++ )
      cout << "pi[" << i << "] = "  << pi[ i ] << endl;
     delete[] pi;
     }
    #endif

    // check solution
    //mcf->CheckPSol();
    //mcf->CheckDSol();

    break;
   case( MCFClass::kUnfeasible ):
    cout << "MCF problem unfeasible." << endl;
    break;
   case( MCFClass::kUnbounded ):
    cout << "MCF problem unbounded." << endl;
    break;
   default:
    cout << "Error in the MCF solver." << endl;
   }

  // output the problem in MPS format - - - - - - - - - - - - - - - - - - - -

  if( argc > 4 ) {
   ofstream oFile( argv[ 4 ] );
   mcf->WriteMCF( oFile , MCFClass::kMPS );
   }

  // destroy the object - - - - - - - - - - - - - - - - - - - - - - - - - - -

  delete( mcf );
  }
 // manage exceptions - - - - - - - - - - - - - - - - - - - - - - - - - - - -
 catch( exception &e ) {
  cerr << e.what() << endl;
  return( 1 );
  }
 catch(...) {
  cerr << "Error: unknown exception thrown" << endl;
  return( 1 );
  }

 // terminate - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

 return( 0 );

 }  // end( main )

/*--------------------------------------------------------------------------*/
/*------------------------- End File Main.C --------------------------------*/
/*--------------------------------------------------------------------------*/
