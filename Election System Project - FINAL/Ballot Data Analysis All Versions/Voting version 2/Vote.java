import java.util.ArrayList;

public class Vote extends ArrayList<String> {
	private static final long serialVersionUID = -9108618238849920465L;
	
	public double weight;
	
	public Vote() {
		weight = 1;
	}
	
	public Vote cloneVote() {
		Vote clone = new Vote();
		clone.setWeight(this.weight);
		for(String string: this) {
			clone.add(string);
		}
		
		return clone;
	}
	
	public double getWeight() {
		return weight;
	}
	
	public void setWeight(double inputWeight) {
		weight = inputWeight;
	}
	
	public void nextValidVote(ArrayList<Candidate> candidates) {
		while(isInvalid(candidates, this.get(0)) && this.size() > 1) {
			this.remove(0);
		}
	}
	
	public Boolean isInvalid(ArrayList<Candidate> candidates, String name) {
		Candidate candidate = null;
		
		for(int i=0; i<candidates.size(); i++) {
			if(candidates.get(i).getName().equalsIgnoreCase(name)) {
				candidate = candidates.get(i);
				break;
			}
		}
		
		return !(candidate.valid);
	}
}
