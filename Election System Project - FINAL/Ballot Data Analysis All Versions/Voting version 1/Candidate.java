import java.util.ArrayList;

public class Candidate {

	String name;
	ArrayList<Vote> votes;
	double voteScore;
	boolean valid;
	
	public Candidate(String name) {
		this.name = name;;
		votes = new ArrayList<Vote>();
		voteScore = 0;
		valid = true;
	}
	
	
	
	public String getName() {
		return name;
	}
	
	public ArrayList<Vote> getVotes() {
		return votes;
	}
	
	public double getVoteScore() {
		sumVotes();
		return voteScore;
	}
	
	
	public void setVoteScore(double num) {
		voteScore = num;
	}
	
	public void setInvalid() {
		valid = false;
	}
	
	public void addVote(Vote vote) {
		votes.add(vote);
	}
	
	public void sumVotes() {
		voteScore = 0;
		for(Vote vote: votes) {
			voteScore += vote.getWeight();
		}
	}
	
	public void clearVotes() {
		votes.clear();
	}
	
	public void setWeights(double scoreToRedistribute) {
		double weight = scoreToRedistribute / (double) votes.size();
		
		for(Vote vote: votes) {
			vote.setWeight(weight);
		}
	}
}


