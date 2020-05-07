import java.util.ArrayList;
import java.util.Scanner;
import java.util.StringTokenizer;

import java.io.*;

public class TestData {
	public static Scanner scanner;
	
	File file;
	ArrayList<Vote> master = new ArrayList<Vote>();
	ArrayList<ArrayList<String>> rawNames = new ArrayList<ArrayList<String>>();
	
	ArrayList<Candidate> candidates = new ArrayList<Candidate>();
	
	public TestData(String path) throws FileNotFoundException{
		file = new File(path);
		scanner = new Scanner(file);
		
		initialCandidateData();
		System.out.println();
		initialBallotData();
	}
	public TestData(File file) throws FileNotFoundException{
		this.file = file;
		scanner = new Scanner(this.file);
		
		initialCandidateData();
		System.out.println();
		initialBallotData();
	}

	public void initialBallotData() {
		while(scanner.hasNextLine()){
			String line = scanner.nextLine();
			StringTokenizer st = new StringTokenizer(line);
			ArrayList<String> name = new ArrayList<String>();
		  

			while (st.hasMoreTokens()) {
		    	name.add(st.nextToken());
		    }
		   rawNames.add(name);
		} 
		
		for(ArrayList<String> names: rawNames) {
			if(names.size() > 0) {
				Vote vote = new Vote();
				for(int i=0; i<names.size(); i+=2) {
					vote.add(names.get(i) + " " + names.get(i+1));
				}
				master.add(vote);
			}
		}
		
//		System.out.println(master.size());
//		for(Vote vote: master) {
//			System.out.println(vote);
//		} 
	}
	
	public void initialCandidateData() {
		String line = scanner.nextLine();
		StringTokenizer st = new StringTokenizer(line);
		
		ArrayList<String> candidateNames = new ArrayList<String>();
		  

		while (st.hasMoreTokens()) {
			candidateNames.add(st.nextToken());
	    }
		
		for(int i=0; i<candidateNames.size(); i+=2) {
			String candidateName = candidateNames.get(i) + " " + candidateNames.get(i+1);
			candidates.add(new Candidate(candidateName));
		}
		
//		for(Candidate candidate: candidates) {
//			System.out.println(candidate.name);
//		}
	}
	
	public ArrayList<Vote> getMaster() {
		return master;
	}
	
	public ArrayList<Candidate> getCandidates() {
		return candidates;
	}
}
