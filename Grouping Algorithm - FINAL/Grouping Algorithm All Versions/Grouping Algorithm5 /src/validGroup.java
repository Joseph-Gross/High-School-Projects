import java.util.*;

public class validGroup {

	private int score;
	private ArrayList<String> pairs;
	
	public validGroup(String input){
		score = 0;
		pairs = new ArrayList<String>();
		for(int x = 0; x < input.length(); x = x +2){
			String p = input.substring(x, x+2);
			pairs.add(p);
		}	
	}
	
	public ArrayList<String> getPairs(){
		return pairs;
	}
	
	public int getScore(){
		return score;
	}
	
	public void setScore(int n){
		score = n;
	}
	
	public void outputPairs(){
		System.out.println(pairs);
	}
	
}