import java.util.ArrayList;
import java.util.Scanner;
import java.util.StringTokenizer;

import java.io.*;

public class TestData {
	public static Scanner scanner;
	
	File file;
	ArrayList<Vote> master = new ArrayList<Vote>();
	ArrayList<ArrayList<String>> rawNames = new ArrayList<ArrayList<String>>();
	ArrayList<ArrayList<String>> rawBallotData = new ArrayList<ArrayList<String>>();
	
	ArrayList<Candidate> candidates = new ArrayList<Candidate>();
	
	public TestData(String path, ArrayList<String> candidateNames) throws FileNotFoundException{
		file = new File(path);
		scanner = new Scanner(file);
		
		initialCandidateData(candidateNames);
		System.out.println();
		initialBallotData();
	}
	public TestData(File file, ArrayList<String> candidateNames) throws FileNotFoundException{
		this.file = file;
		scanner = new Scanner(this.file);
		
		initialCandidateData(candidateNames);
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
				ArrayList<String> vote2 = new ArrayList<String>();
				for(int i=0; i<names.size(); i+=2) {
					vote.add(names.get(i) + " " + names.get(i+1));
					vote2.add(names.get(i) + " " + names.get(i+1));
				}
				master.add(vote);
				rawBallotData.add(vote2);
			}
		}
		
//		System.out.println(master.size());
//		for(Vote vote: master) {
//			System.out.println(vote);
//		} 
	}
	
	public void initialCandidateData(ArrayList<String> candidateNames) {
		for(String candidateName: candidateNames) {
			candidates.add(new Candidate(candidateName));
		}
		
//		for(Candidate candidate: candidates) {
//			System.out.println(candidate.name);
//		}
	}
	
	public ArrayList<Vote> getMaster() {
		return master;
	}
	
	public ArrayList<ArrayList<String>> getRawBallotData() {
		return rawBallotData;
	}
	
	public ArrayList<Candidate> getCandidates() {
		return candidates;
	}
}
