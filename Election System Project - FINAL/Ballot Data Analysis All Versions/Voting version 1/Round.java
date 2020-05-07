import java.util.ArrayList;

public class Round {
	static int roundNumber = 1;
	
	int numOfWinners;
	int majority;
	double votesLost;
	double totalVotes;
	Boolean done;
	Boolean candidateAdded;
	ArrayList<Candidate> winningCandidates;
	
	ArrayList<Vote> master;
	ArrayList<Candidate> candidates;
	ArrayList<Vote> nextRoundList;
	
	double[] pastRoundVoteCounts;
	double[] currentRoundVoteCounts;
	
	static ArrayList<ArrayList<String>> allData = new ArrayList<ArrayList<String>>();
	ArrayList<String> roundData;
	
	public Round(ArrayList<Vote> master, ArrayList<Candidate> candidates, 
			ArrayList<Candidate> winningCandidates, int numOfWinners, double[] pastRoundVoteCounts) {
		
		this.master = master;
		this.nextRoundList = master;
		this.numOfWinners = numOfWinners;
		this.candidates = candidates;
		this.winningCandidates = winningCandidates;
		this.pastRoundVoteCounts = pastRoundVoteCounts;
		currentRoundVoteCounts = new double[candidates.size()];
		totalVotes = (double)master.size();
		
		votesLost = 0;
		majority = master.size() / (numOfWinners + 1) + 1;
		
		roundData = new ArrayList<String>();
		
		sortMaster();
		printResults();
		checkForWinner();
		
		allData.add(roundData);
		
		if(roundNumber > 20) {
			done = true;
		}
		
		for(String string: roundData) {
			System.out.println(string);
		}
	}
	
	
	
	public void sortMaster() {
		for(Vote vote: master) {
			sortVote(vote.cloneVote());
		}
	}
	
	public void sortVote(Vote vote) {
		String validVote = vote.get(0);
		
		for(Candidate candidate: candidates) {
			if(validVote.equalsIgnoreCase(candidate.getName())) {
				candidate.addVote(vote);
			}
		}
	}
	
	public void printResults() {
		String a = "Winners so far: ";
		System.out.print(a);
		
		String b = "";
		if(winningCandidates.size()>0) {
			roundData.add(a);
			for(Candidate candidate: winningCandidates) {
				b = candidate.name + " ";
				System.out.print(b);
				roundData.add(b);
			}
			
		} else {
			a += "none";
			roundData.add(a);
		}
		
		System.out.println();
		roundData.add("");
		
		for(Candidate candidate: candidates) {
			if(winningCandidates.contains(candidate)){
				candidate.setVoteScore(majority);
			}
		}
		getTotalVotes();
		
		String c = "Ballots Exhausted: " + round(votesLost);
		String d = "Round " + roundNumber + ": " + round(totalVotes);
		System.out.println(c);
		System.out.println(d);
		roundData.add(c);
		roundData.add(d);
		
		int i=0;
		double voteCount;
		for(Candidate candidate: candidates) {
			String e;
			if(winningCandidates.contains(candidate)) {
				e = candidate.getName() + ": " + round(candidate.voteScore);
				currentRoundVoteCounts[i] = round(candidate.voteScore);
				voteCount = round(currentRoundVoteCounts[i] - pastRoundVoteCounts[i]);
				if(voteCount > 0) {
					e += " (+" + voteCount + ")";
				} else {
					e += " (" + voteCount + ")";
				}
			} else {
				e = candidate.getName() + ": " + round(candidate.getVoteScore());
				currentRoundVoteCounts[i] = round(candidate.voteScore);
				voteCount = round(currentRoundVoteCounts[i] - pastRoundVoteCounts[i]);
				if(voteCount > 0) {
					e += " (+" + voteCount + ")";
				} else {
					e += " (" + voteCount + ")";
				}
			}
			i++;
			System.out.println(e);
			roundData.add(e);
			
//			for(Vote vote: candidate.getVotes()) {
//				System.out.println(vote + " " + round(vote.getWeight()));
//			}
		}
		
		String f = "Quota: " + round(majority);
		System.out.println(f);
		roundData.add(f);
	}
	
	public void checkForWinner() {
		done = false;
		candidateAdded = false;
		
		int index = findMaximum(candidates);
		Candidate winner = candidates.get(index);
			
		if(winner.getVoteScore() >= majority) {
			candidateAdded = true;
			winningCandidates.add(winner);
			
			if(winningCandidates.size()==numOfWinners) {
				String g = "Winner this round: " + winner.name;
				System.out.println(g);
				System.out.println();
				roundData.add(g);
				roundData.add("");
				for(Candidate winningCandidate: winningCandidates) {
					String h = winningCandidate.getName() + " has won";
					System.out.println(h);
					roundData.add(h);
				}
			} else {
				redistributeWinner(winner);
				System.out.println();
				System.out.println();
				roundData.add("");
				roundData.add("");
				roundNumber++;
				new Round(nextRoundList, this.candidates, this.winningCandidates, this.numOfWinners, this.currentRoundVoteCounts);
			}
		} else {
			redistributeLoser();
//			System.out.println(nextRoundList);
			System.out.println();
			System.out.println();
			roundData.add("");
			roundData.add("");
			roundNumber++;
			new Round(nextRoundList, this.candidates, this.winningCandidates, this.numOfWinners, this.currentRoundVoteCounts);
		}
	}
	
	
	
	public void getTotalVotes() {
		totalVotes = (double)0;
		for(Candidate candidate: candidates) {
			if(candidate.valid) {
				totalVotes += candidate.getVoteScore();
			} else if(winningCandidates.contains(candidate)){
				totalVotes += candidate.voteScore;
			} else {
				votesLost += candidate.getVoteScore();
				candidate.clearVotes();
			}
		}
	}
	
	public double round(double n) {
		n *= 1000;
		n = Math.round(n);
		n /= 1000;
		
		return n;
	}

	
	
	public void redistributeWinner(Candidate candidate) {
		double scoreToRedistribute = candidate.getVoteScore() - majority;
		String i = "Winner this round: " + candidate.name;
		String j = "Redistribute: " + round(scoreToRedistribute);
		System.out.println(i);
		System.out.println(j);
		roundData.add(i);
		roundData.add(j);

		candidate.setInvalid();
		for(Vote vote: candidate.getVotes() ) {
			vote.nextValidVote(candidates);
		}
		candidate.setWeights(scoreToRedistribute);
		
		createNextRoundList();
		
		for(Candidate cand: candidates) {
			cand.getVotes().clear();
		}
	}
	
	public void redistributeLoser() {
		int index = findMinimum(candidates);
		Candidate loser = candidates.get(index);
//		System.out.println(loser.getName());
		
		loser.setInvalid();
		
		createNextRoundList();
		
		for(Candidate candidate: candidates) {
			candidate.getVotes().clear();
		}
		
		String k = "Eliminated: " + loser.name;
		System.out.println(k);
		roundData.add(k);
	}
	
	public int findMaximum(ArrayList<Candidate> candidates) {
		double maximumVotes = 0; 
		int maximumIndex = 0;
		for(int i=0; i<candidates.size(); i++) {
			Candidate candidate = candidates.get(i);
			if(candidate.valid) {
				maximumVotes = candidate.getVoteScore();
				maximumIndex = i;
				break;
			}
		}
		
//		System.out.println(maximumIndex + " " + maximumVotes);
		
		for(int i=0; i<candidates.size(); i++) {
			if(candidates.get(i).getVoteScore() > maximumVotes && candidates.get(i).valid) {
				maximumVotes = candidates.get(i).getVoteScore();
				maximumIndex = i;
			} 
		}
		
		return maximumIndex;
	}
	
	public int findMinimum(ArrayList<Candidate> candidates) {
		double minimumVotes = 0; 
		int minimumIndex = 0;
		for(int i=0; i<candidates.size(); i++) {
			Candidate candidate = candidates.get(i);
			if(candidate.valid) {
				minimumVotes = candidate.getVoteScore();
				minimumIndex = i;
				break;
			}
		}
		
//		System.out.println(minimumIndex + " " + minimumVotes);
		
		for(int i=0; i<candidates.size(); i++) {
			if(candidates.get(i).getVoteScore() < minimumVotes && candidates.get(i).valid) {
				minimumVotes = candidates.get(i).getVoteScore();
				minimumIndex = i;
			} 
		}
		
		return minimumIndex;
	}
	
	public void createNextRoundList() {
		nextRoundList.clear();
		for(Candidate candidate: candidates) {
			for(Vote vote: candidate.getVotes()) {
				vote.nextValidVote(candidates);
				nextRoundList.add(vote);
			}
		}
	}
	
	public ArrayList<ArrayList<String>> getAllData() {
		return allData;
	}

}
