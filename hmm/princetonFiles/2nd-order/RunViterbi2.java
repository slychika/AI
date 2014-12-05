import java.util.*;
import java.lang.*;
import java.text.*;
import java.io.*;

/**
 * This is a simple class for running your code if you decide to do
 * the optional part of the assignment using second-order Markov
 * models.  You might want to extend or modify this class, or write
 * your own.  (But your code should still work properly when run with
 * this code.)
 **/
public class RunViterbi2 {

    /**
     * A simple main that loads the dataset contained in the file
     * named in the first command-line argument, builds a second-order
     * HMM, prints it out and finds and prints the most likely state
     * sequence for each of the output sequences.
     **/
    public static void main(String[] argv)
	throws FileNotFoundException, IOException {

	// get file name
	String file_name = "";
	try {
	    file_name = argv[0];
	} catch (Exception e) {
	    System.err.println("Arguments: <file_name>");
	    return;
	}

	// get data from given file
	DataSet ds = new DataSet(file_name);

	// build HMM from given data
	Hmm2 h = new Hmm2(ds.numStates, ds.numOutputs,
			  ds.trainState, ds.trainOutput);

	// create Viterbi2 object for computing most likely sequences
	Viterbi2 v = new Viterbi2(h);

	System.out.println();

	// compute and print most likely sequence for each test sequence
	for (int i = 0; i < ds.testOutput.length; i++) {
	    int[] state = v.mostLikelySequence(ds.testOutput[i]);
	    int errors = 0;

	    System.out.println();
	    System.out.println("sequence "+i+":");
	    for (int j = 0; j < state.length; j++) {
		System.out.println(ds.stateName[ds.testState[i][j]]+"\t"+
				   ds.stateName[state[j]] +"\t"+
				   ds.outputName[ds.testOutput[i][j]]);
		if (state[j] != ds.testState[i][j])
		    errors++;
	    }
	    System.out.println("errors: " + errors + " / " + state.length +
			       " = " + ((double) errors)/state.length);
	}



    }

    // private print formatting stuff
    private static NumberFormat nf = new DecimalFormat("#.000");

    private static String name(String s) {
	return (s + "    ").substring(0, 4);
    }

    private static String num(double d) {
	return nf.format(d);
    }

}
	    
